<!-- Build & Live badges -->
[![Build & Parser Check](https://github.com/bibhu342/PDF-Parser-Pro/actions/workflows/ci.yml/badge.svg)](https://github.com/bibhu342/PDF-Parser-Pro/actions)
[![Live Demo](https://img.shields.io/website?down_message=offline&label=live&up_message=online&url=https://pdf-parser-pro-bibhu342.streamlit.app)](https://pdf-parser-pro-bibhu342.streamlit.app/)

# PDF-Parser-Pro

**Live Demo:** [https://pdf-parser-pro-bibhu342.streamlit.app/](https://pdf-parser-pro-bibhu342.streamlit.app/) ← *Try it instantly with the demo PDF*

---

## 🧾 Overview

**PDF-Parser-Pro** is an AI-powered Python tool that extracts structured tables and key fields from business PDFs (invoices, statements, reports). It handles both text-based and scanned PDFs using OCR, outputting clean CSVs and audit JSONs for transparency and downstream analytics.

Built with `pdfplumber`, `pytesseract`, and `pandas`, this tool is designed for freelancers, data engineers, and businesses who need repeatable, auditable PDF data extraction workflows.

---

## ⚙️ Features

- **Text + OCR Extraction** — Uses `pdfplumber` for text-based PDFs and `pdf2image` + `pytesseract` for scanned documents
- **Intelligent Table Detection** — Automatic table extraction with fallback text-based parsing
- **Normalized Columns** — Standardizes headers to `unit_price`, `quantity`, `line_total`, etc.
- **Invoice Total Validation** — Compares line-item sum vs. declared total and flags mismatches
- **Streamlit UI** with:
  - Drag-and-drop file uploader
  - OCR toggle for scanned PDFs
  - One-click demo button with sample invoice
  - CSV + audit JSON downloads
- **Audit JSON** — Provides transparency (pages parsed, tables found, warnings, validation results)
- **Professional Branding** — Custom UI with sidebar, footer, and green-themed design

---

## 🚀 Live Demo (One-Click)

1. Visit: **[https://pdf-parser-pro-bibhu342.streamlit.app/](https://pdf-parser-pro-bibhu342.streamlit.app/)**
2. Click **"Use demo invoice (sample)"** button
3. View extracted data and audit summary instantly
4. Download CSV or audit JSON with one click

---

## � Local Setup

```powershell
# Clone the repository
git clone https://github.com/bibhu342/PDF-Parser-Pro.git
cd PDF-Parser-Pro

# Create and activate virtual environment
python -m venv .venv
.\.venv\Scripts\Activate  # Windows
```

**The app will open in your browser at `http://localhost:8501`**

### OCR Setup (Optional - for scanned PDFs)

For scanned PDF support, install Tesseract OCR and Poppler:

```powershell
# Install Tesseract OCR
winget install --id UB-Mannheim.TesseractOCR

# Run the setup script to configure OCR dependencies
python setup_ocr_dependencies.py
```

---

## 🧩 File Structure

```
PDF-Parser-Pro/
├── app.py                          # Streamlit UI
├── scripts/
│   ├── parse_pdf_data.py          # Core parser (OCR fallback, normalization, validation)
│   ├── ocr_verify.py              # OCR verification script
│   └── generate_mock_invoice.py   # Demo invoice generator
├── data/
│   ├── raw/                       # Sample input PDFs
│   └── extracted/                 # Output CSVs + audit JSONs
├── notebooks/                     # Development/testing notebooks
├── tests/
│   └── sample_pdfs/               # Test PDFs
├── requirements.txt
├── setup_ocr_dependencies.py      # OCR setup helper
└── README.md
```

---

## 🔧 Command-Line Usage

For batch processing or automation:

```powershell
# Parse all PDFs in a directory
python scripts\parse_pdf_data.py --input data/raw --output data/extracted

# Verify OCR setup
python scripts\ocr_verify.py
```

**Output:**
- `data/extracted/<pdf_basename>.csv` — Cleaned tabular data
- `data/extracted/audit_<pdf_basename>.json` — Parsing summary (pages parsed, tables found, warnings, validation results)

---

## ☁️ Deployment (Streamlit Cloud)

1. Push latest code to GitHub
2. Create an app at [https://share.streamlit.io/](https://share.streamlit.io/)
3. Set `app.py` as the entry point
4. **Done** — live URL auto-syncs on new commits

---

## 💼 Freelance Usage Tips

- **Demo the app live** to clients to showcase automation ability
- **Offer custom parsing** for specific invoice formats or multilingual PDFs
- **Attach sample results** — one invoice + result screenshot in proposals
- **Emphasize accuracy** — data validation, audit logging, and error handling
- **Highlight scalability** — batch processing, API integration potential
- **Show ROI** — hours saved vs. manual data entry costs

---

## 📊 Sample Output

**Input:** Business invoice PDF (text or scanned)

**Output CSV:**
```csv
description,quantity,unit_price,line_total
Widget A,2,1000.00,2000.00
Widget B,1,500.00,500.00
Service C,3,250.00,750.00
```

**Audit JSON:**
```json
{
    "file": "invoice_001.pdf",
    "pages": 1,
    "tables_found": 1,
    "invoice_no": "INV-2025-001",
    "date": "11/11/2025",
    "total": "3,250.00",
    "invoice_total_matches": true,
    "line_sum": 3250.0,
    "warnings": []
}
```

---

## 🎯 Key Capabilities

✅ **Text-based PDFs** — Native table extraction with pdfplumber  
✅ **Scanned PDFs** — OCR fallback with Tesseract  
✅ **Data Normalization** — Standardized column names and types  
✅ **Validation** — Invoice total vs. line-item sum matching  
✅ **Audit Trail** — Complete parsing metadata for each document  
✅ **Professional UI** — Streamlit app with branding and UX polish  
✅ **Batch Processing** — CLI support for automated workflows  

---

## 👨‍💻 Author

**Bibhudendu Behera**  
Aspiring AI Engineer & Freelance Data Tools Developer  
📍 Bangalore, India  
🔗 [GitHub](https://github.com/bibhu342)  
💼 [LinkedIn](https://www.linkedin.com/in/bibhudendu-behera)

---

## 📄 License

MIT License - feel free to use this project for your freelance work or commercial applications.

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/bibhu342/PDF-Parser-Pro/issues).

---

**⭐ Star this repo if you find it useful for your freelance projects!**
Bangalore, India

---

*Created as the starting design doc for PDF-Parser-Pro — follow the repository checklist to convert this into a deployable tool.*
