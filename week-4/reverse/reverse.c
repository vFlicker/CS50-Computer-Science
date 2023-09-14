#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#include "wav.h"

bool check_format(WAVHEADER header);
int get_block_size(WAVHEADER header);

const int BITS_IN_BYTE = 8;

int main(int argc, char *argv[])
{
    // Check command-line arguments
    if (argc != 3)
    {
        fprintf(stderr, "Usage: ./reverse input.wav output.wav\n");
        return 1;
    }

    // Open input file for reading
    FILE *input_file = fopen(argv[1], "r");
    if (input_file == NULL)
    {
        fprintf(stderr, "Could not open file.\n");
        return 1;
    }

    // Read header
    WAVHEADER header;

    fread(&header, sizeof(WAVHEADER), 1, input_file);

    // Use check_format to ensure WAV format
    if (check_format(header) == false)
    {
        fprintf(stderr, "Unsupported file format.\n");
        fclose(input_file);
        return 1;
    }

    // Open output file for writing
    FILE *output_file = fopen(argv[2], "w");
    if (output_file == NULL)
    {
        fprintf(stderr, "Could not open file.\n");
        fclose(input_file);
        return 1;
    }

    // Write header to file
    fwrite(&header, sizeof(WAVHEADER), 1, output_file);

    // Calculate size of block
    int block_size = get_block_size(header);

    // Set the pointer to the beginning of the file
    fseek(input_file, 0, SEEK_END);

    // Calculate audio size
    long audio_data_size = ftell(input_file) - sizeof(WAVHEADER);

    // Calculate number of blocks
    long block_count = audio_data_size / block_size;

    // Create a buffer for a single sample
    BYTE sample[block_size];

    for (int i = block_count - 1; i >= 0; i--)
    {
        fseek(input_file, sizeof(WAVHEADER) + (i * block_size), SEEK_SET);
        fread(&sample, sizeof(BYTE), block_size, input_file);
        fwrite(&sample, sizeof(BYTE), block_size, output_file);
    }

    // Close files
    fclose(input_file);
    fclose(output_file);

    return 0;
}

bool check_format(WAVHEADER header)
{
    return header.format[0] == 'W' && header.format[1] == 'A' && header.format[2] == 'V' && header.format[3] == 'E';
}

int get_block_size(WAVHEADER header)
{
    return (header.numChannels * header.bitsPerSample) / BITS_IN_BYTE;
}
