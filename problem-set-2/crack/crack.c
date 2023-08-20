/*
    brian:51.xJagtPnb6s --> TF
    zamyla:50cI2vYkF0YU2 --> LOL
*/

#include <crypt.h>
#include <cs50.h>
#include <stdio.h>
#include <string.h>

#define _GNU_SOURCE
#define MAX_PASSWORD_LENGTH 5
#define LETTERS_COUNT 52

void extract_salt(string salt, string entered_hash);

int main(int argc, string argv[])
{
    // Check the number of command line arguments
    if (argc != 2)
    {
        printf("Usage: ./crack hash\n");
        return 1;
    }

    // Define the set of possible characters for the password
    string letters = "\0abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ";

    // Create an array to store the password
    char password[MAX_PASSWORD_LENGTH + 1];

    // Extraction of salt from the entered hash
    char salt[3];
    string entered_hash = argv[1];
    extract_salt(salt, entered_hash);

    // Generation of possible passwords and hash matching
    for (int fifth_char_index = 0; fifth_char_index < LETTERS_COUNT; fifth_char_index++)
    {
        for (int fourth_char_index = 0; fourth_char_index < LETTERS_COUNT; fourth_char_index++)
        {
            for (int third_char_index = 0; third_char_index < LETTERS_COUNT; third_char_index++)
            {
                for (int second_char_index = 0; second_char_index < LETTERS_COUNT; second_char_index++)
                {
                    for (int first_letter_index = 0; first_letter_index < LETTERS_COUNT; first_letter_index++)
                    {
                        password[0] = letters[first_letter_index];
                        password[1] = letters[second_char_index];
                        password[2] = letters[third_char_index];
                        password[3] = letters[fourth_char_index];
                        password[4] = letters[fifth_char_index];
                        password[5] = '\0';

                        // Skip empty passwords
                        if (strcmp(password, "\0") == 0)
                        {
                            continue;
                        }

                        // Generate the hash for the current password
                        string current_hash = crypt(password, salt);

                        // Check if the generated hash matches the entered hash
                        if (strcmp(current_hash, entered_hash) == 0)
                        {
                            printf("%s\n", password);
                            return 0;
                        }
                    }
                }
            }
        }
    }

    printf("Failed to crack the password\n");
    return 1;
}

void extract_salt(string salt, string entered_hash)
{
    salt[0] = entered_hash[0];
    salt[1] = entered_hash[1];
    salt[2] = '\0';
}
