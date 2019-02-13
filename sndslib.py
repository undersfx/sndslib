#!/usr/bin/env python3
# sndslib by @undersfx

r"""
Facilita a administração dos IPs listados no painel Sender Network Data Service (Microsoft).

Exemplo de Uso:

	>>>import sndslib
	>>>r = sndslib.getipstatus('mykey')
	>>>ips = sndslib.lista(r)
	>>>print('\n'.join(ips))
Ou:
	>>>print('\n'.join(sndslib.reverso(ips)))

Mais informações em:

[SNDS](https://sendersupport.olc.protection.outlook.com/snds/FAQ.aspx?wa=wsignin1.0)

[SNDS Automated Data Access](https://sendersupport.olc.protection.outlook.com/snds/auto.aspx)

[Mitigação de IPs bloqueados](https://support.microsoft.com/en-us/supportrequestform/8ad563e3-288e-2a61-8122-3ba03d6b8d75)
"""

from urllib.request import urlopen
from socket import gethostbyaddr
import re

def getipstatus(key):
	"""Busca IPs bloqueados no SNDS Automated Data Access. Recebe chave de identificação SNDS ADA para IpStatus e retorna um objeto requests.Response com o CSV de ranges bloqueados."""

	r = urlopen('https://sendersupport.olc.protection.outlook.com/snds/ipStatus.aspx?key={}'.format(key))

	assert r.status == 200, 'código de retorno inválido: {}'.format(r.status)

	return r

def getdata(key, date=None):
	"""Busca os dados de uso do SNDS Automated Data Access. Recebe chave de identificação SNDS ADA para Data e retorna um objeto requests.Response com o CSV de ranges bloqueados."""

	if date:
		r = urlopen('https://sendersupport.olc.protection.outlook.com/snds/data.aspx?key={}&date={}'.format(key, date))
	else:
		r = urlopen('https://sendersupport.olc.protection.outlook.com/snds/data.aspx?key={}'.format(key))

	assert r.status == 200, 'código de retorno inválido: {}'.format(r.status)

	return r

def resumo(response):
	"""Recebe um requests.Response com dados dos IPs e retorna um dict com o status geral"""

	# Transforma os dados do get em uma lista
	csv = list(response.read().decode('utf-8').split('\r\n'))

	# Contagem de incidências do status e total de spamtraps
	resumo = {'red':0, 'green':0, 'yellow':0, 'traps':0, 'ips': len(csv) - 1, 'date':''}

	for i in range(len(csv) - 1):
		line = csv[i].split(',')


		if line[6] == 'GREEN':
			resumo['green'] += 1
		elif line[6] == 'YELLOW':
			resumo['yellow'] += 1
		else:
			resumo['red'] += 1

		if line[10].isnumeric():
			resumo['traps'] += int(line[10])

	resumo['date'] = line[2][:10]

	return resumo

def search_ip_status(ip, rdata):

	csv = list(rdata.read().decode('utf-8').split('\r\n'))

	for line in csv:
		if re.search(ip, line):
			line = line.split(',')
			break
	else:
		return None
	
	ip_data = {'ip_address':line[0],
				'activity_start':line[1],
				'activity_end':line[2],
				'rcpt_commands':line[3],
				'data_commands':line[4],
				'message_recipients':line[5], 
				'filter_result':line[6], 
				'complaint_rate':line[7],
				'trap_message_start':line[8],
				'trap_message_end':line[9],
				'traphits':line[10],
				'sample_helo':line[11],
				'sample_mailfrom':line[11],
				'comments':line[12],
			}

	return ip_data

def lista(response):
	"""Recebe um requests.Response com ranges bloqueados e retorna lista de todos ips bloqueados."""

	# Lista que receberá o total de IPs bloqueados
	lista = []

	# Transforma os dados do get em uma lista
	csv = list(response.read().decode('utf-8').split('\r\n'))

	rangestart = []
	rangeend = []

	# Calcula a diferença entre IP de inicio fim do range bloqueado
	for x in range(len(csv) - 1):
		rangestart.append(csv[x].split(',')[0])
		rangeend.append(csv[x].split(',')[1])

		# Adiciona primeiro IP a lista de bloqueado a lista
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

			# Adiciona IP atualizado a lista
			lista.append('.'.join(inicial))

	return lista

def reverso(ips):
	"""Recebe uma lista de IPs e retorna um dict com o ip e host."""

	# Dict que será retornado
	rdns = {}

	# Caso seja passado apenas um IP
	if type(ips) == str:
		try:
			rdns[str(ips)] = gethostbyaddr(ips)[0]

		# Função 'gethostbyaddr' levanta exceção caso o IP não tenha rDNS
		except Exception as e:
			rdns[str(ips)] = str(e)

		return rdns

	# Caso seja passada uma lista de IPs
	for ip in ips:
		try:
			rdns[str(ip)] = gethostbyaddr(ip)[0]

		# Função 'gethostbyaddr' levanta exceção caso o IP não tenha rDNS
		except Exception as e:
			rdns[str(ip)] = str(e)

	return rdns
