#!/usr/bin/env python3
"""
Manual Review Tool for OCR Results
Helps reviewers quickly identify and correct OCR errors.
"""

import argparse
import re
import os
from pathlib import Path


def load_processed_file(file_path):
    """Load and parse a processed OCR file."""
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Parse sections
    sections = {}
    current_section = None
    current_content = []

    for line in content.split("\n"):
        if line.startswith("--- ") and line.endswith(" ---"):
            if current_section:
                sections[current_section] = "\n".join(current_content).strip()
            current_section = line[4:-4]  # Remove --- and ---
            current_content = []
        else:
            current_content.append(line)

    if current_section:
        sections[current_section] = "\n".join(current_content).strip()

    return sections


def highlight_suspicious_text(text):
    """Highlight potentially problematic text patterns."""
    highlighted = text

    # Highlight repeated characters
    highlighted = re.sub(r"(.)\1{3,}", r"**\1\1\1\1+**", highlighted)

    # Highlight missing spaces (lowercase + uppercase)
    highlighted = re.sub(r"([a-z])([A-Z])", r"\1**\1\2**\2", highlighted)

    # Highlight unusual character sequences
    highlighted = re.sub(r"[^\w\s]{3,}", r"***\g<0>***", highlighted)

    return highlighted


def generate_review_report(sections, output_path):
    """Generate a review report with highlighted issues."""
    report = []
    report.append("# OCR Review Report")
    report.append("=" * 50)

    if "TRANSCRIPTION" in sections:
        report.append("\n## Original Transcription")
        report.append(
            "**Legend:** ***unusual chars***, **missing space**, ****repeated chars****"
        )
        report.append("\n" + highlight_suspicious_text(sections["TRANSCRIPTION"]))

    if "TRANSLATION" in sections:
        report.append("\n## Spanish Translation")
        report.append(sections["TRANSLATION"])

    if "QUALITY ASSESSMENT" in sections:
        report.append("\n## Quality Assessment")
        report.append(sections["QUALITY ASSESSMENT"])

    if "AUTOMATED ANALYSIS" in sections:
        report.append("\n## Automated Analysis")
        report.append(sections["AUTOMATED ANALYSIS"])

    # Add review checklist
    report.append("\n## Review Checklist")
    report.append("- [ ] Check highlighted sections for errors")
    report.append("- [ ] Verify proper spacing between words")
    report.append("- [ ] Confirm special characters are correct")
    report.append("- [ ] Check for missing or garbled text")
    report.append("- [ ] Validate translation accuracy")
    report.append("- [ ] Review confidence score and issues")

    report.append("\n## Quick Corrections Needed")
    report.append("(Add corrections here)")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(report))

    print(f"Review report generated: {output_path}")


def main():
    parser = argparse.ArgumentParser(description="OCR Manual Review Tool")
    parser.add_argument("input_file", help="Path to processed OCR file")
    parser.add_argument("--review-report", "-r", help="Generate detailed review report")
    parser.add_argument(
        "--all", "-a", action="store_true", help="Generate review report"
    )

    args = parser.parse_args()

    if not os.path.exists(args.input_file):
        print(f"Error: File '{args.input_file}' not found.")
        return 1

    # Load and parse the file
    sections = load_processed_file(args.input_file)
    base_path = Path(args.input_file).stem

    # Generate review report (default behavior)
    if args.all or args.review_report:
        review_path = f"{base_path}_review.md"
        generate_review_report(sections, review_path)
    else:
        # If no specific option given, generate review report by default
        review_path = f"{base_path}_review.md"
        generate_review_report(sections, review_path)

    return 0


if __name__ == "__main__":
    exit(main())
