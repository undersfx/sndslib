#!/usr/bin/env python3
# snds cli by @undersfx


from sndslib import sndslib
from argparse import ArgumentParser
from sndslib.__version__ import __version__
from sndslib.utils import Presenter
from sndslib.exceptions import SndsHttpError, SndsCliError


parser = ArgumentParser(prog='snds', description='Searches and formats the SNDS dashboard data')

parser.add_argument('-V', '--version', action='version', version=f'sndslib {__version__}',
                    help='returns the version of sndslib')

parser.add_argument('-k', action='store', dest='key',
                    help='snds access key automated data access',
                    required=True)

parser.add_argument('-d', action='store', dest='date',
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


class Cli:
    def __init__(self, key, date=None, presenter=Presenter()) -> None:
        self.key = key
        self.date = date
        self.presenter = presenter
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
        self.presenter.summary(_summary, self.blocked_ips)

    def ip_data(self, ip):
        _ip_status = sndslib.search_ip_status(ip, self.usage_data)
        if _ip_status:
            self.presenter.ip_data(_ip_status)
        else:
            print('No data found for the given IP.')

    def list_blocked_ips(self):
        self.presenter.list_blocked_ips(self.blocked_ips)

    def list_blocked_ips_rdns(self):
        res = sndslib.get_ip_rdns(self.blocked_ips)
        self.presenter.list_blocked_ips_rdns(res)


def main():
    args = parser.parse_args()
    command = Cli(args.key, args.date)

    try:
        if args.s:
            command.summary()

        if args.ip:
            command.ip_data(args.ip)

        if args.l:
            command.list_blocked_ips()

        if args.r:
            command.list_blocked_ips_rdns()
    except SndsHttpError as e:
        raise SndsCliError(e)
