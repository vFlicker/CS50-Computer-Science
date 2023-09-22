from nltk.tokenize import sent_tokenize


def lines(a, b):
    """Return lines in both a and b"""

    a_lines = set(a.split("\n"))
    b_lines = set(b.split("\n"))

    return a_lines & b_lines


def sentences(a, b):
    """Return sentences in both a and b"""

    a_sentences = set(sent_tokenize(a))
    b_sentences = set(sent_tokenize(b))

    return a_sentences & b_sentences


def substrings(a, b, n):
    """Return substrings of length n in both a and b"""

    a_substrings = set(get_substrings(a, n))
    b_substrings = set(get_substrings(b, n))

    return a_substrings & b_substrings


def get_substrings(string, n):
    substrings = []

    for start in range(len(string) - n + 1):
        end = start + n
        substrings.append(string[start:end])

    return substrings
