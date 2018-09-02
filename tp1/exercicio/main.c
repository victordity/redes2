#include <stdio.h>
#include <stdlib.h>
#include <string.h>


int main()
{
    int tam_buffer = 10;
    char buf[tam_buffer];;
    FILE *fr;
    fr =  fopen("arquivo.txt", "r");
    if (fr == NULL ) {
        printf("Erro ao abrir arquivo");
        return;
    }
    while(1) {

        fread(buf, sizeof(char), tam_buffer, fr);
        printf("O conteudo que o Server leu foi %s \n", buf);
        printf("enviou %s \n", buf);
        if (feof(fr)) break;
        memset(buf, 0, tam_buffer);
        //for (int i = 0; i < tam_buffer; i++) {
         //   buf[i] = NULL;
        //}
    }

    return 0;
}
