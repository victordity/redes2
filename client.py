import binascii
import socket
import sys
import utils
from typing import TextIO


# Armazena o texto em uma variavel
def getText(arquivo):
    entrada = open(arquivo, 'r')
    line = entrada.read()
    tam = len(line)
    return line

# Retorna um vetor com um quadro em cada posicao
def enquadramento(arquivoArmazenado):
    sync = 'dcc023c2'
    arquivo = open(arquivoArmazenado, 'r')
    idQuadro = 1
    for line in arquivo:
        if (idQuadro == 1):
            idQuadro = 0
        else:
            idQuadro = 1
        checksum = utils.checksum(dado)
        length = utils.maskLength(len(dado))
        flags = 0
        quadro = ('{}{}{}{}{}{}{}'.format(sync,sync,length,checksum,idQuadro,flags,dado))
        # s.send(quadro)
        # msg = con.recv(1024)


    return quadro


host = '127.0.0.1'

# server_port = sys.argv[1]
server_port = 5152

# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
dest = (host, server_port)
# s.connect(dest)

# arquivoArmazenado = sys.argv[2]
arquivoArmazenado = 'teste.txt'


    quadros = enquadramento(arquivoArmazenado)

# msg = sys.argv[3]
msg = 'ABC'
mb16 = utils.encode16(msg)
# msgb = msg.encode('utf-8')
print('A mensagem a ser enviada eh: {}'.format(mb16))

# s.close()
