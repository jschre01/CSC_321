def main():
    string1 = input("Enter a string: ")
    string2 = input("Enter another string of the same length: ")
    xor = xor_strings(string1, string2)
    print(f"Encrypted string hex: {xor}")

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
