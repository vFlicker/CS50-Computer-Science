// Modifies the volume of an audio file

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef uint8_t HEADER;
typedef int16_t SAMPLE;

// Number of bytes in .wav header
const int HEADER_SIZE = 44;

int main(int argc, char *argv[])
{
    // Check command-line arguments
    if (argc != 4)
    {
        printf("Usage: ./volume input.wav output.wav factor\n");
        return 1;
    }

    // Open files and determine scaling factor
    FILE *input = fopen(argv[1], "r");
    if (input == NULL)
    {
        printf("Could not open file.\n");
        return 1;
    }

    FILE *output = fopen(argv[2], "w");
    if (output == NULL)
    {
        printf("Could not open file.\n");
        return 1;
    }

    float factor = atof(argv[3]);

    // Copy header from input file to output file
    HEADER header[HEADER_SIZE];

    fread(header, sizeof(HEADER), HEADER_SIZE, input);
    fwrite(header, sizeof(HEADER), HEADER_SIZE, output);

    // Create a buffer for a single sample
    SAMPLE sample;

    // Read single sample into buffer
    while (fread(&sample, sizeof(SAMPLE), 1, input))
    {
        // Update volume of sample
        sample *= factor;

        // Write updated sample to new file
        fwrite(&sample, sizeof(SAMPLE), 1, output);
    }

    // Close files
    fclose(input);
    fclose(output);
}
