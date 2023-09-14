"""
    brian:51.xJagtPnb6s --> TF
    zamyla:50cI2vYkF0YU2 --> LOL
"""

from passlib.hash import des_crypt
from sys import argv, exit


def main():
    # Check the number of command line arguments
    if len(argv) != 2:
        print("Usage: python crack.py hash")
        exit(1)

    # Remember the hash value
    hash_value = argv[1]

    # Define the string of possible characters for the password
    letters = " abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

    # Generate possible passwords and check for hash match
    for char5 in letters:
        for char4 in letters:
            for char3 in letters:
                for char2 in letters:
                    for char1 in letters:
                        # Create a possible password
                        password = f"{char5}{char4}{char3}{char2}{char1}".strip()

                        # Skip iteration if the password is empty
                        if password == "":
                            continue

                        # Check if the password matches the hash
                        if des_crypt.verify(password, hash_value):
                            print(password)
                            exit(0)

    print("Failed to crack the password")
    exit(1)


main()
