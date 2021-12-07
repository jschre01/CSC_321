from bcrypt import hashpw
from nltk.corpus import words
from progressbar import ProgressBar

def main():
    wordlist = get_wordlist()
    user_list = []
    hash_list = []

    with open("shadow.txt", "r") as shadow:
        line = shadow.readline().strip()
        while line != "":
            temp = line.split(":")
            user_list.append(temp[0])
            hash_list.append(temp[1])

            line = shadow.readline().strip()

    passwords = crack_passwords(hash_list, wordlist)

def crack_passwords(hash_list: list, wordlist:list) -> dict:
    password_dict = {}
    for hash in hash_list:
        password_dict[hash] = None
    
    for hash_str in hash_list:
        hash = hash_str.encode()
        salt_str = hash_str[:29]
        salt = salt_str.encode()
        shared_salts = []
        for h in hash_list:
            if salt_str in h:
                shared_salts.append(h)

        if (password_dict[hash_str] is None):
            pbar = ProgressBar()
            print(f"Cracking shared salts: {shared_salts}")
            for word in pbar(wordlist):
                new_hash = hashpw(word.encode(), salt)
                if (new_hash.decode() in shared_salts):
                    password_dict[new_hash.decode()] = word
                    shared_salts.remove(new_hash.decode())
                    print(f"\n\nHash broken: {{{new_hash.decode()}}} : {{{password_dict[new_hash.decode()]}}}")
                    print(f"Shared salts remaining: {shared_salts}\n")
                if (len(shared_salts) == 0):
                    break

    return password_dict

def get_wordlist() -> list:
    wordlist_full = words.words()
    wordlist = [ n for n in wordlist_full if len(n) >= 6 and len(n) <= 10]
    wordlist.sort(key=len, reverse=False)
    return wordlist

if __name__ == "__main__":
    main()