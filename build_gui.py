import os

import PyInstaller.__main__

# Build the GUI executable
PyInstaller.__main__.run(
    [
        "gui.py",
        "--onefile",  # Single executable file
        "--windowed",  # No console window (for GUI apps)
        "--name=OCR_GUI",  # Name of the executable
        "--add-data=processor.py:.",
        "--add-data=rasterize.py:.",
        "--add-data=review_tool.py:.",
        "--hidden-import=google.generativeai",
        "--hidden-import=dotenv",
        "--hidden-import=pdf2image",
        "--hidden-import=PIL",
        "--hidden-import=reportlab",
    ]
)

print("Build complete. Check dist/ folder for the executable.")
