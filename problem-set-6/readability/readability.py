def main():
    # Prompt the user for some text
    text = input("Text: ")

    # Count the number of letters, words, and sentences in the text
    letter_count = count_letters(text)
    word_count = count_words(text)
    sentence_count = count_sentences(text)

    # Compute the Coleman-Liau index
    index = calculate_index(letter_count, word_count, sentence_count)

    # Print the grade level
    print_grade(index)


def count_letters(text):
    letter_count = 0

    for character in text:
        if character.isalpha():
            letter_count += 1

    return letter_count


def count_words(text):
    word_count = 1  # At least one word in a non-empty text

    for character in text:
        if character.isspace():
            word_count += 1

    return word_count


def count_sentences(text):
    sentence_count = 0

    for character in text:
        if character == "." or character == "!" or character == "?":
            sentence_count += 1

    return sentence_count


def calculate_index(letters, words, sentences):
    l = letters / words * 100
    s = sentences / words * 100

    return round(0.0588 * l - 0.296 * s - 15.8)


def print_grade(index):
    if index >= 16:
        print("Grade 16+")
    elif index < 1:
        print("Before Grade 1")
    else:
        print(f"Grade {index}")


main()
