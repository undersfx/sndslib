#!/usr/bin/env python3
# snds command by @undersfx

import sndslib
from argparse import ArgumentParser
from __init__ import __version__


def print_lista(blocked_ips):
    print('\n'.join(blocked_ips))


def print_reverso(rdns):
    for ip in rdns:
        print(ip['ip'] + ';' + ip['rdns'])


def print_status(resumo, blocked_ips):
    message = (
        f"Data: {resumo['date']:>9} \n"
        f"IPs: {resumo['ips']:>10} \n"
        f"Green: {resumo['green']:>8} \n"
        f"Yellow: {resumo['yellow']:>7} \n"
        f"Red: {resumo['red']:>10} \n"
        f"Trap Hits: {resumo['traps']:>4} \n"
        f"Blocked: {len(blocked_ips):>6}"
    )

    print(message)


def print_ipdata(ipdata):
    message = (
        f"Activity: {ipdata['activity_start']} until {ipdata['activity_end']} \n"
        f"IP: {ipdata['ip_address']:>15} \n"
        f"Messages: {ipdata['message_recipients']:>9} \n"
        f"Filter: {ipdata['filter_result']:>11} \n"
        f"Complaint: {ipdata['complaint_rate']:>8} \n"
        f"Trap Hits: {ipdata['traphits']:>8} \n"
    )

    print(message)


# Argument's instructions
parser = ArgumentParser(prog='snds',
                        description='Searches and formats the SNDS \
                            dashboard data',
                        epilog='You can also use a configuration file using @ \
                            (e.g. "snds -s @parameters.txt")',
                        fromfile_prefix_chars='@')

parser.add_argument('-V', '--version', action='version', version=f'sndslib version {__version__}',
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


# Parse and execution of the arguments
def main():
    args = parser.parse_args()

    # Conection with SNDS
    try:
        if args.data:
            rdata = sndslib.get_data(args.key, args.data)
        else:
            rdata = sndslib.get_data(args.key)

        if not args.ip:
            rstatus = sndslib.get_ip_status(args.key)
            blocked_ips = sndslib.lista(rstatus)
    except AssertionError as e:
        print(e)
        return

    # Arguments execution chain
    if args.r:
        rdns = sndslib.reverso(blocked_ips)
        print_reverso(rdns)
    elif args.l:
        print_lista(blocked_ips)

    if args.s:
        resumo = sndslib.resumo(rdata)
        print_status(resumo, blocked_ips)
    elif args.ip:
        ipdata = sndslib.search_ip_status(args.ip, rdata)
        if ipdata:
            print_ipdata(ipdata)
        else:
            print('IP not found')


if __name__ == '__main__':
    main()
