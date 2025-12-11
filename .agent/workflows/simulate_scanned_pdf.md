---
description: Simulate scanned PDFs by rasterizing text-based PDFs into images.
---

This workflow converts a "perfect" digital PDF into a pixel-based image PDF, simulating a scanned document. This is useful for testing OCR capabilities.

# Prerequisites

- The project virtual environment must be active (`source venv/bin/activate`)
- `poppler-utils` must be installed on the system (already verified).

# Steps

1.  **Run the rasterization script**

    Use the `rasterize.py` script to process your PDF. You can specify the DPI (default is 200).

    ```bash
    # Syntax: python rasterize.py <input_pdf> [--output <output_pdf>] [--dpi <dpi>]
    
    # Example:
    python rasterize.py input/document.pdf --output input/document_scanned.pdf --dpi 200
    ```

2.  **Verify the output**

    Open the generated PDF. You should not be able to select the text with your cursor, confirming it is an image.

3.  **Run the OCR tool**

    Now you can use this simulated scan with the main OCR tool:

    ```bash
    python main.py input/document_scanned.pdf
    ```
