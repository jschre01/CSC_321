from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES

def main():
    key = generate_key(16)
    iv = generate_key(8)
    string = input("Enter a string to submit: ")
    encrypted = submit(string, key, iv)
    print(encrypted)
    string = input("Enter a string to verify: ")
    result = verify(string, key, iv)
    print(result)


def submit(string, key, iv):
    pre = "userid=456;userdata="
    post = ";session-id=31337"
    user_str = ""
    for i in string:
        if i == "=":
            user_str += "%3D"
        elif i == ";":
            user_str += "%3B"
        else:
            user_str += i
    new_string = pre + user_str + post
    padded_string = pkcs(bytearray(new_string.encode('utf-8')))
    return cbc_encrypt(padded_string, key, iv)

def verify(string, key, iv):
    byte_string = bytearray(string.encode('latin'))
    text = cbc_decrypt(byte_string, key, iv)
    print(text)
    if "admin=true" in text:
        return True
    else:
        return False



def cbc_decrypt(text, key, iv):
    decrypt = AES.new(key, AES.MODE_CBC, iv)
    string = ""
    for i in range(0, len(text), 16):
        pt = (int.from_bytes(decrypt.decrypt(int.from_bytes(text[i:i+16], "big")), "big") ^ int.from_bytes(iv, "big"))
        print(type(pt))
        iv = text[i:i+16]
    return string


def cbc_encrypt(text, key, iv):
    encrypt = AES.new(key, AES.MODE_ECB)
    string = ""
    for i in range(0, len(text), 16):
        iv = encrypt.encrypt((int.from_bytes(bytes(text[i:i+16]), "big") ^ int.from_bytes(iv, "big")).to_bytes(16, "big"))
        string += iv.decode('latin')
    return string


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


if __name__ == "__main__":
    main()
