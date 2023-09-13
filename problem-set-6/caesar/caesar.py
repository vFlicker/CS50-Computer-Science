from sys import argv, exit

FIRST_UPPERCASE_LETTER_ASCII = 65
FIRST_LOWERCASE_LETTER_ASCII = 97
ALPHABET_LENGTH = 26


def main():
    # Check that the user entered a single argument
    # and the every character in argv[1] is a digit
    if len(argv) != 2 or is_valid_argument(argv[1]) == False:
        print("Usage: python ./caesar key")
        exit(1)

    # Remember key
    key = int(argv[1])

    # Prompt user for plaintext
    plaintext = input("plaintext:  ")

    # Print the output
    print(f"ciphertext: {rotate(plaintext, key)}")

    exit(0)


def is_valid_argument(argument):
    for char in argument:
        if not char.isdigit():
            return False

    return True


def rotate(text, key):
    rotatedText = ""

    for character in text:
        if character.isalpha():
            ascii_offset = (
                FIRST_UPPERCASE_LETTER_ASCII
                if character.isupper()
                else FIRST_LOWERCASE_LETTER_ASCII
            )

            pi = ord(character) - ascii_offset
            ci = (pi + key) % ALPHABET_LENGTH

            rotatedText += chr(ci + ascii_offset)
        else:
            rotatedText += character

    return rotatedText


main()
