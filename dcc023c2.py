import sys
import socket
import threading as thread
from _thread import *

print_lock = thread.Lock()


def emuladorServer(SERVER_PORT, INPUT, OUTPUT):
    # SERVER_PORT = argv[1]
    HOST = '127.0.0.1'
    PORT = 5000
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
    except socket.error as error_message:

        print("Error #%d: %s", error_message[0], error_message[1])
        sys.exit(-1)

    s.listen(5)
    print("Esperando conexao")
    while True:
        con, cliente = s.accept()
        # lock acquired by client
        print_lock.acquire()
        print('\nConectado a :', cliente[0], ':', cliente[1])
        # Começa nova thread
        start_new_thread(conectado, (con,cliente))
    s.close()


def conectado(con,cliente):
    print('Conectado por', con)

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
        data = con.recv(1024).decode()
        if not data:
            print('Bye')
            print_lock.release()
            break
        print("\nRecebi do usuario " + str(data))

        data = str(data).upper()
        con.send(data.encode())
        print(data.encode())
    # print('Finalizando conexao do cliente', cliente)
    con.close()


def emuladorClient(IP, SERVER_PORT, INPUT, OUTPUT):
    host = '127.0.0.1'

    SERVER = 5000
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
    s.settimeout(1)  # dse detectado demora na resposta timeout
    s.connect((host, SERVER))
    message = input("hallo")

    # while message != 'q':
    #     s.send(message.encode())
    #
    #     msg = s.recv(1024).decode()
    #     print('\nRecebido:' + msg)
    #
    #     message = input("\nInsira sua mensagem ->")
    # s.close()
    ack = False

    while not ack:
        try:
            ack,addr = s.recvfrom(1024)
        except socket.timeout:
            s.send(message)
    print(ack)
    s.close()

# fileName = sys.argv[2]
# fileName = 'teste.txt'
# quadros = enquadramento(fileName)
# msg = sys.argv[3]
# msg = 'ABC'
# mb16 = utils.encode16(msg)
# msgb = msg.encode('utf-8')
# print('A mensagem a ser enviada eh: {}'.format(mb16))
# s.close()

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


def getText(arquivo):

    entrada = open(arquivo, 'r')
    line = entrada.read()
    tam = len(line)
    return line


def main():
    flag = sys.argv[1]
    if flag == '-s':
        emuladorServer(sys.argv[2], sys.argv[3], sys.argv[4])

    else:
        emuladorClient(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
    # python dcc023c2.py -s 5000 in out


if __name__ == '__main__':
    Main()
