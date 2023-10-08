# Questions

## What's `stdint.h`?

`stdint` is an abbreviation for "standard integer types." It is a set of data types defined in the C/C++ programming language standard (and sometimes supported by other programming languages) with the goal of providing portability and platform independence.

`stdint` provides integer data types with fixed sizes that do not depend on a specific computer architecture. For example, instead of using `int`, which can have different sizes on different platforms (e.g., 16 bits, 32 bits, or 64 bits), you can use `stdint` to define types with precise sizes.

Using `stdint` ensures confidence in the size of data types, reducing the risk of portability issues and avoiding problems related to incorrect integer sizes on specific platforms.

## What's the point of using `uint8_t`, `uint32_t`, `int32_t`, and `uint16_t` in a program?

In `stdint`, types like `int8_t`, `int16_t`, `int32_t`, `int64_t` are defined for signed integers with fixed sizes, and corresponding unsigned types `uint8_t`, `uint16_t`, `uint32_t`, `uint64_t` are provided. These types ensure a standard size regardless of the platform, making it easier to move code between different systems.

Here are a few examples of using these types:

- `uint8_t` (unsigned 8-bit integer type) is used when values need to be stored in the range of 0 to 255 without using a sign bit.
- `uint16_t` (unsigned 16-bit integer type) is used when values need to be stored in the range of 0 to 65,535 without using a sign bit.
- `int32_t` (signed 32-bit integer type) is used when values need to be stored in the range of -2,147,483,648 to 2,147,483,647, including zero.
- `uint32_t` (unsigned 32-bit integer type) is used when values need to be stored in the range of 0 to 4,294,967,295 without using a sign bit.

## How many bytes is a `BYTE`, a `DWORD`, a `LONG`, and a `WORD`, respectively?

- `BYTE` consists of 1 byte (`uint8_t`).
- `DWORD` consists of 4 bytes (`uint32_t`).
- `LONG` consists of 4 bytes (`int32_t`).
- `WORD` consists of 2 bytes (`uint16_t`).

## What (in ASCII, decimal, or hexadecimal) must the first two bytes of any BMP file be? Leading bytes used to identify file formats (with high probability) are generally called "magic numbers."

The first two bytes of any BMP file are used to identify the file format and are often referred to as "magic numbers." They should be represented in hexadecimal.

## What's the difference between `bfSize` and `biSize`?

- `bfSize` is a field that specifies the size in bytes of the BMP file. It is located in the `BITMAPFILEHEADER` structure.
- `biSize` is a field that specifies the size in bytes of the headers in the BMP file. It is located in the `BITMAPINFOHEADER` structure.

## What does it mean if `biHeight` is negative?

If `biHeight` is negative, the bitmap image is a top-down Device Independent Bitmap (DIB), and its origin is in the upper-left corner. When `biHeight` is negative, indicating a top-down DIB, `biCompression` should be either `BI_RGB` or `BI_BITFIELDS`. A top-down DIB cannot be compressed.

## What field in `BITMAPINFOHEADER` specifies the BMP's color depth (i.e., bits per pixel)?

The `biBitCount` field in the `BITMAPINFOHEADER` structure defines the BMP color depth, which is the number of bits used to represent the color of each pixel in the image.

`biBitCount = 1`: Used for black and white (monochrome) format, where each pixel can be either black or white, and 1 bit is used per pixel.
`biBitCount = 8`: Used for indexed color, where image colors are stored as indexes in a color palette, and 8 bits are used per pixel (256 possible colors).
`biBitCount = 24`: Used for full color (RGB), where each pixel is represented by red, green, and blue components, and 24 bits are used per pixel (16.7 million colors).

The value of `biBitCount` determines the number of possible colors and the method of color representation in the BMP file.

## Why might `fopen` return `NULL` in lines 24 and 32 of `copy.c`?

`fopen` can return `NULL` if it fails to open the input or output file.

## Why is the third argument to `fread` always `1` in our code?

The third argument of `fread` is always `1` because we are reading structures of type `BITMAPFILEHEADER` or `BITMAPINFOHEADER`, and we are reading them one at a time.

## What value does line 65 of `copy.c` assign to `padding` if `bi.biWidth` is `3`?

`padding` would be equal to 3

```
4 - (bi.biWidth * sizeof(RGBTRIPLE)) % 4) % 4 = x
4 - (8 * 3) % 4) % 4 = x
4 - (9 % 4) % 4 = x
4 - (9 % 4) % 4 = x
(4 - 1) % 4 = x
x = 3
```

## What does `fseek` do?

`fseek` moves the read position of the input file by `padding` bytes from the current position, effectively skipping over any extra padding in the input file.

## What is `SEEK_CUR`?

`fseek` moves the read position of the input file by `padding` bytes from the current position, effectively skipping over any extra padding in the input file.

## Whodunit?

`SEEK_CUR` is one of the constants for the `origin` argument in the `fseek` function. Using `SEEK_CUR` indicates that the offset is calculated from the current file position.
