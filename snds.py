#!/usr/bin/env python3
# snds command by @undersfx

from argparse import ArgumentParser
import sndslib
import time

tempo = time.time()

dados = rstatus = rdata = []

def lista():
    global dados
    print('\n'.join(dados))
    print('Blocked: {:>6}'.format(len(dados)))

def reverso():
    global rstatus, dados
    rdns = sndslib.reverso(dados)
    for item in rdns.items():
        print(item[0]+';'+item[1])
    print('Blocked: {:>6}'.format(len(dados)))

def status():
    global rstatus, rdata, dados
    resumo = sndslib.resumo(rdata)
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
parser.add_argument('-k', action='store', dest='key',
                    help='utiliza chave de acesso customizada')
parser.add_argument('-d', action='store', dest='data',
                    help='retorna o status geral na data informada (formato=MMDDYY)')

def main():
    args = parser.parse_args()

    if args.key:
        global key
        key = args.key

    global dados, rstatus, rdata
    try:
        rstatus = sndslib.getipstatus(key)
        rdata = sndslib.getdata(key)
        dados = sndslib.lista(rstatus)
    except Exception as e:
        print('Não foi possível resgatar os dados. (Erro: {})'.format(e))
        return

	# Chamada de funções por parâmetros

    if args.r:
        reverso()
        pass
    elif args.l:
        lista()
        pass

    if args.data:
        pass
    elif args.s:
        status()
        pass

if __name__ == '__main__':
    main()

    print('\nTempo de execução: {:.2f}s'.format(time.time() - tempo))
