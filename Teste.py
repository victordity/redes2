
SYNC = 'dcc023c2'


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
    # msg = message.encode("utf-8")
    # print(message)
    b = binascii.unhexlify(message)
    return b


def criaQuadro(line, id):
    length = maskLength(len(line))
    flags = '00'
    quadro = ('{}{}{}{}{}{}{}'.format(SYNC, SYNC, length, 0, id, flags, line))
    checksum = ichecksum(quadro)
    quadroCheck = ('{}{}{}{}{}{}{}'.format(SYNC, SYNC, length, checksum, id, flags, line))
    # print("O checksum [e esse aqui no cliente:", checksum)
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
    quadroACK = quadro[:(tamQuadro - (length + 2))] + '01'
    return quadroACK


def getAck(quadro):
    tamQuadro = len(quadro)
    length = int(quadro[17:20])
    ack = quadro[(tamQuadro - 2):]
    return ack


def getId(quadro):
    length = int(quadro[16:20])
    id = quadro[(len(quadro) - (length + 4)):(len(quadro) - (length + 2))]
    return id


inputFile = open('alice.txt', 'rb')
id = '01'
for line in inputFile:
    if (id == '00'):
        id = '01'
    else:
        id = '00'
    # Cria o quadro no formato da especificacao
    quadro = criaQuadro(line.decode(), id)
    # Pega o ack do quadro inicializado com 00 ps(getAck eh diferente de setAck)
    novoQuadro = setAck(quadro)
    ack = getAck(novoQuadro)
