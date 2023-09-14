def main():
    # Prompt the user for a greeting
    greeting = input("Greeting: ")

    # Remove leading and trailing whitespace,
    # and convert to lowercase for case-insensitive comparison
    greeting = greeting.strip().lower()

    # Check the conditions and output the corresponding amount
    if greeting.startswith("hello"):
        print("$0")
    elif greeting.startswith("h"):
        print("$20")
    else:
        print("$100")


main()
