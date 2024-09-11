#include <stdio.h>
#include <stdlib.h>
#include <errno.h>
#include <inttypes.h>
#include <string.h>

void filtro(uint8_t* matriz_entrada, int rows, int cols, uint8_t* matriz_salida){
    // implementar el filtro como corresponde 
    // esto es solo dummy 
    memcpy(matriz_salida, matriz_entrada, rows*cols);
}


int main(int argc, char** argv){
    if(argc < 3){
        fprintf(stderr, "No se tienen suficientes parámetros");
        return 1;
    }
    FILE *input = fopen(argv[1], "r");
    if(input == NULL){
        return 2;
    }
    FILE *output = fopen(argv[2], "w"); 
    if(output == NULL){
        return 2;
    }
    int rows;
    int cols;
    if(fscanf(input, "%d\n", &rows)==EOF) return 3;
    if(fscanf(input, "%d\n", &cols) ==EOF) return 3;
    int pixel_count = rows*cols;
    uint8_t* src_image = (uint8_t*) malloc(pixel_count*sizeof(uint8_t));
    uint8_t* out_image = (uint8_t*) malloc(pixel_count*sizeof(uint8_t));
    if(src_image == NULL) return 3;
    int i = 0;
    int pixel;
    
    while(fscanf(input, "%d\n", &pixel)!=EOF){
        src_image[i] = pixel;
        ++i;
    }
    
    filtro(src_image, rows, cols, out_image);
    
    fprintf(output, "%d\n%d\n", rows, cols);
    for(int i=0; i < pixel_count; i++){
        fprintf(output, "%d\n", *(out_image+i));
    }


}
