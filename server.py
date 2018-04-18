import sys
from socket import *
import _thread as thread

host = '127.0.0.1'
server_port = int(sys.argv[1])

def conected(con, client):
    print('Conectador por {}'.format(client))

    msg = con.recv(1024)
    print('O cliente {} enviou a menssagem {}'.format(client,msg))
    print('Finalizando conexao do cliente {}'.format(client))
    con.close()
    thread.exit()

s = socket(AF_INET, SOCK_STREAM)

orig = (host, server_port)
s.bind(orig)
s.listen(1)

while True:
    con, client = s.accept()
    thread.start_new_thread(conected, tuple([con,client]))

s.close()