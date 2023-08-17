#include <cs50.h>
#include <ctype.h>
#include <math.h>
#include <stdio.h>
#include <string.h>

int count_letters(string text);
int count_words(string text);
int count_sentences(string text);
int calculate_index(int letters, int words, int sentences);
void print_grade(int index);

int main(void)
{
    // Prompt the user for some text
    string text = get_string("Text: ");

    // Count the number of letters, words, and sentences in the text
    int letter_count = count_letters(text);
    int word_count = count_words(text);
    int sentence_count = count_sentences(text);

    // Compute the Coleman-Liau index
    int index = calculate_index(letter_count, word_count, sentence_count);

    // Print the grade level
    print_grade(index);
}

int count_letters(string text)
{
    int letter_count = 0;

    for (int i = 0, length = strlen(text); i < length; i++)
    {
        if (isalpha(text[i]))
        {
            letter_count += 1;
        }
    }

    return letter_count;
}

int count_words(string text)
{
    int word_count = 1; // At least one word in a non-empty text

    for (int i = 0, length = strlen(text); i < length; i++)
    {
        if (isspace(text[i]))
        {
            word_count += 1;
        }
    }

    return word_count;
}

int count_sentences(string text)
{
    int sentence_count = 0;

    for (int i = 0, length = strlen(text); i < length; i++)
    {
        char currentChar = text[i];

        if (currentChar == '.' || currentChar == '!' || currentChar == '?')
        {
            sentence_count += 1;
        }
    }

    return sentence_count;
}

int calculate_index(int letters, int words, int sentences)
{
    float L = (float) letters / words * 100;
    float S = (float) sentences / words * 100;

    return round(0.0588 * L - 0.296 * S - 15.8);
}

void print_grade(int index)
{
    if (index >= 16)
    {
        printf("Grade 16+\n");
    }
    else if (index < 1)
    {
        printf("Before Grade 1\n");
    }
    else
    {
        printf("Grade %i\n", index);
    }
}
