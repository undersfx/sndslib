#!/usr/bin/env python3
# snds command by @undersfx

from argparse import ArgumentParser
import sndslib
import time

tempo = time.time()

def lista():
    global rstatus, dados
    try:
        rstatus = sndslib.getipstatus(key)
        dados = sndslib.lista(rstatus)
    except Exception as e:
        print('(Erro: {})'.format(e))
        return
    
    print('\n'.join(dados))
    print('Blocked: {:>6}'.format(len(dados)))

def reverso():
    global key, rstatus, dados
    try:
        rstatus = sndslib.getipstatus(key)
        dados = sndslib.lista(rstatus)
        rdns = sndslib.reverso(dados)
    except Exception as e:
        print('(Erro: {})'.format(e))
        return

    for item in rdns.items():
        print(item[0]+';'+item[1])
    print('Blocked: {:>6}'.format(len(dados)))

def status(data=None):
    global key, rstatus, rdata, dados
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

parser.add_argument('-s', action='store_true',
                    help='retorna o status geral da data mais recente')
parser.add_argument('-l', action='store_true',
                    help='retorna a lista de IPs bloqueados')
parser.add_argument('-r', action='store_true',
                    help='retorna a lista de IPs bloqueados com reversos')
parser.add_argument('-d', action='store', dest='data',
                    help='retorna o status geral na data informada (formato=MMDDYY)')
parser.add_argument('-k', action='store', dest='key',
                    help='chave de acesso snds automated data access', required=True)                    

def main():
    args = parser.parse_args()

    global key, dados, rstatus, rdata
    if args.key: key = args.key

	# Chamada de funções por parâmetros
    if args.r:
        reverso()
    elif args.l:
        lista()

    if args.data:
        status(args.data)
    elif args.s:
        status()

if __name__ == '__main__':
    main()

    print('\nTempo de execução: {:.2f}s'.format(time.time() - tempo))
