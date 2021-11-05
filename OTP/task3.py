from progressbar import ProgressBar
from base64 import b64encode
from sys import argv
from os import urandom

def main():
    __HEADER_BYTES__ = 54
    if len(argv) != 4:
        print("Usage: task2.py <input image> <output image ciphertext> <output image plaintext>")
        exit(1)

    with open(argv[1], 'rb') as fd1:
        bmp_header = fd1.read(__HEADER_BYTES__)
        bmp_bytes = fd1.read()

        key_bytes = urandom(len(bmp_bytes))

        ciphertext = xor_bytes(bmp_bytes, key_bytes)

        # write encrypted image
        with open(argv[2], 'wb') as fd2:
            fd2.write(bmp_header)
            fd2.write(ciphertext)

        # write decrypted image
        with open(argv[3], 'wb') as fd3:
            decrypted_bytes = xor_bytes(ciphertext, key_bytes)
            fd3.write(bmp_header)
            fd3.write(decrypted_bytes)

def xor_bytes(byte_string1: bytes, byte_string2: bytes) -> bytes:
    if len(byte_string1) != len(byte_string2):
        raise ValueError(f"bytes are not the same length: {len(byte_string1)} and {len(byte_string2)}")

    xor = b''
    pbar = ProgressBar()
    for c in pbar(range(len(byte_string1))):
        xor += (byte_string1[c] ^ byte_string2[c]).to_bytes(1, 'big')

    return xor


if __name__ == "__main__":
    main()
