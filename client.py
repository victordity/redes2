#from socket import *
import sys


def encode16(message):
    encoded = binascii.hexlify(bytes(message, "utf-8"))
    encoded = str(encoded).strip("b")
    encoded = encoded.strip("")
    return encoded


host = '127.0.0.1'
server_port = 5152
# s = socket(AF_INET, SOCK_STREAM)
dest = (host, server_port)
# s.connect(dest)

msg = ("Mensagem de teste")
# msgb = msg.encode('utf-8')
msgb16 = encode16(msg)
print(msgb16)
# s.send(msgb16)
# s.close()
