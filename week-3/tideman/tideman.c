#include <cs50.h>
#include <stdio.h>
#include <string.h>

// Max number of candidates
#define MAX 9

// preferences[i][j] is number of voters who prefer i over j
int preferences[MAX][MAX];

// locked[i][j] means i is locked in over j
bool locked[MAX][MAX];

// Each pair has a winner, loser
typedef struct
{
    int winner;
    int loser;
} pair;

// Array of candidates
string candidates[MAX];
pair pairs[MAX * (MAX - 1) / 2];

int pair_count;
int candidate_count;

// Function prototypes
bool vote(int rank, string name, int ranks[]);
void record_preferences(int ranks[]);
void add_pairs(void);
void sort_pairs(void);
void lock_pairs(void);
void print_winner(void);
int calculate_difference(int index);
bool is_cycle(int winner, int loser_index);
bool is_source(int candidate_index);

int main(int argc, string argv[])
{
    // Check for invalid usage
    if (argc < 2)
    {
        printf("Usage: tideman [candidate ...]\n");
        return 1;
    }

    // Populate array of candidates
    candidate_count = argc - 1;
    if (candidate_count > MAX)
    {
        printf("Maximum number of candidates is %i\n", MAX);
        return 2;
    }
    for (int i = 0; i < candidate_count; i++)
    {
        candidates[i] = argv[i + 1];
    }

    // Clear graph of locked in pairs
    for (int i = 0; i < candidate_count; i++)
    {
        for (int j = 0; j < candidate_count; j++)
        {
            locked[i][j] = false;
        }
    }

    pair_count = 0;
    int voter_count = get_int("Number of voters: ");

    // Query for votes
    for (int i = 0; i < voter_count; i++)
    {
        // ranks[i] is voter's ith preference
        int ranks[candidate_count];

        // Query for each rank
        for (int j = 0; j < candidate_count; j++)
        {
            string name = get_string("Rank %i: ", j + 1);

            if (!vote(j, name, ranks))
            {
                printf("Invalid vote.\n");
                return 3;
            }
        }

        record_preferences(ranks);

        printf("\n");
    }

    add_pairs();
    sort_pairs();
    lock_pairs();
    print_winner();
    return 0;
}

// Update ranks given a new vote
bool vote(int rank, string name, int ranks[])
{
    for (int candidate_index = 0; candidate_index < candidate_count; candidate_index++)
    {
        if (strcmp(candidates[candidate_index], name) == 0)
        {
            ranks[rank] = candidate_index; // Update the ranks array
            return true;                   // Return true to indicate a successful vote
        }
    }

    return false; // Candidate name not found
}

// Update preferences given one voter's ranks
void record_preferences(int ranks[])
{
    for (int i = 0; i < candidate_count; i++)
    {
        int winner_index = ranks[i];

        for (int j = i + 1; j < candidate_count; j++)
        {
            int loser_index = ranks[j];
            preferences[winner_index][loser_index] += 1; // Update preferences
        }
    }
}

// Record pairs of candidates where one is preferred over the other
void add_pairs(void)
{
    for (int i = 0; i < candidate_count; i++)
    {
        for (int j = i + 1; j < candidate_count; j++)
        {
            if (preferences[i][j] == preferences[j][i])
            {
                continue;
            }
            else if (preferences[i][j] > preferences[j][i])
            {
                pairs[pair_count].winner = i;
                pairs[pair_count].loser = j;
            }
            else if (preferences[i][j] < preferences[j][i])
            {
                pairs[pair_count].winner = j;
                pairs[pair_count].loser = i;
            }

            pair_count += 1;
        }
    }
}

// Sort pairs in decreasing order by strength of victory
void sort_pairs(void)
{
    for (int i = 0; i < pair_count - 1; i++)
    {
        for (int j = 0; j < pair_count - 1 - i; j++)
        {
            int current_pair_difference = calculate_difference(j);
            int next_pair_difference = calculate_difference(j + 1);

            if (current_pair_difference < next_pair_difference)
            {
                pair temporary = pairs[j];
                pairs[j] = pairs[j + 1];
                pairs[j + 1] = temporary;
            }
        }
    }
}

// Lock pairs into the candidate graph in order, without creating cycles
void lock_pairs(void)
{
    // Iterate through sorted pairs and add to locked if no cycle is created
    for (int i = 0; i < pair_count; i++)
    {
        int winner_index = pairs[i].winner;
        int loser_index = pairs[i].loser;

        // Check if adding this edge creates a cycle
        if (is_cycle(winner_index, loser_index) == false)
        {
            locked[winner_index][loser_index] = true;
        }
    }
}

// Print the winner of the election
void print_winner(void)
{
    for (int candidate_index = 0; candidate_index < candidate_count; candidate_index++)
    {
        if (is_source(candidate_index) == true)
        {
            printf("%s\n", candidates[candidate_index]);
            break;
        }
    }
}

int calculate_difference(int index)
{
    int winner_index = pairs[index].winner;
    int loser_index = pairs[index].loser;

    int winner_votes = preferences[winner_index][loser_index];
    int loser_votes = preferences[loser_index][winner_index];

    return winner_votes - loser_votes;
}

bool is_cycle(int winner_index, int loser_index)
{
    // Base case: if the winner and loser are the same candidate, there's a cycle
    if (winner_index == loser_index)
    {
        return true; // Cycle found
    }

    // Check if there's a path from the winner to the loser
    for (int i = 0; i < candidate_count; i++)
    {
        // If there's a direct edge from candidate i to the winner,
        // recursively check if there's a path from candidate i to the loser.
        if (locked[i][winner_index] == true)
        {
            return is_cycle(i, loser_index); // Cycle found
        }
    }

    // If no cycle was found after checking all paths, return false.
    return false; // No cycle found
}

bool is_source(int candidate_index)
{
    for (int i = 0; i < pair_count; i++)
    {
        if (locked[i][candidate_index] == true)
        {
            return false;
        }
    }

    return true;
}
