from os import path, listdir, makedirs, rename
from hashlib import sha256, md5, sha1
from collections import defaultdict
from random import choices
from string import ascii_letters, digits
from time import time

UPASS_DIRECTORY = "../Unprocessed-Passwords/"
PPASS_DIRECTORY = "../Processed/"
INDEX_DIRECTORY = "../Index/"
pass_count_dict = defaultdict(int)

def search_password(password):
    found = False
    search_directory = f"../Index/{password[0]}/"
    try:
        for filename in listdir(search_directory):
            if path.isfile(path.join(search_directory, filename)):
                with open((search_directory + filename), "r") as file:
                    for line in file:
                        if line.split("|")[0] == password:
                            return line
    except FileNotFoundError:
        pass
    return found

def add_password(pw, source_file="search"):
    sub_index = pw[0]
    pass_count_dict[sub_index] += 1
    if not path.exists(INDEX_DIRECTORY + sub_index):
        try:
            makedirs(INDEX_DIRECTORY + sub_index)
        except OSError:
            sub_index = "wildcards"
            if not path.exists(INDEX_DIRECTORY + sub_index):
                makedirs(INDEX_DIRECTORY + sub_index)
    with open(f"{INDEX_DIRECTORY}{sub_index}/{pass_count_dict[sub_index] // 10000}.txt", "a", encoding='utf-8') as sub_index_file:
        sub_index_file.write(f"{pw}|{md5(pw.encode()).hexdigest()}|{sha1(pw.encode()).hexdigest()}|{sha256(pw.encode()).hexdigest()}|{source_file}\n")

def sort_passwords():
    for upass_file in listdir(UPASS_DIRECTORY):
        if path.isfile(path.join(UPASS_DIRECTORY, upass_file)):
            with open(path.join(UPASS_DIRECTORY, upass_file), "r", encoding='utf-8') as file:
                for line in file.readlines():
                    if search_password(line.rstrip("\n")) == False:
                        add_password(line.rstrip("\n"), upass_file)
        rename(path.join(UPASS_DIRECTORY, upass_file), path.join(PPASS_DIRECTORY, upass_file))

if __name__ == "__main__":
    option = input("[1] Create Index\n[2] Search Password\n[3] Calculate Performance\n[4] Quit\nChoice: ")
    match option:
        case "1":
            sort_passwords()
            print("Passwords successfully sorted.")
        case "2":
            password = input("Password to search for: ")
            output = search_password(password)
            if output == False:
                add_password(password)
                print(f"Password '{password}' not found and added.")
            else:
                print(output)
        case "3":
            random_passwords = ["".join(choices(ascii_letters + digits, k=15)) for _ in range(10)]
            start = time()
            for _ in range(10):
                search_password(random_passwords[_])
            end = time()
            print(f"Total time passed searching for 10 random passwords: {end - start}")
        case "4" | _:
            print("Thank you for choosing us. See you next time!")