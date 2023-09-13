def main():
    height = width = get_height()
    print_pyramid(height, width)


def get_height():
    while True:
        try:
            height = int(input("Height: "))
            if height > 0 and height < 9:
                break
        except ValueError:
            None

    return height


def print_pyramid(height, width):
    for i in range(1, height + 1):
        hash_count = i
        space_count = width - hash_count

        print(" " * space_count, end="")
        print("#" * hash_count)


main()
