from base64 import b64encode
from sys import argv
from os import urandom

def main():
    with open(argv[1], 'r') as fd1:
        plaintext = fd1.read()

        key_bytes = urandom(len(plaintext))
        key_str = b64encode(key_bytes).decode('UTF-8')
        key_str = key_str[0:len(plaintext)]
        key_hex = convert_to_hex(key_str)

        print(f"Key: {len(key_str)}, Plaintext: {len(plaintext)}")
        print(f"Key: {key_str}")

        ciphertext = xor_strings(plaintext, key_str)
        print(f"Ciphertext: {ciphertext}")

        decrypted_hex_text = xor_strings(ciphertext, key_hex)
        print(f"Plaintext: {decrypted_hex_text}")

def convert_to_hex(string: str) -> str:
    hex_str = ""
    for c in range(len(string)):
        hex_str = hex_str + format(ord(string[c]), '02x')
    return hex_str

def convert_from_hex(hex_str: str) -> str:
    string = ""
    for c in range(len(hex_str), 2):
        small_hex = hex_str[c] + hex_str[c+1]
        string = string + chr(hex_str[c]) + chr(hex_str[c+1])

    return string

def xor_strings(string1: str, string2: str) -> str:
    if len(string1) != len(string2):
        raise ValueError("Strings are not the same length")

    xor = ""
    for c in range(len(string1)):
        temp = ord(string1[c]) ^ ord(string2[c])
        xor = xor + format(temp, '02x')

    return xor

if __name__ == "__main__":
    main()
