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
    print('''\nData: {:>9}
IPs: {:>10}
Green: {:>8}
Yellow: {:>7}
Red: {:>10}
Trap Hits: {:>4}'''.format(resumo['date'], resumo['ips'], resumo['green'], resumo['yellow'], resumo['red'], resumo['traps']))
    print('Blocked: {:>6}'.format(len(blocked_ips)))

# Instruções dos argumentos
parser = ArgumentParser(prog='snds',
                        description='Busca e formata informações do painel SNDS.',
                        epilog='Para arquivo de configuração: snds @<filename>',
                        fromfile_prefix_chars='@') # Passar parâmetros via arquivos (e.g. snds -s @parametros.txt)

parser.add_argument('-k', action='store', dest='key',
                    help='chave de acesso snds automated data access', required=True)
parser.add_argument('-s', action='store_true',
                    help='retorna o status geral da data mais recente')
parser.add_argument('-d', action='store', dest='data',
                    help='retorna o status geral na data informada (formato=MMDDYY)')                 

group = parser.add_mutually_exclusive_group()

group.add_argument('-l', action='store_true',
                    help='retorna a lista de IPs bloqueados')
group.add_argument('-r', action='store_true',
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

        rstatus = sndslib.getipstatus(args.key)
        blocked_ips = sndslib.lista(rstatus)
        resumo = sndslib.resumo(rdata)

        if args.r: 
            rdns = sndslib.reverso(blocked_ips)
    except Exception as e:
        print('(Erro: {})'.format(e))
        return

	# Cadeia de execução dos argumentos
    if args.r:
        print_reverso(rdns)
    elif args.l:
        print_lista(blocked_ips)

    if args.data:
        print_status(resumo, blocked_ips)
    elif args.s:
        print_status(resumo, blocked_ips)

if __name__ == '__main__':
    main()