import streamlit as st
import pandas as pd
import tempfile
from pathlib import Path
import json
import io
import os
from scripts.parse_pdf_data import parse_single_pdf

st.set_page_config(
    page_title="PDF-Parser-Pro",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown(
    "<link rel='shortcut icon' href='favicon.png'>",
    unsafe_allow_html=True
)

# st.image("banner.png", width='stretch')  # Uncomment when banner.png is available
st.markdown(
    "<h2 style='text-align:center; color:#4CAF50;'>AI-Powered PDF Parser — Extract. Clean. Automate.</h2>",
    unsafe_allow_html=True
)
st.write("---")

with st.sidebar:
    st.image("banner.png", width='stretch')  # Uncomment when banner.png is available
    st.markdown(
        "<h3 style='text-align:center; color:#4CAF50;'>PDF-Parser-Pro</h3>",
        unsafe_allow_html=True
    )
    st.markdown("Extract • Clean • Automate 📄")
    st.write("---")
    st.markdown("### Settings")
    st.markdown("- Upload business PDFs (invoices, reports)")
    st.markdown("- Toggle OCR for scanned files")
    st.markdown("- Download clean CSVs for analytics")
    st.write("---")
    st.markdown(
        "<div style='text-align:center; font-size:0.9em; color:gray;'>"
        "Built by <b>Bibhudendu Behera</b><br>"
        "<a href='https://github.com/bibhu342/PDF-Parser-Pro' target='_blank'>GitHub Repo</a>"
        "</div>",
        unsafe_allow_html=True
    )

st.title("📄 PDF-Parser-Pro")
st.write("Upload your business PDF (invoice, statement, report) and extract structured tables into clean CSVs.")

# ---------- Demo PDF quick-test button ----------
st.markdown("### Try a demo PDF")
if st.button("Use demo invoice (sample)"):
    demo_src = Path("data/raw/mock_invoice_01.pdf")
    if not demo_src.exists():
        st.error("Demo PDF not found in data/raw/. Please add mock_invoice_01.pdf or update demo_src.")
    else:
        # create a small temp output dir and parse demo file
        output_dir = Path(tempfile.mkdtemp())
        st.info("🔍 Parsing demo PDF — please wait...")
        try:
            audit = parse_single_pdf(demo_src, output_dir)
            csv_files = list(output_dir.glob("*.csv"))
            csv_path = csv_files[0] if csv_files else None

            if csv_path and csv_path.exists():
                df = pd.read_csv(csv_path)
                st.success("✅ Demo parsing complete!")

                st.subheader("📊 Extracted Data (demo)")
                st.dataframe(df, width='stretch')

                st.subheader("🧾 Audit Summary (demo)")
                st.json(audit)

                with open(csv_path, "rb") as f:
                    st.download_button("⬇️ Download Demo CSV", f, file_name="demo_parsed.csv")

                audit_json = json.dumps(audit, indent=4)
                st.download_button(
                    "⬇️ Download Demo Audit JSON",
                    io.BytesIO(audit_json.encode()),
                    file_name="demo_audit.json",
                )
            else:
                st.error("Demo parsing completed but no CSV was produced.")
        except Exception as e:
            st.error(f"Demo parsing error: {e}")
        finally:
            # keep temp output for inspection if you want; no removal here to avoid race issues
            pass
# ---------- end demo button ----------

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

st.markdown("---")
st.markdown(
    "<div style='text-align:center; font-size:0.9em; color:gray;'>"
    "Built with ❤️ by <b>Bibhudendu Behera</b> • "
    "<a href='https://github.com/bibhu342/PDF-Parser-Pro' target='_blank'>GitHub</a> • "
    "v1.0"
    "</div>",
    unsafe_allow_html=True
)
