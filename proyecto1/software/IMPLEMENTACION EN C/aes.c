#include <wmmintrin.h> //Para poder usar AES-NI y SIMD
#include <stdio.h>
#include <string.h>

//Encriptacion con SIMD
void aes_encrypt_vectorial(const unsigned char* key, const unsigned char* in, unsigned char* out) {
    __m128i key_schedule = _mm_loadu_si128((const __m128i*)key);
    __m128i data = _mm_loadu_si128((const __m128i*)in);
    data = _mm_xor_si128(data, key_schedule); 

    for (int i = 0; i < 10; i++) {
        data = _mm_aesenc_si128(data, key_schedule);
    }
    data = _mm_aesenclast_si128(data, key_schedule); 

    _mm_storeu_si128((__m128i*)out, data);
}


//Desencriptacion con SIMD
void aes_decrypt_vectorial(const unsigned char* key, const unsigned char* in, unsigned char* out) {
    __m128i key_schedule = _mm_loadu_si128((const __m128i*)key);
    __m128i data = _mm_loadu_si128((const __m128i*)in);
    data = _mm_xor_si128(data, key_schedule); 

    for (int i = 0; i < 10; i++) {
        data = _mm_aesdec_si128(data, key_schedule);
    }
    data = _mm_aesdeclast_si128(data, key_schedule);

    _mm_storeu_si128((__m128i*)out, data);
}



/*
 GENTE PARA QUE PUEDAN CORRER EL CODIGO SI O SI LO TIENEN QUE COMPILAR ASI:

 """""""""""""""""""""""""""""""
 gcc -maes -msse4.1 aes.c -o aes
 """""""""""""""""""""""""""""""

tienen que usar el -maes y el -msse4.1 por que si no, el programa no corre
luego lo corren con ./aes

*/


int main() {
    
    // Estos de aca son solo datos de prueba
    unsigned char key[16] = { 0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07,
                              0x08, 0x09, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x0F };
    unsigned char data[16] = { 0x32, 0x43, 0xF6, 0xA8, 0x88, 0x5A, 0x30, 0x8D,
                               0x31, 0x31, 0x98, 0xA2, 0xE0, 0x37, 0x07, 0x34 };
    unsigned char result[16];
    int option;


    printf("Seleccione una opción:\n");
    printf("1. Cifrar\n");
    printf("2. Descifrar\n");
    scanf("%d", &option);

    if (option == 1) {
        aes_encrypt_vectorial(key, data, result);
        printf("Datos cifrados: ");
    } else if (option == 2) {
        aes_decrypt_vectorial(key, data, result);
        printf("Datos descifrados: ");
    } else {
        printf("Opción inválida\n");
        return 1;
    }

    for (int i = 0; i < 16; i++) { //hexa
        printf("%02x ", result[i]);
    }
    printf("\n");

    return 0;
}
