#!/usr/bin/env python3

"""
get_image_exif.py - A command-line tool to extract and display EXIF metadata from image files.

Requires the Pillow (PIL) library. Install it using: pip install Pillow
"""

from PIL import Image
from PIL.ExifTags import TAGS
import argparse
import sys
import io

# ASCII Banner
BANNER = """
  _ __   ___   ___  _ __
 | '_ \ / _ \ / _ \| '_ \\
 | |_) | (_) | (_) | | | |
 | .__/ \___/ \___/|_| |_|
 |_|
"""

def get_exif_data(image_path):
    """Retrieves EXIF data from an image file.

    Args:
        image_path (str): The path to the image file.

    Returns:
        dict or None: A dictionary containing EXIF tags and their values,
                     or None if no EXIF data is found or the file is not a valid image.
    """
    try:
        img = Image.open(image_path)
        exif_data = img.info.get('exif')
        if exif_data:
            return exif_data
        else:
            return None
    except FileNotFoundError:
        print(f"Error: Image file not found at '{image_path}'", file=sys.stderr)
        return None
    except Exception as e:
        print(f"Error: Could not open or process image file '{image_path}': {e}", file=sys.stderr)
        return None

def decode_exif_data(exif_data):
    """Decodes raw EXIF data into human-readable tag names and values.

    Args:
        exif_data (bytes): The raw EXIF data.

    Returns:
        dict: A dictionary where keys are human-readable EXIF tag names
              and values are their corresponding decoded values.
    """
    decoded_exif = {}
    try:
        for tag, value in Image.open(io.BytesIO(exif_data))._getexif().items():
            tag_name = TAGS.get(tag, tag)
            decoded_exif[tag_name] = value
    except AttributeError:
        # _getexif() might return None for some images or if no EXIF
        return {}
    except Exception as e:
        print(f"Error decoding EXIF data: {e}", file=sys.stderr)
        return {}
    return decoded_exif

def main():
    parser = argparse.ArgumentParser(description="Extract and display EXIF metadata from image files.")
    parser.add_argument("image_path", help="The path to the image file.")
    parser.add_argument("-r", "--raw", action="store_true", help="Display raw EXIF byte data instead of decoded values.")
    args = parser.parse_args()

    print(BANNER)  # Print the banner

    exif_bytes = get_exif_data(args.image_path)

    if exif_bytes is not None:
        if args.raw:
            print("Raw EXIF Data:")
            print(exif_bytes)
        else:
            decoded_exif = decode_exif_data(exif_bytes)
            if decoded_exif:
                print(f"EXIF Metadata for '{args.image_path}':")
                for tag, value in sorted(decoded_exif.items()):
                    print(f"{tag}: {value}")
            else:
                print(f"No readable EXIF metadata found in '{args.image_path}'.")
    else:
        # get_exif_data already prints error messages
        pass

if __name__ == "__main__":
    main()