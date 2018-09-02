#include <stdlib.h>
#include <unistd.h>
#include <stdio.h>
#include <string.h>
#include <pthread.h>

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
	int s, porto_do_servidor, tam_buffer;

	porto_do_servidor = atoi(argv[1]);
	tam_buffer = atoi(argv[2]);

    printf("Porta : %d\n", porto_do_servidor);
    printf("Buffer: %d\n", tam_buffer);

	s = socket(AF_INET, SOCK_STREAM, 0);
	if(s == -1) logexit("socket");

	struct in_addr inaddr;
	inet_pton(AF_INET, "127.0.0.1", &inaddr);

	struct sockaddr_in addr;
	struct sockaddr *addrptr = (struct sockaddr *)&addr;
	addr.sin_family = AF_INET;
	addr.sin_port = htons(porto_do_servidor);
	addr.sin_addr = inaddr;

	if(bind(s, addrptr, sizeof(struct sockaddr_in)))
		logexit("bind");

	if(listen(s, 10)) logexit("listen");
	printf("esperando conexao\n");

    	while(1) {
		struct sockaddr_in raddr;
		struct sockaddr *raddrptr =
			(struct sockaddr *)&raddr;
		socklen_t rlen = sizeof(struct sockaddr_in);

		int r = accept(s, raddrptr, &rlen);
		if(r == -1) logexit("accept");

		char nome_arquivo[512];
		char buf[tam_buffer];
		char ipcliente[512];
		inet_ntop(AF_INET, &(raddr.sin_addr),
				ipcliente, 512);

		printf("conexao de %s %d\n", ipcliente,
				(int)ntohs(raddr.sin_port));

		size_t c = recv(r, nome_arquivo, 512, 0);
		printf("recebemos %d bytes\n", (int)c);
		puts(nome_arquivo);

		// Abrir o arquivo para leitura
		FILE *fr;
		fr =  fopen(nome_arquivo, "r");
		if (fr == NULL ) {
            printf("Erro ao abrir arquivo");
            return;
		}
		int tam = 0;
		char verificador;
        while(1) {
            fread(buf, sizeof(char), tam_buffer, fr);
            printf("O conteudo que o Server leu foi %s \n", buf);
            send(r, buf, strlen(buf)-1, 0);
            printf("enviou %s \n", buf);
            tam = strlen(buf);
            printf("buf tamanho %d Verificador %c \n", tam, buf[tam-2]);
            verificador = buf[tam-2];
            printf("Condicional do verificador %c \n", verificador);
            if (verificador == '0') {
                break;
            }
            //if (feof(fr)) break;
            memset(buf, 0, tam_buffer);
        }
        fclose(fr);
		printf("Acabou envio \n");

		close(r);
	}

	exit(EXIT_SUCCESS);


	return 0;
}
