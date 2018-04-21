import binascii
import socket
import sys
from typing import TextIO


def getLine(arquivo):
    entrada = open(arquivo, 'r')  # type: TextIO # Atribuir utf-8 caso necessario
    line = entrada.readline()
    return line


def encode16(message):
    msg = message.encode("utf-8")
    mb16 = binascii.hexlify(msg)
    return mb16


host = '127.0.0.1'

# server_port = sys.argv[1]
server_port = 5152

# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
dest = (host, server_port)
# s.connect(dest)

# arquivo = sys.argv[2]
arquivo = 'teste.txt'
linha = getLine(arquivo)

# msg = sys.argv[3]
msg = 'ABC'
mb16 = encode16(msg)
# msgb = msg.encode('utf-8')
print('A mensagem a ser enviada eh: {}'.format(mb16))
# s.send(mb16)
# s.close()