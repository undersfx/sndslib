#!/usr/bin/env python3
# snds command by @undersfx

from argparse import ArgumentParser
import sndslib

def print_lista(blocked_ips):    
    print('\n'.join(blocked_ips))

def print_reverso(rdns):
    for item in rdns.items():
        print(item[0]+';'+item[1])

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

# Instruções dos argumentos
parser = ArgumentParser(prog='snds',
                        description='Busca e formata informações do painel SNDS.',
                        epilog='Para arquivo de configuração: snds @<filename>',
                        fromfile_prefix_chars='@') # Passar parâmetros via arquivos (e.g. snds -s @parametros.txt)

parser.add_argument('-k', action='store', dest='key',
                    help='chave de acesso snds automated data access', required=True)

group1 = parser.add_mutually_exclusive_group()

group1.add_argument('-s', action='store_true',
                    help='retorna o status geral da data mais recente')

group1.add_argument('-ip', action='store',
                    help='retorna o status completo do IP informado')

parser.add_argument('-d', action='store', dest='data',
                    help='retorna o status geral na data informada (formato=MMDDYY)')                 

group2 = parser.add_mutually_exclusive_group()

group2.add_argument('-l', action='store_true',
                    help='retorna a lista de IPs bloqueados')
group2.add_argument('-r', action='store_true',
                    help='retorna a lista de IPs bloqueados com reversos')

# Parse e execução dos argumentos
def main():
    args = parser.parse_args()

    # Conexão com SNDS
    try:
        if args.data:
            rdata = sndslib.getdata(args.key, args.data)
        else:
            rdata = sndslib.getdata(args.key)

        if not args.ip:
            rstatus = sndslib.getipstatus(args.key)
            blocked_ips = sndslib.lista(rstatus)
    except Exception as e:
        print('(Erro: {})'.format(e))
        return

	# Cadeia de execução dos argumentos    
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
        print_ipdata(ipdata)

if __name__ == '__main__':
    main()