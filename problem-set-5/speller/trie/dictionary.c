// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "dictionary.h"

// Represents number of children for each node in a trie
#define N 27

// Represents a node in a trie
typedef struct node
{
    bool is_word;
    struct node *children[N];
} node;

// Function prototypes
node *make_node();
void unloader(node *current_node);

// Global variables
node *root;              // Root of trie
int number_of_words = 0; // The number of words in the dictionary

// Returns true if word is in dictionary else false
bool check(const char *word)
{
    node *cursor = root;

    for (int i = 0, length = strlen(word); i < length; i++)
    {
        unsigned int hash_index = hash(word[i]);

        // If there is no child
        if (cursor->children[hash_index] == NULL)
        {
            return false; // Word not found
        }

        // Go to node which we may have just been made
        cursor = cursor->children[hash_index];
    }

    return cursor->is_word; // Check if it is a complete word
}

// Hashes charapter to a number
unsigned int hash(const char c)
{
    return c == '\'' ? N - 1 : toupper(c) - 'A';
}

// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    // Initialize the trie root
    root = make_node();
    if (root == NULL)
    {
        return false;
    }

    // Open dictionary file
    FILE *file = fopen(dictionary, "r");
    if (file == NULL)
    {
        return false;
    }

    // Buffer to store words read from the dictionary
    char word[LENGTH + 1];

    // Add words to trie
    while (fscanf(file, "%s", word) == 1)
    {
        node *cursor = root;

        for (int i = 0, length = strlen(word); i < length; i++)
        {
            unsigned int hash_index = hash(word[i]);

            // If there is no child
            if (cursor->children[hash_index] == NULL)
            {
                // Make new node
                node *new_node = make_node();
                if (new_node == NULL)
                {
                    fclose(file);
                    unload();
                    return false;
                }

                cursor->children[hash_index] = new_node;
            }

            // Go to node which we may have just been made
            cursor = cursor->children[hash_index];
        }

        // If we are at the end of the word, make it as being a word
        cursor->is_word = true;

        // Increase the number of words
        number_of_words += 1;
    }

    fclose(file);

    return true;
}

// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    return number_of_words;
}

// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    unloader(root);

    return true;
}

node *make_node()
{
    // Allocate memory for the new node
    node *new_node = malloc(sizeof(node));
    if (new_node == NULL)
    {
        return false;
    }

    new_node->is_word = false;
    for (int i = 0; i < N; i++)
    {
        new_node->children[i] = NULL;
    }

    return new_node;
}

void unloader(node *current_node)
{
    // Iterate over all the children to see if they point to anything
    // and go there if they do point
    for (int i = 0; i < N; i++)
    {
        if (current_node->children[i] != NULL)
        {
            unloader(current_node->children[i]);
        }
    }

    // After we check all the children point to null we can get rid of the node
    // and return to the previous iteration of this function.
    free(current_node);
}
