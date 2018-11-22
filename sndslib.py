# sndslib by @undersfx

r"""
Facilita a administração dos IPs listados no painel Sender Network Data Service (Microsoft).

Exemplo de Uso:

	>>>import sndslib
	>>>r = sndslib.get('mykey')
	>>>ips = sndslib.lista(r)
	>>>print('\r\n'.join(ips))

Mais informações em:

[SNDS](https://sendersupport.olc.protection.outlook.com/snds/FAQ.aspx?wa=wsignin1.0)

[SNDS Automated Data Access](https://sendersupport.olc.protection.outlook.com/snds/auto.aspx)
"""

def get(key):
	"""Busca IPs bloqueados no SNDS Automated Data Access. Recebe chave de identificação SNDS ADA e retorna um objeto requests.Response com o CSV de ranges bloqueados."""

	from requests import get

	r = get('https://sendersupport.olc.protection.outlook.com/snds/ipStatus.aspx?key=' + key)

	return r

def lista(r):
	"""Recebe um requests.Response com ranges bloqueados e retorna array de todos ips bloqueados."""
	
	# Array que recebera o total de IPs bloqueados
	lista = []

	# Transforma o CSV de retorno em uma lista
	t = list(r.text.split('\r\n'))

	ipstart = []
	ipend = []	

	# Calcula a diferença entre IP de inicio fim do range bloqueado
	for x in range(len(t) - 1):
		ipstart.append(t[x].split(',')[0])
		ipend.append(t[x].split(',')[1])

		# Adiciona primeiro IP a lista de bloqueado ao array
		lista.append(ipstart[x])

		# Quebra os octetos do IP para calcular a diferenca entre IP inicial e final
		a = ipstart[x].split('.')
		b = ipend[x].split('.')

		# Calcula o próximo IP bloqueado se existir mais de um no range (inicial != final)
		while a != b:
			if int(a[3]) < 255:
				a[3] = str(int(a[3]) + 1)
			elif int(a[2]) < 255:
				a[2] = str(int(a[2]) + 1)
			elif int(a[1]) < 255:
				a[1] = str(int(a[1]) + 1)
			elif int(a[1]) < 255:
				a[0] = str(int(a[0]) + 1)

			# Adiciona IP atualizado ao array
			lista.append('.'.join(a))

	return lista

def reverso(r, separador=';'):
	"""Recebe um objeto requests.Response e retorna um array com o ip e reverso."""

	from socket import gethostbyaddr

	dados = lista(r)

	for x in range(len(dados)):
		try:
			dados[x] = dados[x] + separador + gethostbyaddr(dados[x])[0]
		except Exception as e:
			# 'gethostbyaddr' levanta exceção caso o IP não tenha rDNS
			dados[x] = dados[x] + separador + str(e)

	return dados
