# OCR PDF Processor

A cross-platform GUI application for processing PDF files with OCR using Google Gemini API. Extracts text from PDFs, translates to Spanish, and provides quality analysis.

## Features

- **GUI Interface**: User-friendly interface for Windows, Linux, and MacOS
- **OCR Processing**: Uses Google Gemini for accurate text extraction
- **Translation**: Automatic translation to Spanish
- **Quality Analysis**: Confidence scoring and anomaly detection
- **Rasterization**: Option to simulate scanned documents
- **Batch Processing**: CLI support for multiple files

## Installation

### Prerequisites

- Python 3.8+
- Google Gemini API key (set in `.env` file)

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Environment Setup

Create a `.env` file in the project root:

```
GEMINI_API_KEY=your_api_key_here
```

## Usage

### GUI Application

Run the graphical interface:

```bash
python gui.py
```

Or use the standalone executable in `dist/OCR_GUI` (after building).

#### GUI Instructions

1. Click "Browse" to select input PDF file
2. Optionally set output file path (defaults to `ocr-{filename}.txt` in input directory)
3. Check "Rasterize PDF" to simulate scanned document (adjust DPI if needed)
4. Click "Process PDF" to start processing
5. View progress and results in the log area

### Command Line Interface

Process a single PDF:

```bash
python main.py input.pdf
```

With custom output:

```bash
python main.py input.pdf --output output.txt
```

### Rasterization

Convert PDF to simulated scanned document:

```bash
python rasterize.py input.pdf --dpi 200
```

### Review Tool

Generate detailed review report for processed files:

```bash
python review_tool.py processed_file.txt
```

## Building Executable

To create a standalone executable:

```bash
python build_gui.py
```

The executable will be in `dist/OCR_GUI`.

## Testing

To verify the export functionality (Word/PDF generation), you can run the included test script:

```bash
python test_export.py
```

This will generate sample files in the `test_outputs/` directory.

## Project Structure

- `gui.py`: Graphical user interface
- `main.py`: CLI entry point
- `processor.py`: Core OCR and translation logic
- `rasterize.py`: PDF rasterization utilities
- `review_tool.py`: Quality review and reporting
- `build_gui.py`: PyInstaller build script

## API Key Setup

1. Get a Google Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Add it to `.env` file as `GEMINI_API_KEY=your_key`

## Troubleshooting

- Ensure API key is valid and has quota
- For GUI issues on Linux, install `python3-tk`: `sudo apt-get install python3-tk`
- Check `.env` file is in project root and properly formatted

