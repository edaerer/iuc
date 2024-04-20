import os
from hashlib import sha256, md5, sha1

def sort_passwords():
    upass_directory = "../Unprocessed-Passwords/"
    ppass_directory = "../Processed/"
    index_directory = "../Index/"
    for filename in os.listdir(upass_directory):
        if os.path.isfile(os.path.join(upass_directory, filename)):
            with open(os.path.join(upass_directory, filename), "r", encoding='utf-8') as upfiles:
                for line in upfiles.readlines():
                    password = line.rstrip("\n")
                    name = password[0]
                    if not os.path.exists(index_directory + f"{line[0]}"):
                        try:
                            os.makedirs(index_directory + f"{line[0]}")
                        except OSError:
                            if not os.path.exists(index_directory + "wildcards"):
                                os.makedirs(index_directory + "wildcards")
                            name = "wildcards"
                    with open(f"{index_directory}{name}/0.txt", "a", encoding='utf-8') as indexfile:
                        md5_hash = md5(line.encode()).hexdigest()
                        sha128_hash = sha1(line.encode()).hexdigest()
                        sha256_hash = sha256(line.encode()).hexdigest()
                        indexfile.write(f"{password}|{md5_hash}|{sha128_hash}|{sha256_hash}|{filename}\n")
        # os.rename(os.path.join(upass_directory, filename), os.path.join(ppass_directory, filename))

if __name__ == "__main__":
    sort_passwords()