#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

const char FIRST_UPPERCASE_LETTER = 'A';
const char FIRST_LOWERCASE_LETTER = 'a';
const int ALPHABET_LENGTH = 26;

bool is_valid_argument(string argument);
char rotate(char symbol, int key);

int main(int argc, string argv[])
{
    // Check that the user entered a single argument
    // and the every character in argv[1] is a digit
    if (argc != 2 || is_valid_argument(argv[1]) == false)
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }

    // Remember key
    int key = atoi(argv[1]);

    // Prompt user for plaintext
    string plaintext = get_string("plaintext:  ");

    // Print the beginning for output
    printf("ciphertext: ");

    // For each character in the plaintext
    for (int i = 0, length = strlen(plaintext); i < length; i++)
    {
        // Print “rotated” character
        printf("%c", rotate(plaintext[i], key));
    }

    // Print newline
    printf("\n");

    return 0;
}

bool is_valid_argument(string argument)
{
    for (int i = 0, length = strlen(argument); i < length; i++)
    {
        if (!isdigit(argument[i]))
        {
            return false;
        }
    }

    return true;
}

char rotate(char symbol, int key)
{
    if (isalpha(symbol))
    {
        int ascii_offset = isupper(symbol) ? FIRST_UPPERCASE_LETTER : FIRST_LOWERCASE_LETTER;

        char pi = symbol - ascii_offset;
        char ci = (pi + key) % ALPHABET_LENGTH;

        return ci + ascii_offset;
    }
    else
    {
        return symbol;
    }
}
