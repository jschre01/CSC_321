from itertools import permutations
from hashlib import sha256
from time import time

def main():
    # Print menu for task
    print("Menu")
    print("a.) Hash arbitrary inputs")
    print("b.) Hash 2 arbitrary inputs whose Hamming Distance is 1 bit")
    print("c.) Hash collisions with 8-50 bits")
    option = input("Enter a choice: ")

    # Execute menu choice
    if (option == 'a'):
        plaintext = input("Enter plaintext to be hashed using SHA256: ")
        sha256hex = create_sha256_hash(plaintext)
        print(sha256hex)
    elif (option == 'b'):
        plaintext1 = input("Enter plaintext to be hashed using SHA256: ")
        plaintext2 = input("Enter plaintext to be hashed using SHA256: ")
        sha256hex1 = create_sha256_hash(plaintext1)
        sha256hex2 = create_sha256_hash(plaintext2)
        print(sha256hex1)
        print(sha256hex2)
    elif (option == 'c'): 
        for i in range(8, 51):
            generate_collisions(i)

# Returns hex string SHA256 hash
def create_sha256_hash(plaintext: str) -> str:
    hash = sha256(plaintext.encode('utf-8')).hexdigest()
    return hash

# Returns the bitwise representation of SHA256 hash of specified length
def create_sha256_bits(plaintext: str, length: int) -> str:
    hash = create_sha256_hash(plaintext)
    bits = bin(int(hash, base=16)).lstrip('0b')
    return bits[:length]

# Generates a list of characters to use for collision generation
def get_list_of_chars():
    list = []
    for i in range(48, 145):
        list.append(chr(i))
    return list

# Generates collisions for hashes of specific length
def generate_collisions(bit_len: int):
    start_time = time()
    input_count = 0
    # Get a list of legal characters ascii codes 1-255
    legal_chars = get_list_of_chars()

    # Key: raw bits of hash, Value: plaintext string
    htable = {}

    # For strings of length 0 to 8
    for str_len in range(1, 5):

        # Get all permutations of legal characters of length str_length
        perms = list(permutations(legal_chars, r=str_len))

        # For each permutation generated...
        # Merge the tuple into a string
        # Hash the string and get raw bits
        for tup in perms:
            plaintext = ''.join(tup)
            hash_bits = create_sha256_bits(plaintext, bit_len)
            input_count += 1

            # If raw bits exist as a key, we have a collision
            if hash_bits in htable:
                delta = time() - start_time
                print(f"COLLISION at {bit_len} bits: {{{hash_bits:50}}} : "
                f"{{{plaintext.encode('utf-8').hex():10}}} and {{{htable[hash_bits].encode('utf-8').hex():10}}} "
                f"in {delta:7.4f} seconds with {input_count} inputs")
                return
            else:
                htable[hash_bits] = plaintext

if __name__ == "__main__":
    main()
