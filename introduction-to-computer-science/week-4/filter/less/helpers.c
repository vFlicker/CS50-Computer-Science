#include <math.h>

#include "helpers.h"

RGBTRIPLE calculateBlurredPixel(int i, int j, int height, int width, RGBTRIPLE image[height][width]);

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            RGBTRIPLE currentPixel = image[i][j];

            int originalRed = currentPixel.rgbtRed;
            int originalGreen = currentPixel.rgbtGreen;
            int originalBlue = currentPixel.rgbtBlue;

            int averageValue = round((originalRed + originalGreen + originalBlue) / 3.0);

            image[i][j].rgbtRed = averageValue;
            image[i][j].rgbtGreen = averageValue;
            image[i][j].rgbtBlue = averageValue;
        }
    }
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            RGBTRIPLE currentPixel = image[i][j];

            int originalRed = currentPixel.rgbtRed;
            int originalGreen = currentPixel.rgbtGreen;
            int originalBlue = currentPixel.rgbtBlue;

            int sepiaRed = round(0.393 * originalRed + 0.769 * originalGreen + 0.189 * originalBlue);
            int sepiaGreen = round(0.349 * originalRed + 0.686 * originalGreen + 0.168 * originalBlue);
            int sepiaBlue = round(0.272 * originalRed + 0.534 * originalGreen + 0.131 * originalBlue);

            image[i][j].rgbtRed = fmin(sepiaRed, 255);
            image[i][j].rgbtGreen = fmin(sepiaGreen, 255);
            image[i][j].rgbtBlue = fmin(sepiaBlue, 255);
        }
    }
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width / 2; j++)
        {
            RGBTRIPLE leftPixel = image[i][j];
            RGBTRIPLE rightPixel = image[i][width - 1 - j];

            image[i][j] = rightPixel;
            image[i][width - 1 - j] = leftPixel;
        }
    }
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    // Allocate memory for a copy of the image
    RGBTRIPLE imageCopy[height][width];

    // Copy the original image to the imageCopy array
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            imageCopy[i][j] = image[i][j];
        }
    }

    // Iterate over all image rows
    for (int i = 0; i < height; i++)
    {
        // Iterate over all image pixels in row
        for (int j = 0; j < width; j++)
        {
            // Calculate the blurred pixel using the neighboring pixels
            image[i][j] = calculateBlurredPixel(i, j, height, width, imageCopy);
        }
    }
}

RGBTRIPLE calculateBlurredPixel(int rowIndex, int pixelIndex, int height, int width, RGBTRIPLE image[height][width])
{
    float totalRed = 0;
    float totalGreen = 0;
    float totalBlue = 0;

    int count = 0;

    // Iteration over all square 3x3 pixels
    for (int i = -1; i <= 1; i++)
    {
        for (int j = -1; j <= 1; j++)
        {
            int neighborRowIndex = rowIndex + i;
            int neighborPixelIndex = pixelIndex + j;

            // Check if the neighbor pixel is within the image boundaries
            if (neighborRowIndex >= 0 && neighborRowIndex < height && neighborPixelIndex >= 0 && neighborPixelIndex < width)
            {
                RGBTRIPLE currentPixel = image[neighborRowIndex][neighborPixelIndex];

                totalRed += currentPixel.rgbtRed;
                totalGreen += currentPixel.rgbtGreen;
                totalBlue += currentPixel.rgbtBlue;

                count += 1;
            }
        }
    }

    // Calculate the average values for the blurred pixel
    RGBTRIPLE blurryPixel;

    blurryPixel.rgbtRed = round(totalRed / count);
    blurryPixel.rgbtGreen = round(totalGreen / count);
    blurryPixel.rgbtBlue = round(totalBlue / count);

    return blurryPixel;
}
