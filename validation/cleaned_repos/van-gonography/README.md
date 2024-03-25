#### Hide any type of files inside a image of your choice

# Features

- **File Hiding:** Hide any type of file within an image of your choice, without altering the image's visual appearance.
- **Decoding Capability:** Decode hidden files from images.
- **Image Comparison:** Visualize the difference between two images.
- **Detailed Logging:** Create a log file that records comprehensive information about the program's execution.
- **Command-Line Interface (CLI):** Offers a developer-friendly mode with command-line options for more advanced usage.
- **User Interface (UI):** Provides an intuitive and easy-to-use mode for non-developers.
- **Open After Decoding:** Automatically open the decoded file after extracting it from the image.
- **Cross-Platform:** Works on Windows, Linux, and macOS.
- **Free and Open-Source:** Van Gonography is completely free and open-source, and will always be.
- **Encryption:** Encrypt the hidden file with a password of your choice *(coming soon)*.
- **Compression:** Compress the hidden file to reduce its size *(coming soon)*.
- **Multiple Files:** Hide multiple files inside an image *(coming soon)*.
- **Stealth Mode:** Hide the fact that the image contains a hidden file *(coming soon)*.
- **User settings:** Save your preferences for future use.

# How it works

**The Basics of Digital Storage**

Everything on your computer, from `.exe` files to `.jpg` images, is stored as bits. Bits are just 1s and 0s. For instance:
- The letter `A` = `01000001`
- The letter `B` = `01000010`

So, a 1-gigabyte file is really 8,5 billion 1s and 0s all lined up in a row. This is called [binary](https://en.wikipedia.org/wiki/Binary_code) and is the basis of all digital storage.

**Pixels and Colors**

Images consist of pixels. Each pixel's color comes from the [RGB](https://en.wikipedia.org/wiki/RGB_color_model) (Red, Green, Blue) format. Each RGB channel ranges from 0 to 255, allowing for 256 values. This range is equivalent to 8 bits (2^8 = 256), so each channel can be represented by 1 byte.

Example: A red pixel is `(0xFF, 0x00, 0x00)` or in bits `11111111 00000000 00000000`.

**Hiding a File in an Image**

Hiding file inside a image is actually simpler than it sounds. All we need to do is:
1. Convert the file (in our case what we want to hide) to bits.
2. Replace _some_ bits in the image's pixels with the file's bits.

For example, if we take the first 2 bits from a file and replace them in a pixel's channel, a red pixel `(11111111 00000000 00000000)` can change to `(11111111 00000000 00000011)` without a visible difference.

Repeat this process for each pixel and every bit in the file, and voilà, the file is hidden in the image!

**Try it Yourself**

Check out the provided Python repository for an easy-to-understand implementation of this process.

# Usage

For running the program in the UI mode (simpler and easier to use but also less useful for developers) just run the following command:

```bash
python vangonography.py
```

For running the program in the CLI mode (more complicated but with a bit more functionalities) just run the following command:
```bash
python vangonography.py -cli
```
You can then use the following arguments along with it:
```console
usage: vangonography.py [-h] [-ood] [-l] [-cli] [-o OUTPUT_DIR] [-v] [--encrypt] [--decrypt] [--key KEY] [--json JSON_FILE] [--stealth] [-s] [-e] [-d] [-c COVER_IMAGE]
                        [-f HIDDEN_FILE]

Van Gonography is a steganography tool that hides files in images.

options:
  -h, --help            show this help message and exit

Optional arguments:
  -ood                  Open file after decoding from image (default: False)
  -l, --log             Log file for the program (default: False)
  -cli                  Run the program in CLI mode, this means there's not gonna be any menu (default: False)
  -o OUTPUT_DIR, --output OUTPUT_DIR
                        Output directory for the modified image or revealed file
  -v, --version         Show the version number and exit
  --encrypt             Encrypt the data before hiding it (default: False)
  --decrypt             Decrypt the data after revealing it (default: False)
  --key KEY             Key to decrypt the data (default: None)
  --json JSON_FILE      JSON file containing the arguments (default: None)
  --stealth             Hides the file in stealth mode (default: False)

Positional arguments (only used in CLI mode):
  -s, --show            Show the difference between two images (default: False)
  -e, --encode          Encode the file in the image (default: False)
  -d, --decode          Decode the file hidden in the image (default: False)
  -c COVER_IMAGE, --cover COVER_IMAGE
                        Image to be used for hiding or revealing, positional only when using decoding, encoding or differentiate
  -f HIDDEN_FILE, --file HIDDEN_FILE
                        File to be hidden
```
For example, if you want to hide a file called `secret.txt` inside an image called `image.png` and you want to save the modified image in a folder called `output` you would run the following command:
```bash
python vangonography.py -cli -e -c [Absolute path to your `image.png` cover image] -f [Absolute path to your `secret.txt` file] -o Output
```
This will create a directory called `Output` in the same directory as the program and inside it will be a file called `Cover_txt.png` which will be the modified image with the hidden file inside it. If you want to decode the file from the image you would run the following command:
```bash
python vangonography.py -cli -d -c [Absolute path (or not) to your `Cover_txt.png` cover image] -o Output
```
If you also want to create a log.log file with all the information about the program you can run the following command:
```bash
python vangonography.py -cli -d -c [Absolute path (or not) to your `Cover_txt.png` cover image] -o Output -l
```