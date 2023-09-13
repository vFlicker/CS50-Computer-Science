from pyfiglet import Figlet
import random
import sys

# Default variables
VALID_FLAGS = ["-f", "--font"]

# Initial Figlet
figlet = Figlet()


def main():
    # Ensure correct usage
    if len(sys.argv) not in [1, 3]:
        sys.exit("Invalid usage")

    if len(sys.argv) == 1:
        font = random.choice(figlet.getFonts())
    else:
        flag = sys.argv[1]
        font = sys.argv[2]

        if flag not in VALID_FLAGS or font not in figlet.getFonts():
            sys.exit("Invalid usage")

    # Prompt for input
    plaintext = input("Input: ")

    # Set font
    figlet.setFont(font=font)

    # Print the output
    print("Output:")
    print(figlet.renderText(plaintext))


main()
