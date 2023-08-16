#include <cs50.h>
#include <stdio.h>

int get_height(void);
void printPyramid(int height, int width);
void repeat(string symbol, int times);

int main(void)
{
    int height = get_height();
    int wight = height;

    printPyramid(height, wight);
}

int get_height(void)
{
    int height;

    do
    {
        height = get_int("Height: ");
    }
    while (height < 1 || height > 8);

    return height;
}

void printPyramid(int height, int width)
{
    for (int i = 1; i <= height; i++)
    {
        int hash_count = i;
        int space_count = width - hash_count;

        repeat(" ", space_count);
        repeat("#", hash_count);

        printf("\n");
    }
}

void repeat(string symbol, int times)
{
    for (int i = 0; i < times; i++)
    {
        printf("%s", symbol);
    }
}
