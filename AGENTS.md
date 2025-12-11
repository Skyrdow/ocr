# AGENTS.md

## Build/Lint/Test Commands

### Installation
```bash
pip install -r requirements.txt
```

### Running the Application
```bash
# Process a PDF file (generates output.txt with confidence scoring)
python main.py input.pdf

# Process with custom output
python main.py input.pdf --output output.txt

# Simulate scanned PDF (rasterize)
python rasterize.py input.pdf --dpi 200

# Generate review report for manual checking
python review_tool.py output.txt
```

### Testing
No formal test suite exists. Run manual tests:
```bash
# Test OCR processing
python main.py test.pdf

# Test rasterization
python rasterize.py test.pdf

# Review OCR results with automated analysis
python review_tool.py test_processed.txt
```

### Error Detection & Manual Review
The system now includes automated error detection:
- **Confidence scoring**: 0-100% based on text quality analysis
- **Anomaly detection**: Identifies garbled text, missing spaces, unusual characters
- **Manual review tools**: Generate reports with highlighted issues

```bash
# Generate detailed review report with highlighted issues
python review_tool.py processed_file.txt
```

### Linting & Code Quality
```bash
# Install recommended tools
pip install flake8 black isort mypy

# Lint code
flake8 *.py

# Format code
black *.py

# Sort imports
isort *.py

# Type check
mypy *.py
```

## Code Style Guidelines

### Imports
- Use absolute imports
- Group imports: standard library, third-party, local
- Use `from dotenv import load_dotenv` for environment loading

### Naming Conventions
- Functions: `snake_case` (e.g., `transcribe_and_translate`)
- Variables: `snake_case` (e.g., `input_path`, `output_path`)
- Constants: `UPPER_CASE` (e.g., `API_KEY`)

### Error Handling
- Use try/except blocks for API calls and file operations
- Raise `ValueError` for missing required environment variables
- Print error messages to stderr and exit with code 1

### Types & Documentation
- Use type hints where beneficial
- Add docstrings for public functions explaining purpose and parameters
- Keep functions focused on single responsibilities

### File Structure
- `main.py`: CLI entry point and argument parsing
- `processor.py`: Core OCR and translation logic
- `rasterize.py`: PDF rasterization utilities
- Keep configuration in `.env` files

### Security
- Never commit API keys or secrets
- Load sensitive data from environment variables only
- Use `.env` files for local development (add `.env` to `.gitignore`)