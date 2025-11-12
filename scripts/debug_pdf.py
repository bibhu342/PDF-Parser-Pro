# debug_pdf.py
import pdfplumber
from pathlib import Path
import json

pdf_path = Path("data/raw/mock_invoice_01.pdf")
if not pdf_path.exists():
    print("ERROR: PDF not found at", pdf_path)
    raise SystemExit(1)

with pdfplumber.open(pdf_path) as pdf:
    print(f"Opened: {pdf_path} | pages: {len(pdf.pages)}\n")
    for i, page in enumerate(pdf.pages, start=1):
        print("=== PAGE", i, "===")
        txt = page.extract_text()
        print("Text present? ->", bool(txt))
        # print a short text preview (first 800 chars)
        if txt:
            print("--- text preview ---")
            print(txt[:800].replace("\n", "\\n"))
            print("--- end preview ---")
        else:
            print("(no text extracted by pdfplumber)")

        # Show how many tables pdfplumber detects and some sample structure
        tables = page.extract_tables()
        print("tables detected:", len(tables))
        for ti, t in enumerate(tables, start=1):
            print(f" table {ti} rows:", len(t))
            # print header if present and first 2 rows
            if len(t) > 0:
                print("  header (first row):", t[0])
            if len(t) > 1:
                print("  sample row:", t[1])
        print("\n")
print("DEBUG DONE")
