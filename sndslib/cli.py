#!/usr/bin/env python3
# snds cli by @undersfx

from __future__ import absolute_import
from sndslib import sndslib
from argparse import ArgumentParser
from .__version__ import __version__


# CLI's arguments logic
parser = ArgumentParser(prog='snds', description='Searches and formats the SNDS dashboard data')

parser.add_argument('-V', '--version', action='version', version=f'sndslib {__version__}',
                    help='returns the version of sndslib')

parser.add_argument('-k', action='store', dest='key',
                    help='snds access key automated data access',
                    required=True)

parser.add_argument('-d', action='store', dest='data',
                    help='returns the general status on informed date (format=MMDDYY)')

group1 = parser.add_mutually_exclusive_group()

group1.add_argument('-s', action='store_true',
                    help='returns the general status of the most recent data')

group1.add_argument('-ip', action='store',
                    help='returns the complete status of informed IP')

group1.add_argument('-l', action='store_true',
                    help='returns the blocked IPs list')

group1.add_argument('-r', action='store_true',
                    help='returns the blocked IPs list with reverses')


# Adapter class for sndslib
class Cli:
    def __init__(self, key, date=None) -> None:
        self.key = key
        self.date = date
        self._usage_data = None
        self._blocked_ips = None

    @property
    def usage_data(self):
        if not self._usage_data:
            self._usage_data = sndslib.get_data(self.key, self.date)
        return self._usage_data

    @property
    def blocked_ips(self):
        if not self._blocked_ips:
            _ip_status = sndslib.get_ip_status(self.key)
            self._blocked_ips = sndslib.list_blocked_ips(_ip_status)
        return self._blocked_ips

    def summary(self):
        _summary = sndslib.summarize(self.usage_data)
        self._print_summary(_summary, self.blocked_ips)

    def _print_summary(self, summary, blocked_ips):
        message = (
            f"Date: {summary['date']:>9} \n"
            f"IPs: {summary['ips']:>10} \n"
            f"Green: {summary['green']:>8} \n"
            f"Yellow: {summary['yellow']:>7} \n"
            f"Red: {summary['red']:>10} \n"
            f"Trap Hits: {summary['traps']:>4} \n"
            f"Blocked: {len(blocked_ips):>6}"
        )
        print(message)

    def ip_data(self, ip):
        _ip_data = sndslib.search_ip_status(ip, self.usage_data)
        if _ip_data:
            self._print_ip_data(_ip_data)
        else:
            print('No data found for the given IP.')

    def _print_ip_data(self, ipdata):
        message = (
            f"Activity: {ipdata['activity_start']} until {ipdata['activity_end']} \n"
            f"IP: {ipdata['ip_address']:>15} \n"
            f"Messages: {ipdata['message_recipients']:>9} \n"
            f"Filter: {ipdata['filter_result']:>11} \n"
            f"Complaint: {ipdata['complaint_rate']:>8} \n"
            f"Trap Hits: {ipdata['traphits']:>8} \n"
        )
        print(message)

    def list_blocked_ips(self):
        self._print_list_blocked_ips(self.blocked_ips)

    def _print_list_blocked_ips(self, blocked_ips):
        print('\n'.join(blocked_ips))

    def list_blocked_ips_rdns(self):
        _rdns = sndslib.list_blocked_ips_rdns(self.blocked_ips)
        self._print_list_blocked_ips_rdns(_rdns)

    def _print_list_blocked_ips_rdns(self, blocked_ips_rdns):
        for ip in blocked_ips_rdns:
            print(ip['ip'] + ';' + ip['rdns'])


# Parsing and execution
def main():
    args = parser.parse_args()
    command = Cli(args.key, args.data)

    if args.s:
        command.summary()

    if args.ip:
        command.ip_data(args.ip)

    if args.l:
        command.list_blocked_ips()

    if args.r:
        command.list_blocked_ips_rdns()
