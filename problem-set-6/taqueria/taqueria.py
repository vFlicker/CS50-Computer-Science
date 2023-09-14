# Define the menu with prices
menu = {
    "Baja Taco": 4.00,
    "Burrito": 7.50,
    "Bowl": 8.50,
    "Nachos": 11.00,
    "Quesadilla": 8.50,
    "Super Burrito": 8.50,
    "Super Quesadilla": 9.50,
    "Taco": 3.00,
    "Tortilla Salad": 8.00,
}


def main():
    total = 0

    while True:
        try:
            # Prompt the user to enter the item's name
            item = input("Item: ").title()

            # Check if the item is in the menu
            if item in menu:
                total += menu[item]

                # Display the total order amount with 2 decimal places
                print(f"Total: ${total:.2f}")
        except EOFError:
            break


main()
