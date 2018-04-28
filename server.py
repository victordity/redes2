import binascii
from socket import *
import thread
import binascii
import sys


host = '127.0.0.1'

# server_port = argv[1]
server_port = 5152


def conectado(con, cliente):
    print('Conectado por', cliente)

    while True:
        msg = con.recv(1024)
        print('A mensagem recebida foi: {}'.format(msg))
        msgValid = utils.decode16(msg)
        print('A mensagem descriptografada eh: {}'.format(msgValid))
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
