#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

const char FIRST_LOWERCASE_LETTER = 'a';
const int ALPHABET_LENGTH = 26;

// Function prototypes
bool is_valid_argument(string argument);
char substitute(char symbol, string key);
int get_alphabet_index(char symbol);

int main(int argc, string argv[])
{
    // Check that the user entered a single argument
    if (argc != 2)
    {
        printf("Usage: ./substitution key\n");
        return 1;
    }

    // Check that the entered key is valid
    if (is_valid_argument(argv[1]) == false)
    {
        printf("Key must contain 26 characters.\n");
        return 1;
    }

    string key = argv[1];

    // Prompt user for plaintext
    string plaintext = get_string("plaintext:  ");

    // Print the beginning for output
    printf("ciphertext: ");

    // For each character in the plaintext
    for (int i = 0, length = strlen(plaintext); i < length; i++)
    {
        // Print substituted character
        printf("%c", substitute(plaintext[i], key));
    }

    // Print newline
    printf("\n");

    return 0;
}

bool is_valid_argument(string argument)
{
    if (strlen(argument) != ALPHABET_LENGTH)
    {
        return false;
    }

    // Check that all characters are alphabetic
    for (int i = 0; i < ALPHABET_LENGTH; i++)
    {
        if (!isalpha(argument[i]))
        {
            return false;
        }
    }

    // Initialize all elements of the letters array to false (absent)
    bool letters[ALPHABET_LENGTH] = {false};

    // Check that all letters are present exactly once
    for (int i = 0; i < ALPHABET_LENGTH; i++)
    {
        int index = get_alphabet_index(argument[i]);

        if (letters[index] == true)
        {
            return false;
        }

        letters[index] = true;
    }

    return true;
}

char substitute(char symbol, string key)
{
    if (isalpha(symbol))
    {
        int index = get_alphabet_index(symbol);
        return isupper(symbol) ? toupper(key[index]) : tolower(key[index]);
    }
    else
    {
        return symbol;
    }
}

int get_alphabet_index(char symbol)
{
    int index = tolower(symbol) - FIRST_LOWERCASE_LETTER;
    return index;
}
