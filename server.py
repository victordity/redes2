import binascii
from socket import *
import thread
import binascii
import sys
import utils


host = '127.0.0.1'

# server_port = argv[1]
server_port = 5152


def conectado(con, cliente):
    print('Conectado por', cliente)

    while True:
        quadro16 = con.recv(1024)
        quadro = utils.decode16(quadro16)
        sync = 'dcc023c2dcc023c2'
        # Confirmar o sync
        if (quadro[0:16] == sync):
            tamQuadro = len(quadro)
            length = quadro[17:20]
            dado = quadro[(tamQuadro-length):tamQuadro]
            checksum = utils.checksum(dado)

        else:
            pass


        if not msg: break
        print(cliente, msg)

    print('Finalizando conexao do cliente', cliente)
    con.close()
    thread.exit()

s = socket(AF_INET, SOCK_STREAM)

orig = (host, server_port)

s.bind(orig)
s.listen(1)
print("Esperando conexao")
while True:
    con, cliente = s.accept()
    thread.start_new_thread(conectado, tuple([con, cliente]))
s.close()
