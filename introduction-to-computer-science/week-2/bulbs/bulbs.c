#include <cs50.h>
#include <stdio.h>
#include <string.h>

const int BITS_IN_BYTE = 8;

void print_bulb(int bit);

int main(void)
{
    // Prompt user for a message
    string message = get_string("Message: ");

    // For each character in the message:
    for (int i = 0, length = strlen(message); i < length; i++)
    {
        int bits[BITS_IN_BYTE];
        int ascii_code = message[i]; // Convert the character to its ASCII decimal value

        for (int j = BITS_IN_BYTE - 1; j >= 0; j--)
        {
            if (ascii_code > 0 && ascii_code % 2 == 1)
            {
                bits[j] = 1;
            }
            else
            {
                bits[j] = 0;
            }

            ascii_code /= 2;
        }

        for (int j = 0; j < BITS_IN_BYTE; j++)
        {
            print_bulb(bits[j]);
        }

        printf("\n");
    }
}

void print_bulb(int bit)
{
    if (bit == 0)
    {
        // Dark emoji
        printf("\U000026AB");
    }
    else if (bit == 1)
    {
        // Light emoji
        printf("\U0001F7E1");
    }
}
