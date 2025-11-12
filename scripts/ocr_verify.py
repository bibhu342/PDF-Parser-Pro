"""
OCR Verification Script
Verifies that pdf2image and pytesseract are working correctly
"""

import os
import sys
from pathlib import Path

# Configure paths for Windows
TESSERACT_PATH = r"C:/Program Files/Tesseract-OCR/tesseract.exe"
POPPLER_PATH = r"C:\poppler\poppler-23.08.0\Library\bin"

# Add poppler to PATH
if POPPLER_PATH not in os.environ.get("PATH", ""):
    os.environ["PATH"] = POPPLER_PATH + os.pathsep + os.environ.get("PATH", "")

# Configure pytesseract
import pytesseract
pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH


import pdf2image
import pytesseract
from pdf2image import convert_from_path
from pathlib import Path
import sys

print("pdf2image module loaded OK")
try:
    print("pytesseract", pytesseract.get_tesseract_version())
except Exception as e:
    print("pytesseract (error):", repr(e))


pdf_path = Path("data/raw/mock_invoice_01.pdf")
if not pdf_path.exists():
    print("ERROR: test PDF not found at", pdf_path)
    sys.exit(1)

try:
    pages = convert_from_path(str(pdf_path), first_page=1, last_page=1)
    print("pdf2image -> convert_from_path OK, pages:", len(pages))
except Exception as e:
    print("pdf2image convert error:", repr(e))

# Try a quick OCR on the first page (if conversion succeeded)
if 'pages' in locals() and pages:
    try:
        txt = pytesseract.image_to_string(pages[0])
        print("pytesseract -> OCR extracted length:", len(txt))
        print("pytesseract -> OCR sample:", repr(txt[:200]))
    except Exception as e:
        print("pytesseract OCR error:", repr(e))
