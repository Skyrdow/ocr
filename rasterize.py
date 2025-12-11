import argparse
import os

from pdf2image import convert_from_path
from PIL import Image


def rasterize_pdf(input_path, output_path=None, dpi=200):
    """
    Converts a PDF to images (rasterizes) and saves them back as a PDF.
    This simulates a scanned document, removing selectable text.
    """
    if not output_path:
        base, ext = os.path.splitext(input_path)
        output_path = f"{base}_scanned{ext}"

    print(f"Rasterizing '{input_path}' at {dpi} DPI...")

    # Convert PDF to list of images
    try:
        images = convert_from_path(input_path, dpi=dpi)
    except Exception as e:
        print(f"Error converting PDF: {e}")
        return

    if not images:
        print("No images generated.")
        return

    print(f"Converted {len(images)} pages. Saving to '{output_path}'...")

    # Save the first image and append the rest
    # PDF saving in Pillow requires all images to be RGB
    images[0].save(
        output_path, "PDF", resolution=100.0, save_all=True, append_images=images[1:]
    )

    print(f"Done! Saved to '{output_path}'")


def main():
    parser = argparse.ArgumentParser(
        description="Convert a PDF to images and back to PDF (simulate scan)."
    )
    parser.add_argument("input_pdf", help="Path to the input PDF.")
    parser.add_argument("--output", "-o", help="Path to the output PDF.")
    parser.add_argument(
        "--dpi", type=int, default=200, help="DPI for rasterization (default: 200)."
    )

    args = parser.parse_args()

    if not os.path.exists(args.input_pdf):
        print(f"Error: File '{args.input_pdf}' not found.")
        return

    rasterize_pdf(args.input_pdf, args.output, args.dpi)


if __name__ == "__main__":
    main()
