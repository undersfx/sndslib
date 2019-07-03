#!/usr/bin/env python3
# snds command by @undersfx

from argparse import ArgumentParser
import sndslib

def print_lista(blocked_ips):    
    print('\n'.join(blocked_ips))

def print_reverso(rdns):
    for ip in rdns:
        print(ip['ip'] + ';' + ip['rdns'])

def print_status(resumo, blocked_ips):
    print('''Data: {:>9}
IPs: {:>10}
Green: {:>8}
Yellow: {:>7}
Red: {:>10}
Trap Hits: {:>4}'''.format(resumo['date'], resumo['ips'], resumo['green'], resumo['yellow'], resumo['red'], resumo['traps']))
    print('Blocked: {:>6}'.format(len(blocked_ips)))

def print_ipdata(ipdata):
    print('''IP: {:>15}
Activity: {} until {}
Messages: {:>9}
Filter: {:>11}
Complaint: {:>8}
Trap Hits: {:>8}'''.format(ipdata['ip_address'], ipdata['activity_start'], ipdata['activity_end'], ipdata['message_recipients'], ipdata['filter_result'], ipdata['complaint_rate'], ipdata['traphits']))

# Argument's instructions
parser = ArgumentParser(prog='snds',
                        description='Searches and formats the SNDS dashboard data',
                        epilog='For configuration file: snds @<filename>',
                        fromfile_prefix_chars='@') # Pass parameters through files (e.g. snds -s @parameters.txt)

parser.add_argument('-k', action='store', dest='key',
                    help='snds access key automated data access', required=True)

group1 = parser.add_mutually_exclusive_group()

group1.add_argument('-s', action='store_true',
                    help='returns the general status of the most recent data')

group1.add_argument('-ip', action='store',
                    help='returns the complete status of informed IP')

parser.add_argument('-d', action='store', dest='data',
                    help='returns the general status on informed date (format=MMDDYY)')                 

group2 = parser.add_mutually_exclusive_group()

group2.add_argument('-l', action='store_true',
                    help='returns the blocked IPs list')
group2.add_argument('-r', action='store_true',
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
    except Exception as e:
        print('(Erro: {})'.format(e))
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
