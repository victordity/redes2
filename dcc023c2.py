import socket
import sys
import threading as thread
from _thread import *

print_lock = thread.Lock()


def emuladorServer(SERVER_PORT, INPUT, OUTPUT):
    # SERVER_PORT = argv[1]

    # HOST = '127.0.0.1'
    HOST = socket.gethostbyname(socket.getfqdn())
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
        start_new_thread(conectado, (con, cliente))
    s.close()


def conectado(con, cliente):
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


def emuladorClient(host, SERVER, INPUT, OUTPUT):

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
            ack, addr = s.recvfrom(1024)
        except socket.timeout:
            s.send(message)
    print(ack)
    s.close()


def maskLength(n):
    str1 = '000'
    str2 = '00'
    str3 = '0'
    if n < 10:
        str1 = str1 + str(n)
        return (str1)

    elif n < 100:
        str2 = str2 + str(n)
        return (str2)

    elif n < 1000:
        str3 = str3 + str(n)
        return (str3)
    else:
        return (str(n))


def enquadramento(line, idQuadro, sync):
    length = maskLength(len(line))
    length = socket.ntohl(length)
    flags = '00'
    quadro = ('{}{}{}{}{}{}{}'.format(sync, sync, length, 0, idQuadro, flags, line))
    checksum = ichecksum(quadro)
    quadroCheck = ('{}{}{}{}{}{}{}'.format(sync, sync, length, checksum, idQuadro, flags, line))
    # Envia o quadro e recebe o ACK
    # s.send(quadroCheck)
    # ACK = s.recv(1024)

    return quadroCheck


def getText(arquivo):
    entrada = open(arquivo, 'r')
    line = entrada.read()
    tam = len(line)
    return line

def ichecksum(data, sum=0):
    """ Calcula o checksum da internet
        junta cada 8 bits e retorna o valor do checksum
    """
    # make 16 bit words out of every two adjacent 8 bit words in the packet
    # and add them up
    for i in range(0, len(data), 2):
        if i + 1 >= len(data):
            sum += ord(data[i]) & 0xFF
        else:
            w = ((ord(data[i]) << 8) & 0xFF00) + (ord(data[i + 1]) & 0xFF)
            sum += w

    # take only 16 bits out of the 32 bit sum and add up the carries
    while (sum >> 16) > 0:
        sum = (sum & 0xFFFF) + (sum >> 16)

    # one's complement the result
    sum = ~sum

    return sum & 0xFFFF

def main():
    flag = sys.argv[1]
    if flag == '-s':
        emuladorServer(sys.argv[2], sys.argv[3], sys.argv[4])

    else:
        emuladorClient(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])  # python dcc023c2.py -s 5000 in out


if __name__ == '__main__':
    main()
