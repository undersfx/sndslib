#!/usr/bin/env python3
# snds cli by @undersfx

from __future__ import absolute_import
from sndslib import sndslib
from argparse import ArgumentParser
from .__version__ import __version__


# Argument's instructions
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


def format_list_blocked_ips(blocked_ips):
    print('\n'.join(blocked_ips))


def format_list_blocked_ips_rdns(blocked_ips_rdns):
    for ip in blocked_ips_rdns:
        print(ip['ip'] + ';' + ip['rdns'])


def format_ip_status(summary, blocked_ips):
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


def format_ip_data(ipdata):
    message = (
        f"Activity: {ipdata['activity_start']} until {ipdata['activity_end']} \n"
        f"IP: {ipdata['ip_address']:>15} \n"
        f"Messages: {ipdata['message_recipients']:>9} \n"
        f"Filter: {ipdata['filter_result']:>11} \n"
        f"Complaint: {ipdata['complaint_rate']:>8} \n"
        f"Trap Hits: {ipdata['traphits']:>8} \n"
    )
    print(message)


# Parse and execution of the arguments
def main():
    blocked_ips = None
    rdata = None
    args = parser.parse_args()

    # Open SNDS Connection
    if args.s or args.ip:
        if args.data:
            rdata = sndslib.get_data(args.key, args.data)
        else:
            rdata = sndslib.get_data(args.key)

    if not args.ip:
        rstatus = sndslib.get_ip_status(args.key)
        blocked_ips = sndslib.list_blocked_ips(rstatus)

    # Arguments execution chain
    if args.r:
        rdns = sndslib.list_blocked_ips_rdns(blocked_ips)
        format_list_blocked_ips_rdns(rdns)
    elif args.l:
        format_list_blocked_ips(blocked_ips)

    if args.s:
        summary = sndslib.summarize(rdata)
        format_ip_status(summary, blocked_ips)
    elif args.ip:
        ipdata = sndslib.search_ip_status(args.ip, rdata)
        if ipdata:
            format_ip_data(ipdata)
        else:
            print('IP not found')


if __name__ == '__main__':
    main()
