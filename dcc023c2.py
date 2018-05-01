import socket
import sys
import threading as thread
from _thread import *
import binascii

print_lock = thread.Lock()

SYNC = 'dcc023c2'

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

    print('Conectado por', con,cliente)

    id_anterior = '00'
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
    s.settimeout(1)  # tempo de esperar para o ACK
    s.connect((host, SERVER))
    message = input("hallo")
    inputFile = open(INPUT, 'r')
    dados = inputFile.read()
    tam = len(dados)
    criaQuadro(dados, '00')

    ack = False
    print('Enviando Mensagem')
    dadosCodificados = encode16(dados)
    s.send(dadosCodificados)
    while ack != '01':
        try:
            resposta, addr = s.recvfrom(1024)
            ack = getACK(resposta) #extrai o ACK
            print("ACK recebido foi", ack)
        except socket.timeout:
            s.send(dadosCodificados)
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

def encode16(message):
    msg = message.encode("utf-8")
    mb16 = binascii.hexlify(msg)
    return mb16

def decode16(message):

    # msg = message.encode("utf-8")
    b = binascii.unhexlify(message)
    return b

def criaQuadro(line, id):

    length = maskLength(len(line))
    length = socket.ntohl(length)
    flags = '00'
    quadro = ('{}{}{}{}{}{}{}'.format(SYNC, SYNC, length, 0, id, flags, line))
    checksum = ichecksum(quadro)
    quadroCheck = ('{}{}{}{}{}{}{}'.format(SYNC, SYNC, length, checksum, id, flags, line))
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


def getACK(quadro):
    tamQuadro = len(quadro)
    length = int(quadro[17:20])
    quadroACK = quadro[:(tamQuadro - (length + 2))] + '01' + quadro[(tamQuadro - length):]
    return quadroACK


def getId(quadro):
    length = int(quadro[16:20])
    id = quadro[(len(quadro)-(length + 4)):(len(quadro)-(length + 2))]
    return id


def main():
    flag = sys.argv[1]
    if flag == '-s':
        emuladorServer(sys.argv[2], sys.argv[3], sys.argv[4])

    else:
        emuladorClient(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])  # python dcc023c2.py -s 5000 in out


if __name__ == '__main__':
    main()
