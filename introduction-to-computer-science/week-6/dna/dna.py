import csv
import sys


def main():
    # Check for command-line usage
    if len(sys.argv) != 3:
        sys.exit("Usage: python dna.py <database.csv> <sequence.txt>")

    # Read database file into a variable
    database = read_database(sys.argv[1])

    # Read DNA sequence file into a variable
    dna_sequence = read_dna_sequence(sys.argv[2])

    # Find longest match of each STR in DNA sequence
    headers = database[0].keys()
    sequence_str_counts = find_longest_match_of_each_str(headers, dna_sequence)

    # Check database for matching profiles
    profile = find_matching_profile(database, sequence_str_counts)

    if profile:
        print(profile["name"])
    else:
        print("No match")


def read_database(filename):
    with open(filename, "r") as file:
        reader = csv.DictReader(file)
        return list(reader)


def read_dna_sequence(filename):
    with open(filename, "r") as file:
        return file.read()


def find_longest_match_of_each_str(headers, sequence):
    sequence_str_counts = {}

    for header in headers:
        if header != "name":
            sequence_str_counts[header] = longest_match(sequence, header)

    return sequence_str_counts


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):
        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:
            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run


def find_matching_profile(database, sequence_str_counts):
    for profile in database:
        match = True

        for header in sequence_str_counts:
            if int(profile[header]) != sequence_str_counts[header]:
                match = False
                break

        if match == True:
            return profile

    return None


main()
