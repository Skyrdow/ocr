import argparse
import os
import sys

from processor import transcribe_and_translate


def main():
    parser = argparse.ArgumentParser(
        description="Transcribe and translate PDF files using Gemini API."
    )
    parser.add_argument("input_pdf", help="Path to the input PDF file.")
    parser.add_argument("--output", "-o", help="Path to save the output text file.")

    args = parser.parse_args()

    input_path = args.input_pdf
    if not os.path.exists(input_path):
        print(f"Error: Input file '{input_path}' not found.")
        sys.exit(1)

    print(f"Processing '{input_path}'...")
    try:
        result = transcribe_and_translate(input_path)

        if args.output:
            output_path = args.output
        else:
            # Default output filename
            base_name = os.path.splitext(os.path.basename(input_path))[0]
            output_path = f"{base_name}_processed.txt"

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(result)

        print(f"Successfully processed PDF. Output saved to '{output_path}'.")

    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
