#include <stdio.h>
#include <stdlib.h>
#include <errno.h>
#include <inttypes.h>
#include <string.h>
#include <math.h>

#define WIDTH  256 // Ancho de la imagen
#define HEIGHT 256  // Alto de la imagen

// Sobel kernels para direccion X y Y
int sobel_x[3][3] = {
    {-1, 0, 1},
    {-2, 0, 2},
    {-1, 0, 1}
};

int sobel_y[3][3] = {
    {-1, -2, -1},
    { 0,  0,  0},
    { 1,  2,  1}
};

// Aplicar el filtro Sobel a un solo canal 
void filterChannel(int16_t* input, int rows, int cols, int16_t* output) {
    int gx, gy;

    for (int i = 1; i < rows - 1; i++) {
        for (int j = 1; j < cols - 1; j++) {
            gx = 0;
            gy = 0;

            for (int x = -1; x <= 1; x++) {
                for (int y = -1; y <= 1; y++) {
                    int input_index = ((i + x) * cols + (j + y));  
                    gx += input[input_index] * sobel_x[x + 1][y + 1];
                    gy += input[input_index] * sobel_y[x + 1][y + 1];
                }
            }

            int magnitude = (int)sqrt(gx * gx + gy * gy);

            if (magnitude > 255) {
                magnitude = 255;
            }
            
            output[i * cols + j] = (int16_t)magnitude;  
        }
    }
}


// Filtro serial edge detection aplicado a cada canal (RGB)
void edgeDetectionSerial(int16_t* matriz_entrada, int rows, int cols, int16_t* matriz_salida) {
    //Canales de entrada (originales)
    int16_t* red = (int16_t*) malloc(rows * cols * sizeof(int16_t));
    int16_t* green = (int16_t*) malloc(rows * cols * sizeof(int16_t));
    int16_t* blue = (int16_t*) malloc(rows * cols * sizeof(int16_t));

    //Canales de salida (filtrados)
    int16_t* red_edges = (int16_t*) malloc(rows * cols * sizeof(int16_t));
    int16_t* green_edges = (int16_t*) malloc(rows * cols * sizeof(int16_t));
    int16_t* blue_edges = (int16_t*) malloc(rows * cols * sizeof(int16_t));

    // Extraer canales R, G, B de la matriz de entrada
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < cols; j++) {
            int index = (i * cols + j) * 3;
            red[i * cols + j] = matriz_entrada[index];
            green[i * cols + j] = matriz_entrada[index + 1];
            blue[i * cols + j] = matriz_entrada[index + 2];
        }
    }

    // Aplicar el filtro Sobel en cada canal -> filterChannel
    filterChannel(red, rows, cols, red_edges);
    filterChannel(green, rows, cols, green_edges);
    filterChannel(blue, rows, cols, blue_edges);

    // Guardar los resultados en la matriz de salida
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < cols; j++) {
            int index = (i * cols + j) * 3;
            matriz_salida[index] = red_edges[i * cols + j];
            matriz_salida[index + 1] = green_edges[i * cols + j];
            matriz_salida[index + 2] = blue_edges[i * cols + j];
        }
    }

    free(red);
    free(green);
    free(blue);
    free(red_edges);
    free(green_edges);
    free(blue_edges);
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
    
    int pixel_count = rows * cols * 3;  // Multiplicamos por 3 para R, G, B
    int16_t* src_image = (int16_t*) malloc(pixel_count * sizeof(int16_t));
    int16_t* out_image = (int16_t*) malloc(pixel_count * sizeof(int16_t));
    if(src_image == NULL || out_image == NULL) return 3;
    
    int i = 0;
    int pixel;
    
    while(fscanf(input, "%d\n", &pixel) != EOF){
        src_image[i] = pixel;
        ++i;
    }
    
    edgeDetectionSerial(src_image, rows, cols, out_image);
    
    fprintf(output, "%d\n%d\n", rows, cols);
    for(int i = 0; i < pixel_count; i++){
        fprintf(output, "%d\n", out_image[i]);
    }

    free(src_image);
    free(out_image);
    fclose(input);
    fclose(output);

    return 0;
}
