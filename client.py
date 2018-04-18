from socket import *
import sys



host = '127.0.0.1'
server_port = 5152
s = socket(AF_INET, SOCK_STREAM)
dest = (host, server_port)
s.connect(dest)

msg = ("Mensagem de teste")
msgb = msg.encode('utf-8')
s.send(msgb)
s.close()
