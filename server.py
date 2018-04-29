import binascii
from socket import *
import _thread
import binascii
import sys
import utils

def conectado(con, cliente):
    print('Conectado por', cliente)

    while True:
        quadro16 = con.recv(1024)
        quadro = (utils.decode16(quadro16)).decode()
        sync = 'dcc023c2dcc023c2'
        # Confirmar o sync
        if(quadro[0:16] == sync):
            if (utils.confirmChecksum(quadro)):
                # Enviar um ACK
                ack = utils.ack(quadro)
                con.send(ack)
            else:
                # Ignora quadro
                con.send(None)
        else:
            con.send(None)

        if not msg: break
        print(cliente, msg)

    print('Finalizando conexao do cliente', cliente)
    con.close()
    _thread.exit()

host = '127.0.0.1'
# server_port = argv[1]
server_port = 5152

s = socket(AF_INET, SOCK_STREAM)

orig = (host, server_port)
s.bind(orig)
s.listen(1)

print("Esperando conexao")
while True:
    con, cliente = s.accept()
    _thread.start_new_thread(conectado, tuple([con, cliente]))
s.close()
