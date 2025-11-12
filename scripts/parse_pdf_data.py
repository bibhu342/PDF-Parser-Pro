"""
parse_pdf_data.py
Author: Bibhudendu Behera
Description:
Extracts tabular and key-value data from PDFs and exports cleaned CSVs using pdfplumber + pandas.
"""

import pdfplumber
import pandas as pd
import re
import json
import os
from pathlib import Path
import argparse

# ---------------------------
# Paths
# ---------------------------
DEFAULT_INPUT_DIR = Path("data/raw")
DEFAULT_OUTPUT_DIR = Path("data/extracted")

# ---------------------------
# Utility Functions
# ---------------------------
def ocr_pdf_to_text(pdf_path: Path, page_number: int = 1, poppler_path: str = None, dpi: int = 300):
    """
    Convert a single PDF page to image(s) and run Tesseract OCR to return extracted text.
    - pdf_path: Path to PDF
    - page_number: 1-based page index
    - poppler_path: optional path to poppler bin (if not in PATH)
    - returns string of extracted text for that page (or empty string)
    """
    try:
        from pdf2image import convert_from_path
        import pytesseract
        kwargs = {"first_page": page_number, "last_page": page_number, "dpi": dpi}
        if poppler_path:
            kwargs["poppler_path"] = poppler_path
        pages = convert_from_path(str(pdf_path), **kwargs)
        if not pages:
            return ""
        img = pages[0]
        text = pytesseract.image_to_string(img)
        return text or ""
    except Exception:
        return ""

def extract_tables_from_pdf(pdf_path: Path):
    """Extract all tables from all pages of a PDF. Uses pdfplumber tables first,
       then a text-based fallback for pages where extract_tables() returns empty.
    """
    all_tables = []
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages, start=1):
            # try native table extraction
            tables = page.extract_tables()
            if tables:
                for table in tables:
                    df = pd.DataFrame(table[1:], columns=table[0])  # first row = header
                    df["page_number"] = i
                    all_tables.append(df)
                continue

            # fallback: try extracting a visually-aligned table from page text
            fallback_tables = extract_table_from_text_fallback(page)
            if fallback_tables:
                for df in fallback_tables:
                    df["page_number"] = i
                    all_tables.append(df)
    return all_tables


# --- START: fallback text-table parser ---
def extract_table_from_text_fallback(page, header_keywords=None):
    """
    Attempt to parse a visually-aligned table from the page's text.
    Returns a list with one DataFrame if successful, otherwise [].
    """
    import pandas as pd
    text = page.extract_text() or ""
    if not text:
        try:
            from pathlib import Path
            import os
            pdf_path = None
            if hasattr(page, "pdf") and hasattr(page.pdf, "stream") and getattr(page.pdf.stream, "name", None):
                pdf_path = Path(page.pdf.stream.name)
            elif os.environ.get("PDFPARSER_CURRENT_PDF"):
                pdf_path = Path(os.environ["PDFPARSER_CURRENT_PDF"])
            if pdf_path and pdf_path.exists():
                ocr_text = ocr_pdf_to_text(pdf_path, page.page_number)
                if ocr_text:
                    text = ocr_text
        except Exception:
            text = text
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    if not lines:
        return []

    # default header keywords (adjust later if needed)
    if header_keywords is None:
        header_keywords = ["description", "qty", "unit", "price", "line", "total"]

    # find header line index by matching keywords
    header_idx = None
    for i, ln in enumerate(lines):
        low = ln.lower()
        if all(any(k in part for part in low.split()) for k in ["description", "qty"]):
            header_idx = i
            break
        if "qty" in low and ("unit" in low or "line" in low):
            header_idx = i
            break

    if header_idx is None:
        return []

    header_line = lines[header_idx]
    cols = re.split(r"\s{2,}|\t", header_line)  # split on 2+ spaces or tabs
    if len(cols) == 1:
        cols = header_line.split()

    cols = [c.strip().lower().replace(" ", "_") for c in cols]

    data_rows = []
    for ln in lines[header_idx + 1 :]:
        if re.match(r"^total[:\s]", ln, flags=re.IGNORECASE):
            break
        parts = re.split(r"\s{2,}|\t", ln)
        if len(parts) == 1:
            parts = ln.split()
        if len(parts) > len(cols):
            extras = parts[: len(parts) - (len(cols) - 1)]
            rest = parts[len(parts) - (len(cols) - 1) :]
            parts = [" ".join(extras)] + rest
        if len(parts) < len(cols):
            parts = parts + [None] * (len(cols) - len(parts))
        data_rows.append([p.strip() if isinstance(p, str) else p for p in parts])

    if not data_rows:
        return []

    df = pd.DataFrame(data_rows, columns=cols)
    df = df.dropna(how="all").reset_index(drop=True)
    try:
        page_no = page.page_number
    except Exception:
        page_no = None
    if page_no is not None:
        df["page_number"] = page_no
    return [df]
