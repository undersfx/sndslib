#!/usr/bin/env python3
# SNDSLIB by @undersfx

r"""
Facilita a administração dos IPs listados no painel Sender Network Data Service (Microsoft).

Exemplo de Uso:

	>>>import sndslib
	>>>r = sndslib.get('mykey')
	>>>ips = sndslib.lista(r)
	>>>print('\n'.join(ips))
Ou:
	>>>print('\n'.join(sndslib.reverso(ips)))

Mais informações em:

[SNDS](https://sendersupport.olc.protection.outlook.com/snds/FAQ.aspx?wa=wsignin1.0)

[SNDS Automated Data Access](https://sendersupport.olc.protection.outlook.com/snds/auto.aspx)
"""

def get(key):
	"""Busca IPs bloqueados no SNDS Automated Data Access. Recebe chave de identificação SNDS ADA e retorna um objeto requests.Response com o CSV de ranges bloqueados."""

	from requests import get

	r = get('https://sendersupport.olc.protection.outlook.com/snds/ipStatus.aspx?key=' + key)

	return r

def lista(response):
	"""Recebe um requests.Response com ranges bloqueados e retorna array de todos ips bloqueados."""
	
	# Array que recebera o total de IPs bloqueados
	lista = []

	# Transforma o CSV de retorno em uma lista
	csv = list(response.text.split('\r\n'))

	rangestart = []
	rangeend = []

	# Calcula a diferença entre IP de inicio fim do range bloqueado
	for x in range(len(csv) - 1):
		rangestart.append(csv[x].split(',')[0])
		rangeend.append(csv[x].split(',')[1])

		# Adiciona primeiro IP a lista de bloqueado ao array
		lista.append(rangestart[x])

		# Quebra os octetos do IP para calcular a diferenca entre IP inicial e final
		inicial = rangestart[x].split('.')
		final = rangeend[x].split('.')

		# Calcula o próximo IP bloqueado se existir mais de um no range (inicial != final)
		while inicial != final:
			if int(inicial[3]) < 255:
				inicial[3] = str(int(inicial[3]) + 1)
			elif int(inicial[2]) < 255:
				inicial[2] = str(int(inicial[2]) + 1)
			elif int(inicial[1]) < 255:
				inicial[1] = str(int(inicial[1]) + 1)
			elif int(inicial[1]) < 255:
				inicial[0] = str(int(inicial[0]) + 1)

			# Adiciona IP atualizado ao array
			lista.append('.'.join(inicial))

	return lista

def reverso(ips, separador=';'):
	"""Recebe uma lista de IPs e retorna um array com o ip e host."""

	from socket import gethostbyaddr

	# Caso seja passado apenas um IP
	if type(ips) == str:
		try:
			ips = ips + separador + gethostbyaddr(ips)
		except Exception as e:
			# 'gethostbyaddr' levanta exceção caso o IP não tenha rDNS
			ips = ips + separador + str(e)
			
		return ips

	# Caso seja passada uma lista de IPs
	for x in range(len(ips)):
		try:
			ips[x] = ips[x] + separador + gethostbyaddr(ips[x])[0]
		except Exception as e:
			ips[x] = ips[x] + separador + str(e)

	return ips
