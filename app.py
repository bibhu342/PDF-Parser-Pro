import streamlit as st
import pandas as pd
import tempfile
from pathlib import Path
import json
import io
import os
from scripts.parse_pdf_data import parse_single_pdf

st.set_page_config(page_title="PDF-Parser-Pro", layout="wide")

st.title("📄 PDF-Parser-Pro")
st.write("Upload your business PDF (invoice, statement, report) and extract structured tables into clean CSVs.")

uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])

if uploaded_file:
    # Save uploaded file to a temporary path
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(uploaded_file.getvalue())
        tmp_path = Path(tmp_file.name)

    enable_ocr = st.checkbox("Enable OCR (for scanned / image-only PDFs)", value=False)

    # Define output folder inside temp dir
    output_dir = Path(tempfile.mkdtemp())

    st.info("🔍 Parsing PDF, please wait...")

    try:
        if enable_ocr:
            os.environ["PDFPARSER_CURRENT_PDF"] = str(tmp_path)
        
        audit = parse_single_pdf(tmp_path, output_dir)
        csv_files = list(output_dir.glob("*.csv"))
        csv_path = csv_files[0] if csv_files else None

        if csv_path and csv_path.exists():
            df = pd.read_csv(csv_path)
            st.success("✅ Parsing complete!")

            st.subheader("📊 Extracted Data")
            st.dataframe(df, width='stretch')

            # Show audit details
            st.subheader("🧾 Audit Summary")
            st.json(audit)

            # Download buttons
            with open(csv_path, "rb") as f:
                st.download_button("⬇️ Download CSV", f, file_name="parsed_data.csv")

            audit_json = json.dumps(audit, indent=4)
            st.download_button(
                "⬇️ Download Audit JSON",
                io.BytesIO(audit_json.encode()),
                file_name="audit_summary.json",
            )
        else:
            st.error("No tables found or CSV could not be generated.")

    except Exception as e:
        st.error(f"❌ Error while parsing: {e}")
    finally:
        os.environ.pop("PDFPARSER_CURRENT_PDF", None)
        if tmp_path.exists():
            tmp_path.unlink(missing_ok=True)
else:
    st.info("👆 Upload a PDF file to start parsing.")
