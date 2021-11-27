from progressbar import ProgressBar
from os import urandom

def main():
    __HEADER_BYTES__ = 54

    fd1 = open("cp-logo.bmp", 'rb')
    fd2 = open("mustang.bmp", 'rb')

    bmp_header = fd1.read(__HEADER_BYTES__)
    fd2.read(__HEADER_BYTES__)

    logo_bytes = fd1.read()
    mustang_bytes = fd2.read()

    key_bytes = urandom(len(logo_bytes))

    ciphertext_logo = xor_bytes(logo_bytes, key_bytes)
    ciphertext_mustang = xor_bytes(mustang_bytes, key_bytes)

    # write encrypted image logo
    with open("cp-logo-2tp.bmp", 'wb') as fd3:
        fd3.write(bmp_header)
        fd3.write(ciphertext_logo)

    # write encrypted image mustang
    with open("mustang-2tp.bmp", 'wb') as fd3:
        fd3.write(bmp_header)
        fd3.write(ciphertext_mustang)

    # write XOR ciphertexts to a file
    with open("xor.bmp", 'wb') as fd3:
        decrypted_bytes = xor_bytes(ciphertext_logo, ciphertext_mustang)
        fd3.write(bmp_header)
        fd3.write(decrypted_bytes)

    fd2.close()
    fd1.close()


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
