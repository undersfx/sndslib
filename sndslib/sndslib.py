#!/usr/bin/env python3
# sndslib by @undersfx

r"""
Facilita a administração dos IPs listados no painel Sender Network Data Service (Microsoft).

Exemplo de Uso:

    >>> from sndslib import sndslib
    >>> r = sndslib.get_ip_status('mykey')
    >>> blocked_ips = sndslib.list_blocked_ips(r)
    [1.1.1.1, 2.2.2.2, 3.3.3.3]

    >>> r = sndslib.get_data('mykey')
    >>> sndslib.summarize(r)
    {'red': 272, 'green': 710, 'yellow': 852, 'traps': 1298, 'ips': 1834, 'date': '12/31/2019'}

    >>> sndslib.search_ip_status('3.3.3.3', r)
    {'activity_end': '12/31/2019 7:00 PM',
    'activity_start': '12/31/2019 10:00 AM',
    'comments': '',
    'complaint_rate': '< 0.1%',
    'data_commands': '1894',
    'filter_result': 'GREEN',
    'ip_address': '3.3.3.3',
    'message_recipients': '1894',
    'rcpt_commands': '1895',
    'sample_helo': '',
    'sample_mailfrom': '',
    'trap_message_end': '',
    'trap_message_start': '',
    'traphits': '0'}
"""

from urllib.request import urlopen
import socket
import re


def get_ip_status(key):
    """Busca os ranges bloqueados no SNDS Automated Data Access."""

    response = urlopen(f'https://sendersupport.olc.protection.outlook.com/snds/ipStatus.aspx?key={key}')

    assert response.status == 200, 'Invalid return code: {}'.format(response.status)

    csv = list(response.read().decode('utf-8').split('\r\n'))

    return csv


def get_data(key, date=None):
    """Busca os dados de uso dos IP no SNDS Automated Data Access."""

    if date:
        response = urlopen(f'https://sendersupport.olc.protection.outlook.com/snds/data.aspx?key={key}&date={date}')
    else:
        response = urlopen(f'https://sendersupport.olc.protection.outlook.com/snds/data.aspx?key={key}')

    assert response.status == 200, 'Invalid return code: {}'.format(response.status)

    csv = list(response.read().decode('utf-8').split('\r\n'))

    return csv


def summarize(response):
    """Recebe a tabela com dados de uso dos IPs (sndslib.get_data) e retorna o status geral.

    >>> r = sndslib.get_data('mykey')
    >>> sndslib.summarize(r)
    {'red': 272, 'green': 710, 'yellow': 852, 'traps': 1298, 'ips': 1834, 'date': '12/31/2019'}
    """

    # Contagem de incidências do status e total de spamtraps
    summary = {'red': 0, 'green': 0, 'yellow': 0, 'traps': 0, 'ips': len(response) - 1, 'date': ''}

    for i in range(len(response) - 1):
        line = response[i].split(',')

        if line[6] == 'GREEN':
            summary['green'] += 1
        elif line[6] == 'YELLOW':
            summary['yellow'] += 1
        else:
            summary['red'] += 1

        if line[10].isnumeric():
            summary['traps'] += int(line[10])

    summary['date'] = line[2][:10]

    return summary


def search_ip_status(ip, response):
    """Porcura pelos status de um IP especifico nos dados de uso de IP (sndslib.get_data).

    >>> r = sndslib.get_data('mykey')
    >>> sndslib.search_ip_status('3.3.3.3', r)
    {'activity_end': '12/31/2019 7:00 PM',
    'activity_start': '12/31/2019 10:00 AM',
    'comments': '',
    'complaint_rate': '< 0.1%',
    'data_commands': '1894',
    'filter_result': 'GREEN',
    'ip_address': '3.3.3.3',
    'message_recipients': '1894',
    'rcpt_commands': '1895',
    'sample_helo': '',
    'sample_mailfrom': '',
    'trap_message_end': '',
    'trap_message_start': '',
    'traphits': '0'}
    """

    for line in response:
        if re.search(ip, line):
            line = line.split(',')
            break
    else:
        return False

    ip_data = {
        'ip_address': line[0],
        'activity_start': line[1],
        'activity_end': line[2],
        'rcpt_commands': line[3],
        'data_commands': line[4],
        'message_recipients': line[5],
        'filter_result': line[6],
        'complaint_rate': line[7],
        'trap_message_start': line[8],
        'trap_message_end': line[9],
        'traphits': line[10],
        'sample_helo': line[11],
        'sample_mailfrom': line[11],
        'comments': line[12],
    }

    return ip_data


def list_blocked_ips(response):
    """Calcula a lista de IPs bloqueados com base na lista de ranges bloqueados (sndslib.get_ip_status).

    >>> sndslib.get_ip_status('mykey')
    ['1.1.1.1,1.1.1.3,Yes,Blocked due to user complaints or other evidence of spamming']
    >>> sndslib.list_blocked_ips(r)
    [1.1.1.1, 1.1.1.2, 1.1.1.3]
    """

    # Lista que receberá o total de IPs bloqueados
    lista = []

    rangestart = []
    rangeend = []

    # Calcula a diferença entre IP de inicio fim do range bloqueado
    for x in range(len(response) - 1):
        rangestart.append(response[x].split(',')[0])
        rangeend.append(response[x].split(',')[1])

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
                inicial[3] = '0'
            elif int(inicial[1]) < 255:
                inicial[1] = str(int(inicial[1]) + 1)
                inicial[2] = inicial[3] = '0'
            elif int(inicial[1]) < 255:
                inicial[0] = str(int(inicial[0]) + 1)
                inicial[1] = inicial[2] = inicial[3] = '0'

            # Adiciona IP atualizado a lista
            lista.append('.'.join(inicial))

    return lista


def list_blocked_ips_rdns(ips: list) -> list:
    """Busca o host de uma lista de endereços IP (sndslib.list_blocked_ips).

    >>> sndslib.list_blocked_ips_rdns(['1.1.1.1', '1.1.1.2'])
    [{'ip': '1.1.1.1', 'rdns': 'foo.bar.exemple.com'},
     {'ip': '1.1.1.2', 'rdns': 'foo2.bar.exemple.com'}]
    """

    data = []

    if not isinstance(ips, list):
        # Caso seja passado apenas um IP
        try:
            ips = str(ips)
            rdns = socket.gethostbyaddr(ips)[0]
            data.append({'ip': ips, 'rdns': rdns})
        except socket.error as e:
            # 'socket.gethostbyaddr' levanta exceção caso o IP não tenha rdns
            data.append({'ip': ips, 'rdns': str(e)})

        return data
    else:
        # Caso seja passada uma lista de IPs
        for ip in ips:
            try:
                rdns = socket.gethostbyaddr(ip)[0]
                data.append({'ip': str(ip), 'rdns': rdns})
            except socket.error as e:
                data.append({'ip': str(ip), 'rdns': str(e)})

        return data
