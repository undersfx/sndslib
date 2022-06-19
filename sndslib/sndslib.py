#!/usr/bin/env python3
# sndslib by @undersfx

r"""
Wrapper library for Microsoft's SNDS Automated Data Access that provides a better API and an easy to use CLI.

Usage:

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
from ipaddress import IPv4Address
import ipaddress
import socket
import re


__all__ = [
        'get_data',
        'get_ip_status',
        'list_blocked_ips',
        'get_ip_rdns',
        'search_ip_status',
        'summarize',
        ]


def get_ip_status(key):
    """Get blocked IP ranges from SNDS Automated Data Access."""

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
    """Get IP usage data from SNDS Automated Data Access."""

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
    """Calculates a summary based on the IP usage response (sndslib.get_data).

    >>> r = sndslib.get_data('mykey')
    >>> sndslib.summarize(r)
    {'red': 272, 'green': 710, 'yellow': 852, 'traps': 1298, 'ips': 1834, 'date': '12/31/2019'}
    """

    summary = {'red': 0, 'green': 0, 'yellow': 0, 'traps': 0, 'ips': len(response), 'date': ''}

    for ip_status in response:
        status = _adapt_ip_data(ip_status)

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
    """Get a specific IP status based on the IP usage response (sndslib.get_data).

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
            break
    else:
        return {}

    ip_data = _adapt_ip_data(line)

    return ip_data


def _adapt_ip_data(ip_status):
    """Adapt the data from response into a dict based on the response header"""

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

    ip_data = dict(zip(ip_keys, ip_status.split(',')))

    return ip_data


def list_blocked_ips(response):
    """Calculates the list of blocked IPs based on the ip status response (sndslib.get_ip_status).

    >>> sndslib.get_ip_status('mykey')
    ['1.1.1.1,1.1.1.3,Yes,Blocked due to user complaints or other evidence of spamming']

    >>> sndslib.list_blocked_ips(r)
    [1.1.1.1, 1.1.1.2, 1.1.1.3]
    """

    list_of_blocked_ips = []
    for line in response:
        first_ip = IPv4Address(line.split(',')[0])
        last_ip = IPv4Address(line.split(',')[1])

        for network in ipaddress.summarize_address_range(first_ip, last_ip):
            for host in network:
                list_of_blocked_ips.append(str(host))

    return list_of_blocked_ips


def get_ip_rdns(ips) -> list:
    """Get the reverse DNS of a IP or a list of IPs.

    >>> sndslib.get_ip_rdns(['1.1.1.1', '1.1.1.2'])
    [{'ip': '1.1.1.1', 'rdns': 'foo.bar.exemple.com'}, {'ip': '1.1.1.2', 'rdns': 'foo2.bar.exemple.com'}]

    In case there are no valid rDNS for this IP, the return will be a domain error (NXDOMAIN).
    >>> sndslib.get_ip_rdns(['0.0.0.1'])
    [{'ip': '0.0.0.1', 'rdns': 'NXDOMAIN'}]
    """

    def get_rdns(ip):
        try:
            rdns = socket.gethostbyaddr(str(ip))[0]
        except socket.error:
            rdns = 'NXDOMAIN'
        return {'ip': ip, 'rdns': rdns}

    if isinstance(ips, list):
        return [get_rdns(ip) for ip in ips]

    return [get_rdns(ips)]
