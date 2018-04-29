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
def enquadramento(line, idQuadro, sync):

    length = utils.maskLength(len(line))
    flags = '00'
    quadro = ('{}{}{}{}{}{}{}'.format(sync,sync,length,0,idQuadro,flags,line))
    checksum = utils.checksum(quadro)
    quadroCheck = ('{}{}{}{}{}{}{}'.format(sync,sync,length,checksum,idQuadro,flags,line))
    # Envia o quadro e recebe o ACK
    # s.send(quadroCheck)
    # ACK = s.recv(1024)


    return quadroCheck


host = '127.0.0.1'
# server_port = sys.argv[1]
server_port = 5000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
dest = (host, server_port)
s.connect(dest)


# fileName = sys.argv[2]
fileName = 'teste.txt'

# Pegar linha a linha e enquadrar
sync = 'dcc023c2'
arquivo = open(fileName, 'r')
idQuadro = '01'
for line in arquivo:
    if (idQuadro == '01'):
        idQuadro = '00'
    else:
        idQuadro = '01'
    # Enquadra
    quadro = enquadramento(line, idQuadro, sync)
    # Codifica e envia para o servidor
    quadro16 = utils.encode16(quadro)
    s.send(quadro16)
    # Recebe o ACK depois que o tempo passar
    quadroACK = s.recv(1024)
    ack = ackSolo(quadroACK)

# s.close()
