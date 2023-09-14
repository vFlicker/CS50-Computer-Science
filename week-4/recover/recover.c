#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>

#define BUFFER_SIZE 512

typedef uint8_t BYTE;

int main(int argc, char *argv[])
{
    // Check command-line arguments
    if (argc != 2)
    {
        fprintf(stderr, "Usage: ./recover image\n");
        return 1;
    }

    // Remember filename
    char *infile_name = argv[1];

    // Open input file for reading
    FILE *input_file = fopen(infile_name, "r");
    if (input_file == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", infile_name);
        return 1;
    }

    // Initialize variables
    BYTE buffer[512];
    FILE *output_file = NULL;
    char outfile_name[8];
    int jpg_count = 0;

    // Until we reached the end of memory, read 512 bytes into the buffer
    while (fread(buffer, sizeof(BYTE), BUFFER_SIZE, input_file) == BUFFER_SIZE)
    {
        bool isJPEGHeader = buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0;

        // Check for the start of a new JPEG
        if (isJPEGHeader)
        {
            // Close the previous JPEG file, if open
            if (output_file != NULL)
            {
                fclose(output_file);
            }

            // Create a new JPEG file
            sprintf(outfile_name, "%03i.jpg", jpg_count);
            output_file = fopen(outfile_name, "w");
            if (output_file == NULL)
            {
                fclose(input_file);
                fprintf(stderr, "Could not create %s.\n", outfile_name);
                return 1;
            }

            jpg_count += 1;
        }

        // Write data to the current JPEG file
        if (output_file != NULL)
        {
            fwrite(buffer, sizeof(BYTE), BUFFER_SIZE, output_file);
        }
    }

    // Close files
    fclose(output_file);
    fclose(input_file);

    return 0;
}
