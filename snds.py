#!/usr/bin/env python3
# snds command by @undersfx

from argparse import ArgumentParser
import sndslib
import time

# DEBUG
tempo = time.time()

def lista(key):
    global rstatus, dados
    try:
        rstatus = sndslib.getipstatus(key)
        dados = sndslib.lista(rstatus)
    except Exception as e:
        print('(Erro: {})'.format(e))
        return
    
    print('\n'.join(dados))

def reverso(key):
    global rstatus, dados
    try:
        rstatus = sndslib.getipstatus(key)
        dados = sndslib.lista(rstatus)
        rdns = sndslib.reverso(dados)
    except Exception as e:
        print('(Erro: {})'.format(e))
        return

    for item in rdns.items():
        print(item[0]+';'+item[1])

def status(key, data=None):
    global rstatus, rdata, dados
    try:
        if data:
            rdata = sndslib.getdata(key, data)
        else:
            rdata = sndslib.getdata(key)

        rstatus = sndslib.getipstatus(key)
        dados = sndslib.lista(rstatus)
        resumo = sndslib.resumo(rdata)
    except Exception as e:
        print('(Erro: {})'.format(e))
        return

    print('''\nData: {:>9}
IPs: {:>10}
Green: {:>8}
Yellow: {:>7}
Red: {:>10}
Trap Hits: {:>4}'''.format(resumo['date'], resumo['ips'], resumo['green'], resumo['yellow'], resumo['red'], resumo['traps']))
    print('Blocked: {:>6}'.format(len(dados)))

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

	# Cadeia de execução dos argumentos
    if args.r:
        reverso(args.key)
    elif args.l:
        lista(args.key)

    if args.data:
        status(args.key, args.data)
    elif args.s:
        status(args.key)

if __name__ == '__main__':
    main()

    # DEBUG
    print('Tempo de execução: {:.2f}s'.format(time.time() - tempo))