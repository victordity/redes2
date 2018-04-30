import time as t
import binascii
import sys


def getChecksum(quadro):
    tamQuadro = len(quadro)
    length = int(quadro[17:20])
    check = quadro[20:(tamQuadro - (length + 4))]
    return check

class Timer:
    # Classe para medir tempo
    def __enter__(self):
        self.begin = t.time()
        return self

    def __exit__(self, *args):
        self.duration = t.time() - self.begin

# Codifica a entrada para base16
def encode16(message):
    msg = message.encode("utf-8")
    mb16 = binascii.hexlify(msg)
    return mb16

def decode16(message):
    # msg = message.encode("utf-8")
    b = binascii.unhexlify(message)
    return b

def checksum(data):
    # Retorna o cheksum de uma palavra
    sum = 0
    # lê 16 bits (2 WORDs)
    for i in range(0, len(data), 2):
        if i < len(data) and (i + 1) < len(data):
            sum += (ord(data[i]) + (ord(data[i + 1]) << 8))
        elif i < len(data) and (i + 1) == len(data):
            sum += ord(data[i])
    addon_carry = (sum & 0xffff) + (sum >> 16)
    result = (~ addon_carry) & 0xffff
    # swap bytes
    result = result >> 8 | ((result & 0x00ff) << 8)
    return result

# Valida o Checksum aplicado
def confirmChecksum(quadro):
    check = checksum(quadro)

    return True

# !/usr/bin
# iFunção para criar maskara dos tamanho do quadro

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

# Atribuio o componente ACK ao quadro pra ser enviado de volta ao cliente
def ack(quadro):
    tamQuadro = len(quadro)
    length = int(quadro[17:20])
    quadroACK = quadro[:(tamQuadro - (length + 2))] + '01' + quadro[(tamQuadro - length):]
    return quadroACK

def ackSolo(quadro):
    tamQuadro = len(quadro)
    length = int(quadro[17:20])
    ack = quadro[(tamQuadro - (length + 2)):(tamQuadro - length)]
    return ack
# ...
# def emulador():
#     flag = sys.argv[1];
#     if( flag == 'c')
#         client(s)
#         else:
#             servidor()
