// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
} node;

// Function prototypes
void unloader(node *current_node);

// Global variables
const unsigned int N = 1000; // Choose number of buckets in hash table
node *table[N];              // Hash table
int number_of_words = 0;     // The number of words in the dictionary

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    // Hash the word to determine the index in the table
    unsigned int hash_index = hash(word);

    // Traverse the linked list at the given index
    node *current_node = table[hash_index];

    while (current_node != NULL)
    {
        if (strcasecmp(current_node->word, word) == 0)
        {
            return true; // Word found in dictionary
        }

        current_node = current_node->next;
    }

    return false; // Word not found in dictionary
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    int hashValue = 0;

    for (int i = 0, length = strlen(word); i < length; i++)
    {
        hashValue += (int) toupper(word[i]);
    }

    return hashValue % N;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    // Open dictionary file
    FILE *file = fopen(dictionary, "r");
    if (file == NULL)
    {
        return false;
    }

    // Initialize all hash table elements as NULL
    for (int i = 0; i < N; i++)
    {
        table[i] = NULL;
    }

    // Buffer to store words read from the dictionary
    char word[LENGTH + 1];

    // Add words to hash table
    while (fscanf(file, "%s", word) == 1)
    {
        // Allocate memory for a new node
        node *new_node = malloc(sizeof(node));
        if (new_node == NULL)
        {
            return false;
        }

        unsigned int hash_index = hash(word);

        strcpy(new_node->word, word);
        new_node->next = table[hash_index];

        table[hash_index] = new_node;

        // Increase the number of words
        number_of_words += 1;
    }

    fclose(file);

    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    return number_of_words;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    // Iterate over all buckets in hash table
    for (int i = 0; i < N; i++)
    {
        node *current_node = table[i];

        while (current_node != NULL)
        {
            node *previous_node = current_node;
            current_node = current_node->next;
            free(previous_node);
        }
    }

    return true;
}
