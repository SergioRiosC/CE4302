#include <stdio.h>
#include <stdint.h>
#include <string.h>


static const uint8_t sbox[256] = {
    0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, 0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76,

};

static const uint8_t inv_sbox[256] = {
    0x52, 0x09, 0x6A, 0xD5, 0x30, 0x36, 0xA5, 0x38, 0xBF, 0x40, 0xA3, 0x9E, 0x81, 0xF3, 0xD7, 0xFB,
};

void sub_bytes(uint8_t* state) { // Función SubBytes
    for (int i = 0; i < 16; i++) {
        state[i] = sbox[state[i]];
    }
}

void inv_sub_bytes(uint8_t* state) { // Función SubBytes inversa 
    for (int i = 0; i < 16; i++) {
        state[i] = inv_sbox[state[i]];
    }
}


void shift_rows(uint8_t* state) {
    uint8_t temp;

    temp = state[1]; // Fila 2 -> rotar 1 byte a la izquierda
    state[1] = state[5];
    state[5] = state[9];
    state[9] = state[13];
    state[13] = temp;


    temp = state[2]; // Fila 3 -> rotar 2 bytes a la izquierda
    state[2] = state[10];
    state[10] = temp;
    temp = state[6];
    state[6] = state[14];
    state[14] = temp;


    temp = state[3]; // Fila 4 -> rotar 3 bytes a la izquierda
    state[3] = state[15];
    state[15] = state[11];
    state[11] = state[7];
    state[7] = temp;
}


void inv_shift_rows(uint8_t* state) {
    uint8_t temp;

    temp = state[13]; // Fila 2 -> rotar 1 byte a la derecha
    state[13] = state[9];
    state[9] = state[5];
    state[5] = state[1];
    state[1] = temp;


    temp = state[2]; // Fila 3 -> rotar 2 bytes a la derecha
    state[2] = state[10];
    state[10] = temp;
    temp = state[6];
    state[6] = state[14];
    state[14] = temp;


    temp = state[7]; // Fila 4 -> rotar 3 bytes a la derecha
    state[7] = state[11];
    state[11] = state[15];
    state[15] = state[3];
    state[3] = temp;
}

void add_round_key(uint8_t* state, const uint8_t* round_key) { // Añadir clave de ronda
    for (int i = 0; i < 16; i++) {
        state[i] ^= round_key[i];
    }
}

void aes_encrypt_basic(const uint8_t* key, const uint8_t* in, uint8_t* out) { // Encriptación AES
    uint8_t state[16];

    memcpy(state, in, 16);
    add_round_key(state, key);
    sub_bytes(state);
    shift_rows(state);
    add_round_key(state, key);
    memcpy(out, state, 16);
}


void aes_decrypt_basic(const uint8_t* key, const uint8_t* in, uint8_t* out) { // Desencriptación AES 
    uint8_t state[16];

    memcpy(state, in, 16);
    add_round_key(state, key);
    inv_shift_rows(state);
    inv_sub_bytes(state);
    add_round_key(state, key);
    memcpy(out, state, 16);
}

int main() {
    uint8_t key[16] = { 0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07,
                        0x08, 0x09, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x0F };
    uint8_t data[16] = { 0x32, 0x43, 0xF6, 0xA8, 0x88, 0x5A, 0x30, 0x8D,
                         0x31, 0x31, 0x98, 0xA2, 0xE0, 0x37, 0x07, 0x34 };
    uint8_t encrypted[16];
    uint8_t decrypted[16];


    printf("Datos originales: "); // Imprimir datos originales
    for (int i = 0; i < 16; i++) {
        printf("%02x ", data[i]);
    }
    printf("\n");

  



    aes_encrypt_basic(key, data, encrypted); // Encriptar
    printf("Datos cifrados: ");
    for (int i = 0; i < 16; i++) {
        printf("%02x ", encrypted[i]);
    }
    printf("\n");


    aes_decrypt_basic(key, encrypted, decrypted); // Desencriptar
    printf("Datos descifrados: ");
    for (int i = 0; i < 16; i++) {
        printf("%02x ", decrypted[i]);
    }
    printf("\n");

    return 0;
}