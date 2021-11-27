from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import sys

def main():
    in_file = sys.argv[0]
    bmp_header = None
    if '.bmp' in in_file:
        f = open(in_file, 'rb')
        bmp_header = f.read(54)
    else:
        f = open(in_file, 'r')

    plaintext = f.read()

    
    text = pad(bytearray(plaintext), 8)

    file_ecb = open("ecb_encrypt.txt", "w")
    file_cbc = open("cbc_encrypt.txt", "w")

    ecb_encrypt(text, file_ecb, bmp_header)
    cbc_encrypt(text, file_cbc, bmp_header)

    #encrypt = AES.new(ecb_key, AES.MODE_ECB)
    ##NEED TO PAD f BEFORE DOING THIS vvv Can use Crypto.Util.Padding
    #ecb_ct = ecb_cipher.encrypt(text)
    #cbc_cipher = AES.new(cbc_key, AES.MODE_CBC, cbc_iv)
    #cbc_ct = cbc_cipher.encrypt(text)

    #f_ecb.write(ecb_ct)
    #f_cbc.write(cbc_ct)

    f.close()
    file_ecb.close()
    file_cbc.close()

def generate_key(num_bytes:int) -> bytes:
    return get_random_bytes(num_bytes)

def cbc_encrypt(text, outfile, bmp_header):
    if bmp_header != None:
        outfile.write(bmp_header)
    cbc_key = generate_key(16)
    iv = generate_key(8)
    encrypt = AES.new(cbc_key, AES.MODE_ECB)
    for i in range(len(text), 8):
        iv = encrypt.encrypt(text[i:i+8] ^ iv)
        outfile.write(iv)

def ecb_encrypt(text, outfile, bmp_header):
    if bmp_header != None:
        outfile.write(bmp_header)
    ecb_key = generate_key(16)
    encrypt = AES.new(ecb_key, AES.MODE_ECB)
    for i in range(len(text), 8):
        outfile.write(encrypt.encrypt(text[i:i+8]))
    




if __name__ == "__main__":
    main()
