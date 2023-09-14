def main():
    # Prompt for input
    card_number = get_card_number()

    # Check for card length and starting digits
    card_type = check_card_type(card_number)

    # Print the card type
    print(card_type)


def get_card_number():
    while True:
        try:
            card_number = int(input("Number: "))
            if card_number >= 0:
                break
        except ValueError:
            None

    return card_number


# American Express: 15 digits, starts with 34 or 37.
# MasterCard: 16 digits, starts with 51, 52, 53, 54 or 55.
# Vise Express: 13 or 16 digits, starts with 4.
def check_card_type(card_number):
    if is_valid_checksum(card_number) == False:
        return "INVALID"

    first_digit = second_digit = 0
    digit_count = 0

    while card_number > 0:
        second_digit = first_digit
        first_digit = card_number % 10

        card_number //= 10
        digit_count += 1

    first_two_digits = (first_digit * 10) + second_digit

    if digit_count == 15 and first_two_digits in [34, 37]:
        return "AMEX"
    elif digit_count == 16 and first_two_digits in range(51, 56):
        return "MASTERCARD"
    elif digit_count in range(13, 17) and first_digit == 4:
        return "VISA"
    else:
        return "INVALID"


# Validation:
#   1. Take each odd digit.
#   2. Multiply each odd digit by 2.
#   3. If the result is a two-digit number, split it (e.g., 12 --> 1 + 2).
#   4. Add the obtained numbers to the even digits.
#   5. Take the remainder of the sum divided by 2; if it's 0, then the validation is successful.
def is_valid_checksum(card_number):
    result = 0
    digit_position = 1

    while card_number > 0:
        current_digit = card_number % 10

        if digit_position % 2 == 0:  # Take each even digit
            multiplied_digit = current_digit * 2  # Multiply each one of them by 2
            result += (multiplied_digit // 10) + (multiplied_digit % 10)
        else:  # Add every odd digit to the result
            result += current_digit

        card_number //= 10
        digit_position += 1

    # Check if the result is a multiple of 2
    return result % 10 == 0


main()
