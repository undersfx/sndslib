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

from sndslib.exceptions import SndsHttpError
from urllib.request import urlopen
from urllib.error import HTTPError
from datetime import datetime
import ipaddress
import socket
import re


__all__ = [
        'get_data',
        'get_ip_status',
        'list_blocked_ips',
        'list_blocked_ips_rdns',
        'search_ip_status',
        'summarize',
        ]


def get_ip_status(key):
    """Searches SNDS Automated Data Access to blocked IP ranges."""

    try:
        response = urlopen(f'https://sendersupport.olc.protection.outlook.com/snds/ipStatus.aspx?key={key}')
    except HTTPError as e:
        raise SndsHttpError(e)

    csv = []
    if response.status == 200:
        csv = list(response.read().decode('utf-8').split('\r\n'))
        csv = list(filter(None, csv))

    return csv


def get_data(key, date=None):
    """Busca os dados de uso dos IP no SNDS Automated Data Access."""

    try:
        if date:
            response = urlopen(f'https://sendersupport.olc.protection.outlook.com/snds/data.aspx?key={key}&date={date}')
        else:
            response = urlopen(f'https://sendersupport.olc.protection.outlook.com/snds/data.aspx?key={key}')
    except HTTPError as e:
        raise SndsHttpError(e)

    csv = []
    if response.status == 200:
        csv = list(response.read().decode('utf-8').split('\r\n'))
        csv = list(filter(None, csv))

    return csv


def summarize(response):
    """Recebe a tabela com dados de uso dos IPs (sndslib.get_data) e retorna o status geral.

    >>> r = sndslib.get_data('mykey')
    >>> sndslib.summarize(r)
    {'red': 272, 'green': 710, 'yellow': 852, 'traps': 1298, 'ips': 1834, 'date': '12/31/2019'}
    """

    # Contagem de incidências do status e total de spamtraps
    summary = {'red': 0, 'green': 0, 'yellow': 0, 'traps': 0, 'ips': len(response), 'date': ''}

    for ip_status in response:
        status = _format_ip_data(ip_status.split(','))

        if status['filter_result'] == 'GREEN':
            summary['green'] += 1
        elif status['filter_result'] == 'YELLOW':
            summary['yellow'] += 1
        else:
            summary['red'] += 1

        summary['traps'] += int(status['traphits'])

        if not summary.get('date'):
            data = datetime.strptime(status['activity_end'], '%m/%d/%Y %I:%M %p')
            summary['date'] = data.strftime('%m/%d/%Y')

    return summary


def search_ip_status(ip, response):
    """Porcura pelos status de um IP especifico nos dados de uso de IP (sndslib.get_data).

    >>> r = sndslib.get_data('mykey')
    >>> sndslib.search_ip_status('3.3.3.3', r)
    {'activity_end': '12/31/2019 7:00 PM',
    'activity_start': '12/31/2019 10:00 AM',
    'complaint_rate': '< 0.1%',
    'data_commands': '1894',
    'filter_result': 'GREEN',
    'ip_address': '3.3.3.3',
    'message_recipients': '1894',
    'rcpt_commands': '1895',
    'trap_message_end': '',
    'trap_message_start': '',
    'traphits': '0'
    'sample_helo': '',
    'sample_mailfrom': '',
    'comments': ''}
    """

    for line in response:
        if re.search(ip, line):
            line = line.split(',')
            break
    else:
        return {}

    ip_data = _format_ip_data(line)

    return ip_data


def _format_ip_data(ip_status):
    """Nomeia os dados de cada linha de status de IP com base no cabeçalho especificado pelo SNDS"""

    ip_keys = (
        'ip_address',
        'activity_start',
        'activity_end',
        'rcpt_commands',
        'data_commands',
        'message_recipients',
        'filter_result',
        'complaint_rate',
        'trap_message_start',
        'trap_message_end',
        'traphits',
        'sample_helo',
        'sample_mailfrom',
        'comments',
    )
    ip_data = dict(zip(ip_keys, ip_status))

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
    # Calcula a diferença entre IP de inicio fim do range bloqueado
    for value in response:
        inicial = ipaddress.IPv4Address(value.split(',')[0])
        final = ipaddress.IPv4Address(value.split(',')[1])

        lista.append(str(inicial))
        # Calcula o próximo IP bloqueado se existir mais de um no range
        while inicial != final:
            inicial += 1
            # Adiciona IP atualizado a lista
            lista.append(str(inicial))

    return lista


def list_blocked_ips_rdns(ips: list) -> list:
    """Busca o host de uma lista de endereços IP (sndslib.list_blocked_ips).

    >>> sndslib.list_blocked_ips_rdns(['1.1.1.1', '1.1.1.2'])
    [{'ip': '1.1.1.1', 'rdns': 'foo.bar.exemple.com'}, {'ip': '1.1.1.2', 'rdns': 'foo2.bar.exemple.com'}]

    No caso do IP não tem um rDNS válido ou retornar erro na pesquisa, o retorno será 'NXDOMAIN'
    >>> sndslib.list_blocked_ips_rdns(['0.0.0.1'])
    [{'ip': '0.0.0.1', 'rdns': 'NXDOMAIN'}]
    """

    data = []

    if not isinstance(ips, list):
        # Caso seja passado apenas um IP
        ip = str(ips)
        try:
            rdns = socket.gethostbyaddr(ip)[0]
        except socket.error:
            # 'socket.gethostbyaddr' levanta exceção caso o IP não tenha rdns
            rdns = 'NXDOMAIN'

        data.append({'ip': ip, 'rdns': rdns})

        return data
    else:
        # Caso seja passada uma lista de IPs
        for ip in ips:
            try:
                rdns = socket.gethostbyaddr(ip)[0]
            except socket.error:
                rdns = 'NXDOMAIN'

            data.append({'ip': str(ip), 'rdns': rdns})

        return data
