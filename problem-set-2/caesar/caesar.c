#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define FIRST_UPPERCASE_LETTER 'A'
#define FIRST_LOWERCASE_LETTER 'a'
#define ALPHABET_LENGTH 26

bool only_digits(string string);
char rotate(char symbol, int key);

int main(int argc, string argv[])
{
    // Сheck that the user entered a single argument
    // and the every character in argv[1] is a digit
    if (argc != 2 || only_digits(argv[1]) == false)
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }

    // Convert argv[1] from a `string` to an `int`
    int key = atoi(argv[1]);

    // Prompt user for plaintext
    string plaintext = get_string("plaintext:  ");

    printf("ciphertext: ");

    // For each character in the plaintext:
    for (int i = 0, length = strlen(plaintext); i < length; i++)
    {
        printf("%c", rotate(plaintext[i], key));
    }

    printf("\n");

    return 0;
}

bool only_digits(string string)
{
    for (int i = 0, length = strlen(string); i < length; i++)
    {
        if (!isdigit(string[i]))
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
