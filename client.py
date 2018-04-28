import binascii
import socket
import sys
import utils
from typing import TextIO

SYNC = 'dcc023c2';


# Armazena o texto em uma variavel
def getText(arquivo):
    entrada = open(arquivo, 'r')
    line = entrada.read()
    tam = len(line)
    return line

# Retorna um vetor com um quadro em cada posicao
def enquadramento(fileName):
    sync = 'dcc023c2'
    arquivo = open(fileName, 'r')
    idQuadro = '01'
    for line in arquivo:
        if (idQuadro == '01'):
            idQuadro = '00'
        else:
            idQuadro = '01'
        checksum = utils.checksum(line)
        length = utils.maskLength(len(line))
        flags = '00'
        quadro = ('{}{}{}{}{}{}{}'.format(sync,sync,length,checksum,idQuadro,flags,line))
        # s.send(quadro)
        # msg = con.recv(1024)


    return quadro


host = '127.0.0.1'

# server_port = sys.argv[1]
server_port = 5152

# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
dest = (host, server_port)
# s.connect(dest)


# fileName = sys.argv[2]
fileName = 'teste.txt'
quadros = enquadramento(fileName)


# msg = sys.argv[3]
msg = 'ABC'
mb16 = utils.encode16(msg)
# msgb = msg.encode('utf-8')
print('A mensagem a ser enviada eh: {}'.format(mb16))

# s.close()
