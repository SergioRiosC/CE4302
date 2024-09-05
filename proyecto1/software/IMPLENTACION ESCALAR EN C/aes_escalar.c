#include <openssl/evp.h>
#include <string.h>
#include <stdio.h>

//DEBEN INSTALAR EL openssl


//Encriptacion
void aes_encrypt_escalar(const unsigned char* key, const unsigned char* in, unsigned char* out) {
    EVP_CIPHER_CTX* ctx = EVP_CIPHER_CTX_new();
    int len;

    EVP_EncryptInit_ex(ctx, EVP_aes_128_ecb(), NULL, key, NULL);
    EVP_EncryptUpdate(ctx, out, &len, in, 16);
    EVP_EncryptFinal_ex(ctx, out + len, &len);
    EVP_CIPHER_CTX_free(ctx);
}

//Desencriptacion
void aes_decrypt_escalar(const unsigned char* key, const unsigned char* in, unsigned char* out) {
    EVP_CIPHER_CTX* ctx = EVP_CIPHER_CTX_new();
    int len;

    EVP_DecryptInit_ex(ctx, EVP_aes_128_ecb(), NULL, key, NULL);
    EVP_DecryptUpdate(ctx, out, &len, in, 16);
    EVP_DecryptFinal_ex(ctx, out + len, &len);
    EVP_CIPHER_CTX_free(ctx);
}

int main() {
    unsigned char key[16] = { 0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07,
                              0x08, 0x09, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x0F };
    unsigned char data[16] = { 0x32, 0x43, 0xF6, 0xA8, 0x88, 0x5A, 0x30, 0x8D,
                               0x31, 0x31, 0x98, 0xA2, 0xE0, 0x37, 0x07, 0x34 };
    unsigned char encrypted[16];
    unsigned char decrypted[16];

    int option;
    printf("Seleccione una opción:\n");
    printf("1. Cifrar\n");
    printf("2. Descifrar\n");
    scanf("%d", &option);

    if (option == 1) {
        aes_encrypt_escalar(key, data, encrypted);
        printf("Datos cifrados: ");
        for (int i = 0; i < 16; i++) {
            printf("%02x ", encrypted[i]);
        }
        printf("\n");
    } else if (option == 2) {
        aes_decrypt_escalar(key, encrypted, decrypted);
        printf("Datos descifrados: ");
        for (int i = 0; i < 16; i++) {
            printf("%02x ", decrypted[i]);
        }
        printf("\n");
    } else {
        printf("Opción inválida\n");
        return 1;
    }

    return 0;
}