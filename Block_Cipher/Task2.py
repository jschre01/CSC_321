from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES

'''User gets to choose any arbitary string to submit. They get back the encrypted version. They can choose to enter 'same', which will automatically decrypt the string that they entered, and check to verify it. They can choose 'flip' which will flip the correct bits in the ciphertext in order to verify the user, but only if the user enters the string ':admin<true'. It will flip the : to ; and the < to = for the user to get past verify. The user can also enter any arbitrary string that they want to verify, which will probably cause an error as they must get the padding scheme correct.'''

def main():
    key = generate_key(16)
    iv = generate_key(16)
    string = input("Enter a string to submit: ")
    encrypted = submit(string, key, iv)
    print(encrypted)
    string = input("Enter a string to verify: ")
    if string == "same":
        result = verify(encrypted, key, iv)
    elif string == "flip":
        flip = '\x00'*4 + '\x01' + '\x00' * 5 + '\x01' + '\x00' *5
        flip = bytearray(flip.encode('utf-8'))
        arg1 = int.from_bytes(bytearray(encrypted.encode('latin'))[:16], "big")
        arg2 =  int.from_bytes(flip, "big")
        new = (arg1 ^ arg2).to_bytes(16, "big").decode('latin')
        encrypted = new + encrypted[16:]
        result = verify(encrypted, key, iv)
    else:
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
    if ";admin=true" in text:
        return True
    else:
        return False

def cbc_decrypt(text, key, iv):
    decrypt = AES.new(key, AES.MODE_ECB)
    pt = ""
    for i in range(0, len(text), 16):
        arg1 = int.from_bytes(decrypt.decrypt(text[i:i+16]), "big")
        arg2 = int.from_bytes(iv, "big")
        pt += (arg1 ^ arg2).to_bytes(16, "big").decode('latin')
        iv = text[i:i+16]
    return pt

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
