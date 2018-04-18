from socket import *
import _thread as thread
import _thread

host = '127.0.0.1'              # Endereco IP do Servidor
server_port = 5152            # Porta que o Servidor esta

def conectado(con, cliente):
    print('Conectado por', cliente)

    while True:
        msg = con.recv(1024)
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