# --- END: fallback text-table parser ---


def extract_key_values_from_text(pdf_path: Path):
    """Extract key-value metadata (invoice no, date, total) using regex."""
    patterns = {
        "invoice_no": r"(?:invoice|bill)\s*#?:?\s*([A-Za-z0-9-]+)",
        "date": r"date\s*[:\-]?\s*([0-9]{1,2}[\/\-][0-9]{1,2}[\/\-][0-9]{2,4})",
        "total": r"total\s*(?:amount)?\s*[:\-]?\s*\$?([0-9,]+\.?[0-9]*)"
    }

    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    extracted = {}
    for key, pattern in patterns.items():
        match = re.search(pattern, text, flags=re.IGNORECASE)
        extracted[key] = match.group(1).strip() if match else None
    return extracted


def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Basic cleaning for extracted tables."""
    df.columns = [str(c).strip().lower().replace(" ", "_") for c in df.columns]
    df = df.dropna(how="all").reset_index(drop=True)
    return df


def normalize_numeric_columns(df: pd.DataFrame):
    """
    Convert common currency/number-looking columns to numeric.
    - Handles split header cases like ['line','total'] or ['unit','price'].
    - Returns normalized df.
    """
    cols = list(df.columns)
    lc_cols = [str(c).lower().strip() for c in cols]

    # First handle column merging for split headers
    i = 0
    while i < len(cols) - 1:
        a = lc_cols[i]
        b = lc_cols[i + 1]
        
        # Handle "line" + "total" case - merge the values
        if ("line" in a) and ("total" in b):
            # Merge the two columns by combining non-null values
            col1_values = df[cols[i]].fillna('')
            col2_values = df[cols[i + 1]].fillna('')
            combined_values = []
            for v1, v2 in zip(col1_values, col2_values):
                # Take the first non-empty value
                if str(v1).strip():
                    combined_values.append(v1)
                elif str(v2).strip():
                    combined_values.append(v2)
                else:
                    combined_values.append('')
            df['line_total'] = combined_values
            df = df.drop(columns=[cols[i], cols[i + 1]])
            # Update cols list
            cols = list(df.columns)
            lc_cols = [str(c).lower().strip() for c in cols]
            continue
            
        # Handle "unit" + "price" case - merge the values
        if ("unit" in a) and ("price" in b):
            col1_values = df[cols[i]].fillna('')
            col2_values = df[cols[i + 1]].fillna('')
            combined_values = []
            for v1, v2 in zip(col1_values, col2_values):
                # Take the first non-empty value
                if str(v1).strip():
                    combined_values.append(v1)
                elif str(v2).strip():
                    combined_values.append(v2)
                else:
                    combined_values.append('')
            df['unit_price'] = combined_values
            df = df.drop(columns=[cols[i], cols[i + 1]])
            # Update cols list
            cols = list(df.columns)
            lc_cols = [str(c).lower().strip() for c in cols]
            continue
        i += 1

    # Now handle individual column renaming
    col_map = {}
    for c in cols:
        lc = str(c).lower().strip()
        if "line" in lc and "total" in lc:
            col_map[c] = "line_total"
        elif "unit" in lc and "price" in lc:
            col_map[c] = "unit_price"
        elif lc in ("qty", "quantity"):
            col_map[c] = "quantity"
        elif lc == "price":  # standalone price column should become unit_price
            col_map[c] = "unit_price"
        elif lc == "total":  # standalone total column should become line_total
            col_map[c] = "line_total"
        elif "description" in lc:
            col_map[c] = "description"

    if col_map:
        df = df.rename(columns=col_map)

    # robust per-cell numeric parser
    def to_number(cell):
        # handle list/tuple
        if isinstance(cell, (list, tuple)):
            for item in cell:
                if item is None:
                    continue
                s = str(item).strip()
                if s.lower() not in ("", "nan", "none"):
                    cell = item
                    break
            else:
                return None

        # handle pandas Series-like by trying to extract first element
        if hasattr(cell, "__len__") and not isinstance(cell, (str, bytes)):
            try:
                # handle pandas Series with iloc to avoid FutureWarning
                if hasattr(cell, 'iloc'):
                    # It's a pandas Series, use iloc[0] to get first element
                    if len(cell) > 0:
                        cell = cell.iloc[0]
                    else:
                        return None
                else:
                    # convert to list and pick first non-empty
                    lst = list(cell)
                    for item in lst:
                        if item is None:
                            continue
                        s = str(item).strip()
                        if s.lower() not in ("", "nan", "none"):
                            cell = item
                            break
                    else:
                        return None
            except Exception:
                cell = str(cell)

        # now cell should be scalar-ish
        try:
            if pd.isna(cell):
                return None
        except Exception:
            pass

        s = str(cell).strip()
        if s.lower() in ("", "nan", "none"):
            return None

        s = s.replace(",", "").replace("$", "")
        s = re.sub(r"[^\d.\-]", "", s)
        if s in ("", "-", "."):
            return None
        try:
            return float(s)
        except Exception:
            return None

    # apply per-column conversions (use apply to keep it per-cell)
    if "quantity" in df.columns:
        df["quantity"] = df["quantity"].apply(to_number)

    if "unit_price" in df.columns:
        df["unit_price"] = df["unit_price"].apply(to_number)

    if "line_total" in df.columns:
        df["line_total"] = df["line_total"].apply(to_number)

    # If line_total missing but quantity & unit_price present, compute it
    if "line_total" not in df.columns and {"quantity", "unit_price"}.issubset(df.columns):
        # ensure numeric
        df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")
        df["unit_price"] = pd.to_numeric(df["unit_price"], errors="coerce")
        df["line_total"] = df["quantity"] * df["unit_price"]

    # final: coerce to numeric dtypes safely using per-cell parsing only
    for c in ["quantity", "unit_price", "line_total"]:
        if c in df.columns:
            try:
                # apply the robust per-cell parser defined above (to_number)
                df[c] = df[c].apply(to_number)
                # ensure dtype is numeric where possible (this operates on the Series returned by apply)
                df[c] = pd.to_numeric(df[c], errors="coerce")
            except Exception:
                # last-resort per-cell string-clean then numeric coercion
                def safe_cell_to_num(cell):
                    try:
                        return to_number(cell)
                    except Exception:
                        try:
                            # try to coerce by stringifying nested objects carefully
                            if isinstance(cell, (list, tuple)):
                                # pick first non-empty element
                                for el in cell:
                                    if el is not None and str(el).strip() not in ("", "nan"):
                                        cell = el
                                        break
                                else:
                                    return None
                            if hasattr(cell, "__len__") and not isinstance(cell, (str, bytes)):
                                # try to take first element of sequence-like
                                try:
                                    # handle pandas Series with iloc to avoid FutureWarning
                                    if hasattr(cell, 'iloc'):
                                        cell = cell.iloc[0] if len(cell) > 0 else ""
                                    else:
                                        lst = list(cell)
                                        cell = lst[0] if len(lst) > 0 else ""
                                except Exception:
                                    cell = str(cell)
                            s = str(cell)
                            s = re.sub(r"[^\d.\-]", "", s)
                            return float(s) if s not in ("", "-", ".") else None
                        except Exception:
                            return None
                df[c] = df[c].apply(safe_cell_to_num)


    return df


def parse_single_pdf(pdf_path: Path, output_dir: Path):
    """Parse a single PDF and export results."""
    print(f"🔍 Parsing: {pdf_path.name}")
    audit = {"file": pdf_path.name, "pages": 0, "tables_found": 0, "warnings": []}

    # Extract tables
    tables = extract_tables_from_pdf(pdf_path)
    if not tables:
        audit["warnings"].append("No tables detected.")
        return audit

    # Combine tables
    combined_df = pd.concat([clean_dataframe(df) for df in tables], ignore_index=True)

    # Normalize numeric columns & compute line totals
    combined_df = normalize_numeric_columns(combined_df)

    audit["pages"] = combined_df["page_number"].nunique()
    audit["tables_found"] = len(tables)

    # Extract metadata
    metadata = extract_key_values_from_text(pdf_path)
    audit.update(metadata)

    # Validate invoice total if possible (robust parsing)
    invoice_total = None
    raw_total = metadata.get("total")
    if raw_total:
        s = str(raw_total).strip().replace(",", "").replace("$", "")
        s = re.sub(r"[^\d.\-]", "", s)
        try:
            invoice_total = float(s) if s not in ("", "-", ".") else None
        except Exception:
            invoice_total = None

    # compute line_sum: prefer explicit line_total column, else compute from qty*unit_price
    line_sum = None
    if "line_total" in combined_df.columns:
        try:
            line_total_series = combined_df["line_total"].dropna()
            if not line_total_series.empty:
                result = line_total_series.astype(float).sum()
                line_sum = float(result) if not pd.isna(result) else None
        except Exception:
            try:
                line_total_series = pd.to_numeric(combined_df["line_total"], errors="coerce").dropna()
                if not line_total_series.empty:
                    result = line_total_series.sum()
                    line_sum = float(result) if not pd.isna(result) else None
            except Exception:
                pass

    if (line_sum is None) and {"quantity", "unit_price"}.issubset(combined_df.columns):
        tmp_qty = pd.to_numeric(combined_df["quantity"], errors="coerce")
        tmp_up = pd.to_numeric(combined_df["unit_price"], errors="coerce")
        prod = (tmp_qty * tmp_up).dropna()
        if not prod.empty:
            result = prod.sum()
            line_sum = float(result) if not pd.isna(result) else None

    # record validation results in audit
    if invoice_total is not None and line_sum is not None:
        match = abs(invoice_total - line_sum) < 0.01  # tolerance
        audit["invoice_total_matches"] = bool(match)
        audit["line_sum"] = round(float(line_sum), 2)
        if not match:
            audit["mismatch_amount"] = round(float(invoice_total - line_sum), 2)
            audit["warnings"].append("Invoice total does not match sum of line totals.")
    else:
        audit["invoice_total_matches"] = None
        audit["line_sum"] = (round(float(line_sum), 2) if line_sum is not None and not pd.isna(line_sum) else None)

    # Export results
    output_dir.mkdir(parents=True, exist_ok=True)
    csv_path = output_dir / f"{pdf_path.stem}.csv"
    json_path = output_dir / f"audit_{pdf_path.stem}.json"

    combined_df.to_csv(csv_path, index=False)
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(audit, f, indent=4)

    print(f"✅ Exported: {csv_path.name} | {json_path.name}")
    return audit


def parse_all_pdfs(input_dir: Path, output_dir: Path):
    """Parse all PDFs from the input directory."""
    pdf_files = list(input_dir.glob("*.pdf"))
    if not pdf_files:
        print("⚠️ No PDF files found in input directory.")
        return
    for pdf_path in pdf_files:
        parse_single_pdf(pdf_path, output_dir)


# ---------------------------
# CLI Entry Point
# ---------------------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Parse PDFs into structured CSVs.")
    parser.add_argument("--input", type=str, default=str(DEFAULT_INPUT_DIR), help="Input directory containing PDFs")
    parser.add_argument("--output", type=str, default=str(DEFAULT_OUTPUT_DIR), help="Output directory for extracted CSVs")
    args = parser.parse_args()

    parse_all_pdfs(Path(args.input), Path(args.output))
