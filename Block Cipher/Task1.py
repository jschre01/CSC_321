from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import sys

def main():
    in_file = sys.argv[0]
    f = open(in_file, 'r')
    text = pad(f, 16)
    ecb_key = #generate random key of ecb size
    cbc_key = #generate random key of cbc size
    cbc_iv = #generate random iv of iv size

    f_ecb = open("ecb_encrypt.txt", "w")
    f_cbc = open("cbc_encrypt.txt", "w")
    ecb_cipher = AES.new(ecb_key, AES.MODE_ECB)
    ##NEED TO PAD f BEFORE DOING THIS vvv Can use Crypto.Util.Padding
    ecb_ct = ecb_cipher.encrypt(text)
    cbc_cipher = AES.new(cbc_key, AES.MODE_CBC, cbc_iv)
    cbc_ct = cbc_cipher.encrypt(text)

    f_ecb.write(ecb_ct)
    f_cbc.write(cbc_ct)

    f.close()
    f_ecb.close()
    f_cbc.close()

def generate_key(num_bytes:int) -> bytes:
    return get_random_bytes(num_bytes)

def ecb_encrypt():




if __name__ == "__main__":
    main()
