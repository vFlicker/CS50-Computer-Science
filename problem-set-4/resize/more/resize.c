#include <stdio.h>
#include <stdlib.h>

#include "bmp.h"

int main(int argc, char *argv[])
{
    // ensure proper usage
    if (argc != 4)
    {
        fprintf(stderr, "Usage: ./resize n infile outfile\n");
        return 1;
    }

    // remember resizing factor
    float f = atof(argv[1]);

    // ensure correct factor
    if (f < 0.0 || f > 100.0)
    {
        fprintf(stderr, "Invalid resizing factor. It must be in the range (0.0, 100.0].\n");
        return 1;
    }

    // remember filenames
    char *infile = argv[2];
    char *outfile = argv[3];

    // open input file
    FILE *inptr = fopen(infile, "r");
    if (inptr == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", infile);
        return 2;
    }

    // open output file
    FILE *outptr = fopen(outfile, "w");
    if (outptr == NULL)
    {
        fclose(inptr);
        fprintf(stderr, "Could not create %s.\n", outfile);
        return 3;
    }

    // read infile's BITMAPFILEHEADER
    BITMAPFILEHEADER bf;
    fread(&bf, sizeof(BITMAPFILEHEADER), 1, inptr);

    // read infile's BITMAPINFOHEADER
    BITMAPINFOHEADER bi;
    fread(&bi, sizeof(BITMAPINFOHEADER), 1, inptr);

    // ensure infile is (likely) a 24-bit uncompressed BMP 4.0
    if (bf.bfType != 0x4d42 || bf.bfOffBits != 54 || bi.biSize != 40 || bi.biBitCount != 24 || bi.biCompression != 0)
    {
        fclose(outptr);
        fclose(inptr);
        fprintf(stderr, "Unsupported file format.\n");
        return 4;
    }

    // calculate old and new dimensions
    int oldWidth = bi.biWidth;
    int oldHeight = bi.biHeight;

    int newWidth = oldWidth * f;
    int newHeight = oldHeight * f;

    // calculate paddings
    int oldPadding = (4 - (oldWidth * sizeof(RGBTRIPLE)) % 4) % 4;
    int newPadding = (4 - (newWidth * sizeof(RGBTRIPLE)) % 4) % 4;

    // reconfigure headers
    bi.biWidth = newWidth;
    bi.biHeight = newHeight;
    bi.biSizeImage = ((sizeof(RGBTRIPLE) * newWidth) + newPadding) * abs(newHeight);
    bf.bfSize = bi.biSizeImage + sizeof(BITMAPFILEHEADER) + sizeof(BITMAPINFOHEADER);

    // write outfile's BITMAPFILEHEADER
    fwrite(&bf, sizeof(BITMAPFILEHEADER), 1, outptr);

    // write outfile's BITMAPINFOHEADER
    fwrite(&bi, sizeof(BITMAPINFOHEADER), 1, outptr);

    // allocate memory for factored scanlines
    RGBTRIPLE scanline[newWidth * sizeof(RGBTRIPLE)];

    // iterate over output scanlines
    for (int rowIndex = 0, biHeight = abs(newHeight); rowIndex < biHeight; rowIndex++)
    {
        // iterate over pixels in the output scanline
        for (int pixelIndex = 0; pixelIndex < newWidth; pixelIndex++)
        {
            // calculate corresponding pixel coordinates in the old image
            int oldRowIndex = rowIndex / f;
            int oldPixelIndex = pixelIndex / f;

            // calculate the old image position
            int headers = sizeof(BITMAPFILEHEADER) + sizeof(BITMAPINFOHEADER);
            int skippedRows = (oldWidth * sizeof(RGBTRIPLE) + oldPadding) * oldRowIndex;
            int skipedPixels = oldPixelIndex * sizeof(RGBTRIPLE);

            // temporary storage
            RGBTRIPLE triple;

            // seek to the corresponding position in the old image
            fseek(inptr, headers + skippedRows + skipedPixels, SEEK_SET);

            // read RGB triple from infile
            fread(&triple, sizeof(RGBTRIPLE), 1, inptr);

            scanline[pixelIndex] = triple;
        }

        // write the resized scanline to the output image
        fwrite(scanline, sizeof(RGBTRIPLE), newWidth, outptr);

        // then add it back (to demonstrate how)
        for (int j = 0; j < newPadding; j++)
        {
            fputc(0x00, outptr);
        }
    }

    // close infile
    fclose(inptr);

    // close outfile
    fclose(outptr);

    // success
    return 0;
}
