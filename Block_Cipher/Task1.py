from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import sys

def main():
    in_file = sys.argv[1]
    bmp_header = None
    if '.bmp' in in_file:
        f = open(in_file, 'rb')
        bmp_header = f.read(54)
        file_ecb = open("ecb_encrypt.bmp", "wb")
        file_cbc = open("cbc_encrypt.bmp", "wb")
        plaintext = f.read()
        text = pkcs(plaintext)
        file_ecb.write(bmp_header)
        file_cbc.write(bmp_header)
    else:
        f = open(in_file, 'r')
        file_ecb = open("ecb_encrypt.txt", "wb")
        file_cbc = open("cbc_encrypt.txt", "wb")
        plaintext = f.read()
        text = pkcs(bytearray(plaintext.encode('utf-8')))



    key = generate_key(16)
    iv = generate_key(8)
    ecb_encrypt(text, file_ecb, key)
    cbc_encrypt(text, file_cbc, key, iv)

    f.close()
    file_ecb.close()
    file_cbc.close()

def pkcs(plaintext):
    l = len(plaintext)
    text = plaintext
    remainder = l % 16
    pad = 16 - remainder
    b = pad.to_bytes(1, "big")
    for i in range(pad):
        text += b
    return text

def generate_key(num_bytes:int) -> bytes:
    return get_random_bytes(num_bytes)

def cbc_encrypt(text, outfile, key, iv):
    encrypt = AES.new(key, AES.MODE_ECB)
    for i in range(0, len(text), 16):
        iv = encrypt.encrypt((int.from_bytes(bytes(text[i:i+16]), "big") ^ int.from_bytes(iv, "big")).to_bytes(16, "big"))
        outfile.write(iv)

def ecb_encrypt(text, outfile, key):
    ecb_key = generate_key(16)
    encrypt = AES.new(key, AES.MODE_ECB)
    for i in range(0, len(text), 16):
        outfile.write(encrypt.encrypt(text[i:i+16]))
    




if __name__ == "__main__":
    main()
