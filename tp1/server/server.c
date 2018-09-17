#include <stdlib.h>
#include <unistd.h>
#include <stdio.h>
#include <string.h>
#include <pthread.h>
#include <sys/time.h>

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

	int pid;
    struct timeval tv1, tv2;
    double t1, t2;

    // Processa argumentos da linha de comando
	porto_do_servidor = atoi(argv[1]);
	tam_buffer = atoi(argv[2]);
    // ./client 127.434.33 5000 arquivo 10
    // Faz abertura passiva e aguarda conexão
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

    // Recebe a String com nome do arquivo
    size_t c = recv(r, nome_arquivo, 512, 0);
    puts(nome_arquivo);

    // Abrir o arquivo para leitura
    FILE *fr;
    fr =  fopen(nome_arquivo, "r");

    // Se deu erro fecha a conexao e termina
    if (fr == NULL ) {
        printf("Erro ao abrir arquivo \n");
        return 0;
    }
    int tam = 0;
    char verificador;

    gettimeofday(&tv1, NULL);
    t1 = (double)(tv1.tv_sec) + (double)(tv1.tv_usec)/ 1000000.00;
    // Le o arquivo 1 buffer de cada vez
    while(1) {

        fread(buf, sizeof(char), tam_buffer, fr);
        send(r, buf, strlen(buf)-1, 0);
        tam = strlen(buf);
        verificador = buf[tam-2];
        if (verificador == '0') {
            break;
        }
        memset(buf, 0, tam_buffer);

    }

    gettimeofday(&tv2, NULL);
    t2 = (double)(tv2.tv_sec) + (double)(tv2.tv_usec)/ 1000000.00;
    printf("\nO tempo de execucao de foi: %lf\n",(t2 - t1));
    fclose(fr);
    close(r);

}
    // Fecha a conexao e o arquivo
	exit(EXIT_SUCCESS);


	return 0;
}
