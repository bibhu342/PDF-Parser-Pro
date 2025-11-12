# 📄 PDF-Parser-Pro

### A Python-powered PDF parsing and extraction tool — PDFs → CSV → Analytics-ready

---

## 📘 Project Overview

**PDF-Parser-Pro** is a production-ready Python tool that extracts structured data from business PDFs (invoices, statements, reports), normalizes tables and fields, and exports clean CSVs ready for analytics or downstream ML pipelines.

It is designed for freelancers and engineers who need repeatable, auditable parsing workflows with optional OCR support for scanned documents.

---

## 🎯 Objective

Automate extraction of tabular and key-value data from heterogeneous business PDFs, apply cleaning and validation rules, and output standardized CSV files suitable for analytics and ML.

---

## ⚙️ Tech Stack

* **Language:** Python 3.11+
* **Core libraries:** pdfplumber, pandas, pathlib, regex
* **Optional:** pytesseract, pdf2image (for OCR/scanned PDFs)
* **Dev tools:** Jupyter (notebooks/experiments), VS Code, GitHub

---

## 🧩 Functionality (MVP)

1. Read single or multiple PDF files from `data/raw/`.
2. Detect and extract tabular regions using `pdfplumber`.
3. Extract key-value pairs (invoice no, date, total) using regex heuristics.
4. Normalize column names and data types (dates, currency, numeric fields).
5. Apply validation rules (e.g., `total == sum(line_item_amounts)`) and flag mismatches.
6. Export cleaned CSVs to `data/extracted/` and a small audit log for each file.

---

## 📁 Repository Structure

```
PDF-Parser-Pro/
├── data/
│   ├── raw/          # input PDFs
│   └── extracted/    # parsed CSVs and audits
├── scripts/
│   └── parse_pdf_data.py
├── notebooks/
│   └── PDF_Parser_Pro_Dev.ipynb
├── tests/
│   └── sample_pdfs/  # small set of labeled PDFs for unit tests
├── README.md
├── requirements.txt
└── .gitignore
```

---

## 🛠 How to Use (MVP)

1. Clone repo:

```bash
git clone <repo-url>
cd PDF-Parser-Pro
```

2. Install deps:

```bash
python -m venv .venv
source .venv/bin/activate   # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
```

3. Place PDFs in `data/raw/`.
4. Run parser:

```bash
python scripts/parse_pdf_data.py --input data/raw --output data/extracted
```

5. Output: one CSV per PDF in `data/extracted/` plus `audit_<filename>.json` containing parsing metadata.

---

## ✅ Expected Output

* `data/extracted/<pdf_basename>.csv` — cleaned tabular data
* `data/extracted/audit_<pdf_basename>.json` — parsing summary (pages parsed, tables found, warnings)

---

## 🔧 Future Enhancements

* CLI arguments (file/glob support, verbosity, dry-run)
* OCR pipeline for scanned PDFs (`pytesseract` + `pdf2image`)
* Streamlit UI for drag-and-drop parsing & manual corrections
* Config-driven rules per client (mapping rules, column mappings)
* Unit tests and CI (GitHub Actions) with sample PDFs

---

## 🧾 Notes for Freelancing

* Provide sample PDFs and expected CSV schema in proposals.
* Offer a small manual review pass as part of the gig to handle edge-case layouts.
* Add a short guide in the repo explaining how to map client-specific invoice formats.

---

## 👨‍💻 Author

Bibhudendu Behera
Aspiring AI Engineer | Freelance Data Tools
Bangalore, India

---

*Created as the starting design doc for PDF-Parser-Pro — follow the repository checklist to convert this into a deployable tool.*
