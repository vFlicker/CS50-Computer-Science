from sys import argv, exit


def main():
    # Check the number of command line arguments
    if not len(argv) == 2:
        print("Usage: python bleep.py dictionary")
        exit(1)

    # Remember path
    path = argv[1]

    # Create new set of words
    banned_words = set()

    # Open and read from the file the list of words
    with open(path, "r") as file:
        for line in file:
            word = line.strip()
            banned_words.add(word)

    # Prompt for input
    message = input("What message would you like to censor?\n")

    # Tokenize the message
    inputted_words = message.split(" ")

    # Create a list for censor banned words
    censored_message = []

    for inputted_word in inputted_words:
        if inputted_word.lower() in banned_words:
            censored_message.append(censor_word(inputted_word))
        else:
            censored_message.append(inputted_word)

    # Print the censored message
    censored_message = " ".join(censored_message)
    print(censored_message)


def censor_word(word):
    return "*" * len(word)


if __name__ == "__main__":
    main()
