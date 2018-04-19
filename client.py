import binascii
import socket
import sys
def encode16(message):
    mb16 = binascii.hexlify(bytes(message, "utf-8"))
    return mb16


# host= sys.argv[1]
host = '127.0.0.1'

# server_port = sys.argv[2]
server_port = 5152

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
dest = (host, server_port)
s.connect(dest)

# msg = sys.argv[3]
msg = 'ABC'
mb16 = encode16(msg)
msgb = msg.encode('utf-8')

s.send(mb16)
s.close()
