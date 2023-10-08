#include <cs50.h>
#include <stdio.h>

long long get_card_number(void);
string check_card_type(long long card_number);
bool is_valid_card_number(long long card_number);

int main()
{
    // Prompt for input
    long long card_number = get_card_number();

    // Check for card length and starting digits
    string card_type = check_card_type(card_number);

    // Print the card type
    printf("%s\n", card_type);
}

long long get_card_number(void)
{
    long long card_number;

    do
    {
        card_number = get_long_long("Number: ");
    }
    while (card_number < 0);

    return card_number;
}

/*
    American Express: 15 digits, starts with 34 or 37.
    MasterCard: 16 digits, starts with 51, 52, 53, 54 or 55.
    Vise Express: 13 or 16 digits, starts with 4.
*/
string check_card_type(long long card_number)
{
    if (is_valid_card_number(card_number) == false)
    {
        return "INVALID";
    }

    int first_digit = 0;
    int second_digit = 0;
    int digit_count = 0;

    while (card_number > 0)
    {
        second_digit = first_digit;
        first_digit = card_number % 10;

        card_number /= 10;
        digit_count += 1;
    }

    int first_two_digits = (first_digit * 10) + second_digit;

    if (digit_count == 15 && (first_two_digits == 34 || first_two_digits == 37))
    {
        return "AMEX";
    }
    else if (digit_count == 16 && first_two_digits >= 51 && first_two_digits <= 55)
    {
        return "MASTERCARD";
    }
    else if (digit_count >= 13 && digit_count <= 16 && first_digit == 4)
    {
        return "VISA";
    }
    else
    {
        return "INVALID";
    }
}

/*
    Validation:

    1. Take each odd digit.
    2. Multiply each odd digit by 2.
    3. If the result is a two-digit number, split it (e.g., 12 --> 1 + 2).
    4. Add the obtained numbers to the even digits.
    5. Take the remainder of the sum divided by 2; if it's 0, then the validation is successful.
*/
bool is_valid_card_number(long long card_number)
{
    int result = 0;
    int digit_position = 1;

    while (card_number > 0)
    {
        int current_digit = card_number % 10;

        if (digit_position % 2 == 0) // Take each even digit
        {
            int multiplied_digit = current_digit * 2; // Multiply each one of them by 2
            result += (multiplied_digit / 10) + (multiplied_digit % 10);
        }
        else // Add every odd digit to the result
        {
            result += current_digit;
        }

        card_number /= 10;
        digit_position += 1;
    }

    // Check if the result is a multiple of 2
    return result % 10 == 0;
}
