from base64 import b64encode
from sys import argv
from os import urandom

def main():

    if len(argv) != 4:
        print("Usage: task2.py <input file> <output ciphertext file> <output plaintext file>")
        exit(1)

    with open(argv[1], 'r') as fd1:
        plaintext = fd1.read()

        # Generate random key in correct format
        key_bytes = urandom(len(plaintext))
        key_str = b64encode(key_bytes).decode('UTF-8')
        key_str = key_str[0:len(plaintext)]

        # Generate ciphertext and write to file
        ciphertext_hex = xor_strings(plaintext, key_str)
        ciphertext_string = convert_from_hex(ciphertext_hex)
        with open(argv[2], 'w') as fd2:
            fd2.write(ciphertext_string)

        # Decrypt ciphertext and write plaintext to file
        decrypted_hex_text = xor_strings(ciphertext_string, key_str)
        decrypted_string_text = convert_from_hex(decrypted_hex_text)
        with open(argv[3], 'w') as fd2:
            fd2.write(decrypted_string_text)

# Converts character string to hex string
def convert_to_hex(string: str) -> str:
    hex_str = ""
    for c in range(len(string)):
        hex_str = hex_str + format(ord(string[c]), '02x')
    return hex_str

# Converts hex string to character string
def convert_from_hex(hex_str: str) -> str:
    bytes_array = bytes.fromhex(hex_str)
    ascii_str = bytes_array.decode()

    return ascii_str

# Takes in 2 strings in character format -> returns hex string of XOR
def xor_strings(string1: str, string2: str) -> str:
    if len(string1) != len(string2):
        raise ValueError(f"Strings are not the same length: {len(string1)} and {len(string2)}")

    xor = ""
    for c in range(len(string1)):
        temp = ord(string1[c]) ^ ord(string2[c])
        xor = xor + format(temp, '02x')

    return xor

if __name__ == "__main__":
    main()
