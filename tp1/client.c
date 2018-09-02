#include <stdlib.h>
#include <stdio.h>
#include <string.h>

#include <sys/socket.h>
#include <arpa/inet.h>
#include <netdb.h>



void logexit(const char *str)
{
	perror(str);
	exit(EXIT_FAILURE);
}


int main(int argc, char *argv[])
{
	char *host_do_servidor, *nome_arquivo;
  int s, porto_do_servidor, len, i, tam_buffer;

	host_do_servidor = argv[1];
	porto_do_servidor = atoi(argv[2]);
	nome_arquivo = argv[3];
	tam_buffer = atoi(argv[4]);

    // Faz abertura ativa do host:port do servidor
	struct in_addr inaddr;
	inet_pton(AF_INET, host_do_servidor,
			&inaddr);

    // Faz abertura ativa do porto do servidor
	struct sockaddr_in addr;
	struct sockaddr *addrptr = (struct sockaddr *)&addr;
	addr.sin_family = AF_INET;
	addr.sin_port = htons(porto_do_servidor);
	addr.sin_addr = inaddr;
    memset(addr.sin_zero, 0, 10);

    s = socket(AF_INET, SOCK_STREAM, 0);
    if(s == -1) logexit("socket");

    if(connect(s, addrptr, sizeof(struct sockaddr_in)))
		logexit("connect");

    // Envia o nome do arquivo para o servidor
	ssize_t count;
	count = send(s, nome_arquivo, strlen(nome_arquivo)+1, 0);
	if(count != strlen(nome_arquivo)+1)
		logexit("send");
    //Abre arquivo para escrita
    FILE *fw;
    fw = fopen(nome_arquivo, "w");

    // Recebe os dados do arquivo e escrev
    char buf[tam_buffer + 1];
    printf("Iniciando leitura");
    int tam;
    char verificador;
    while(1) {
        size_t c = recv(s, buf, tam_buffer, 0);
        printf("recebemos %d bytes\n", (int)c);
        puts(buf);
        printf("Verificador fim do arquivo %c \n", buf[tam_buffer - 1]);
        tam = strlen(buf);
        // Escrever no arquivo destino
        printf("Escrevendo a palavra %s de tamanho %d \n", buf, tam-1);
        fwrite(&buf, sizeof(char), tam, fw);

        // Verifica o final da transferencia
        verificador = buf[tam - 1];
        if (verificador == '0') {
            return;
        }
        memset(buf, 0, tam_buffer);
    }

    // sudo iptables -A INPUT -p tcp --dport 5152 -j ACCEPT
	memset(buf, 0, tam_buffer);
	unsigned total = 0;
	while(1) {
		count = recv(s, buf+total, tam_buffer, 0);
		if(count == 0) break;
		total += count;
	}


    fflush(stdout);
    return 0;

}
