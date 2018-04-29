import sys
import socket
import threading as thread
from _thread import *

print_lock =  thread.Lock()


def emuladorServer(SERVER_PORT,INPUT,OUTPUT):
       # SERVER_PORT = argv[1]
    HOST = '127.0.0.1'
    PORT = 5000
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM,0)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
  

    s.listen(5)
    print("Esperando conexao")
    while True:
        con, cliente = s.accept()
        print_lock.acquire()
        print('conected to :', cliente[0], ':',cliente[1])
        # lock acquired by client
        #print_lock.acquire()
        start_new_thread(conectado,(con,))
    s.close()


def conectado(con):
    print('Conectado por',con)

    # while True:
    #     quadro16 = con.recv(1024)
    #     quadro = utils.decode16(quadro16)
    #     sync = 'dcc023c2dcc023c2'
    #     # Confirmar o sync
    #     if (quadro[0:16] == sync):
    #         tamQuadro = len(quadro)
    #         length = quadro[17:20]
    #         dado = quadro[(tamQuadro-length):tamQuadro]
    #         checksum = utils.checksum(dado)

    #     else:
    #         pass


    #     if not msg: break
    #     print(cliente, msg)
    while True:
        data = con.recv(1024)
        if not data:
            break
    msg = 'Recebi: ' + data
    con.send(msg)
    print(data)
    # print('Finalizando conexao do cliente', cliente)
    con.close()


def emuladorClient(IP,SERVER_PORT,INPUT,OUTPUT):
    host = '127.0.0.1'
    
    SERVER = 5000
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM,0)
    s.connect((host,SERVER))
    message = 'my pistol'
    
    while True:
        s.send(message.encode('ascii'))

        msg = s.recv(1024) 
        print('Recebido:',msg.decode(ascii))
        ans = input('\n Quer continuar?')
        if ans == 'y':
            continue
        else:
            break
    s.close()
# fileName = sys.argv[2]
#fileName = 'teste.txt'
#quadros = enquadramento(fileName)
# msg = sys.argv[3]
# msg = 'ABC'
# mb16 = utils.encode16(msg)
# msgb = msg.encode('utf-8')
# print('A mensagem a ser enviada eh: {}'.format(mb16))
# s.close()
    

flag = sys.argv[1]
if flag == '-s':
    emuladorServer(sys.argv[2],sys.argv[3],sys.argv[4])

else:
    emuladorClient(sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5])