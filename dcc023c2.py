import sys


def emuladorServer(SERVER_PORT,INPUT,OUTPUT)
       # SERVER_PORT = argv[1]
    s = socket(AF_INET, SOCK_STREAM)
    host = '127.0.0.1'
    orig = (host, SERVER_PORT)

    s.bind(orig)
    s.listen(1)
    print("Esperando conexao")
    while True:
    con, cliente = s.accept()
    thread.start_new_thread(conectado, tuple([con, cliente]))
    s.close()


def conectado(con, cliente):
    print('Conectado por', cliente)

    while True:
        quadro16 = con.recv(1024)
        quadro = utils.decode16(quadro16)
        sync = 'dcc023c2dcc023c2'
        # Confirmar o sync
        if (quadro[0:16] == sync):
            tamQuadro = len(quadro)
            length = quadro[17:20]
            dado = quadro[(tamQuadro-length):tamQuadro]
            checksum = utils.checksum(dado)

        else:
            pass


        if not msg: break
        print(cliente, msg)

    print('Finalizando conexao do cliente', cliente)
    con.close()
    thread.exit()

def emuladorClient(IP,SERVER_PORT,INPUT,OUTPUT):
host = '127.0.0.1'

# SERVER_PORT = sys.argv[1]

# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
dest = (IP, SERVER_PORT)
# s.connect(dest)
# fileName = sys.argv[2]
fileName = 'teste.txt'
quadros = enquadramento(fileName)
# msg = sys.argv[3]
msg = 'ABC'
mb16 = utils.encode16(msg)
# msgb = msg.encode('utf-8')
print('A mensagem a ser enviada eh: {}'.format(mb16))
# s.close()




flag = sys.argv[1];
if flag == 's':
    emuladorClient(sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5])
    else:
        emuladorServer(sys.argv[2],sys.argv[3],sys.argv[4]);
