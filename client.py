# coding=utf-8
from socket import *
import sys

#host = '127.0.0.1'
host = sys.argv[1]
#erver_port = 5152
server_port = sys.argv[2]

msg = sys.argv[3]

print('Recebemos a informacao do host {} e da porta {} a msg: {}'.format(host, server_port, msg))

# Mensagem a ser enviada em bytes
msgBit = bytes(msg)
'''
# criamos o socket e o conectamos ao servidor
s = socket(AF_INET, SOCK_STREAM)
dest = (host, server_port)
s.connect(dest)

# Mandamos a mensagem
s.send(msg)

data = s.recv(1024)
print('Cliente recebeu: ', data)


s.close()
'''