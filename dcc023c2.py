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

        print("Error #%d: %s", error_message)
        sys.exit(-1)

    s.listen(5)
    print("Esperando conexao")
    while True:
        con, cliente = s.accept()
        # lock acquired by client
        print_lock.acquire()
        print('\nConectado a :', cliente[0], ':', cliente[1])
        # Começa nova thread
        start_new_thread(conectado, (con, OUTPUT))
    s.close()


def conectado(con, OUTPUT):

    # recebe sincronizacao
    print("recebeu conexao")
    pkg = con.recv(2)
    pkg = decode16(pkg)
    epkg = b''
    idAnterior = '01'
    arquivoSaida = open(OUTPUT, 'wb')

    while pkg != epkg:
        epkg = pkg
        if pkg == b'd' or pkg == b'dc' or pkg == b'dcc' or pkg == b'dcc0' or pkg == b'dcc02' or pkg == b'dcc023' \
            or pkg == b'dcc023c' or pkg == b'dcc023c2' or pkg == b'dcc023c2d' or pkg == b'dcc023c2dc' \
            or pkg == b'dcc023c2dcc' or pkg == b'dcc023c2dcc0' or pkg == b'dcc023c2dcc02' or pkg == b'dcc023c2dcc023' \
            or pkg == b'dcc023c2dcc023c':
            pkg_aux = con.recv(2)
            pkg+= decode16(pkg_aux)

        # quadro esta alinhado - começa a recepçao
        elif pkg == b'dcc023c2dcc023c2':

            tam = con.recv(8)
            tam = decode16(tam).decode()

            check = con.recv(10)
            check = decode16(check).decode()

            id = con.recv(4)
            id = decode16(id).decode()

            flag = con.recv(4)
            flag = decode16(flag).decode()

            data = con.recv(int(tam)*2)
            data = decode16(data).decode()

            quadro = '{}{}{}{}{}{}'.format(pkg.decode(), tam, 0, id, flag, data)

            checksum = ichecksum(quadro, int(check))
          # print("\n O chesum e:::", checksum)

            if checksum == 0:
                # Verifica o id pra ver se nao eh quadro repetido
                quadroAck = setAck(quadro)
                if id != idAnterior:
                    idAnterior = id
                    # Escreve no outpub
                    arquivoSaida.write(data.encode())
                    # Envia ack
                    print("\n\n", quadroAck)
                    con.send(encode16(quadroAck))
                    pkg = con.recv(2)
                    pkg = decode16(pkg)
                else:
                    # Quadro enviado repetidamente, envia o ack para confirmalo
                    print(quadroAck)
                    con.send(encode16(quadroAck))


        else:
            pkg = con.recv(2)
            pkg = decode16(pkg)
            epkg = b''

    print('Finalizando conexao do cliente')
    arquivoSaida.close()
    con.close()


def emuladorClient(host, SERVER, INPUT, OUTPUT):

    SERVER = int(SERVER)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
    s.connect((host, SERVER))
    #message = input("hallo")
    inputFile = open(INPUT, 'rb')
    # dados = inputFile.read()
    # Pega o arquivo completo em um vetor onde cada posicao do vetor eh uma linha do texto
    # data = inputFile.readlines()s
    # numQuadros = len(data)
    # tam = len(dados)
    id = '01'

    # Inicia loop para enviar todos os quadros while(tiver quadros)
    # Define id do quadro
    for line in inputFile:
        if id == '00':
            id = '01'
        else:
            id = '00'
        # Cria o quadro no formato da especificacao
        quadro = criaQuadro(line.decode(), id)
        # Pega o ack do quadro inicializado com 00 ps(getAck eh diferente de setAck)
        ack = getAck(quadro)
        #print('Enviando Mensagem')
        dadosCodificados = encode16(quadro)
        s.send(dadosCodificados)
        tam = len(dadosCodificados)
        # Ack chegou?
        s.settimeout(1)  # tempo de esperar para o ACK
        while ack != '01':
            try:
                resposta, addr = s.recvfrom(tam)
                print("\n\n", decode16(resposta).decode())
                ack = getAck(decode16(resposta)).decode() #extrai o ACK
                #print("ACK recebido foi", ack)
            except socket.timeout:
                s.send(dadosCodificados)

       #print(ack)
    s.close()

def getSync(quadro):
    sync = quadro[:16]
    return sync

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

    #msg = message.encode("utf-8")
    #print(message)
    b = binascii.unhexlify(message)
    return b

def criaQuadro(line, id):

    length = maskLength(len(line))
   # #length = socket.ntohl(int(length))
   #  length = socket.ntohl(len(line))
   #  length - maskLength(length)
    flags = '00'
    quadro = ('{}{}{}{}{}{}{}'.format(SYNC, SYNC, length, 0, id, flags, line))
    checksum = ichecksum(quadro)
    quadroCheck = ('{}{}{}{}{}{}{}'.format(SYNC, SYNC, length, checksum, id, flags, line))
    #print("O checksum [e esse aqui no cliente:", checksum)
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

def getChecksum(quadro):
    tamQuadro = len(quadro)
    length = int(quadro[17:20])
    check = quadro[20:(tamQuadro - (length + 4))]
    newQuadro = (quadro[:20] + '0' + quadro[(tamQuadro - (length + 4)):])
    return check, newQuadro


def setAck(quadro):
    tamQuadro = len(quadro)
    length = int(quadro[17:20])
    quadroACK = quadro[:(tamQuadro - (length + 2))] + '01' + quadro[(tamQuadro - length):]
    return quadroACK

def getAck(quadro):
    tamQuadro = len(quadro)
    length = int(quadro[17:20])
    ack = quadro[(tamQuadro - (length + 2)):(tamQuadro - length)]
    return ack

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
