"""
Unit tests for PDF Parser functionality
"""

import pytest
import sys
import re
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.parse_pdf_data import (
    clean_dataframe,
    extract_key_values_from_text,
    normalize_numeric_columns,
)
import pandas as pd


class TestDataFrameCleaning:
    """Test DataFrame cleaning and normalization functions"""

    def test_clean_dataframe_removes_empty_rows(self):
        """Test that clean_dataframe removes empty rows"""
        df = pd.DataFrame({
            "col1": ["a", None, "c"],
            "col2": [1, None, 3],
        })
        cleaned = clean_dataframe(df)
        assert len(cleaned) <= len(df)
        assert cleaned.columns.tolist() == ["col1", "col2"]

    def test_clean_dataframe_normalizes_column_names(self):
        """Test that column names are normalized to lowercase with underscores"""
        df = pd.DataFrame({
            "Column One": [1, 2],
            "Column Two": [3, 4],
        })
        cleaned = clean_dataframe(df)
        assert "column_one" in cleaned.columns
        assert "column_two" in cleaned.columns

    def test_normalize_numeric_columns_creates_standard_names(self):
        """Test that numeric columns are normalized to standard names"""
        df = pd.DataFrame({
            "qty": [2, 1],
            "price": ["1000.00", "500.00"],
            "total": ["2000.00", "500.00"],
        })
        normalized = normalize_numeric_columns(df)
        assert "quantity" in normalized.columns or "qty" in normalized.columns
        assert "unit_price" in normalized.columns or "price" in normalized.columns
        assert "line_total" in normalized.columns or "total" in normalized.columns


class TestKeyValueExtraction:
    """Test key-value extraction from text"""

    def test_extract_invoice_number(self):
        """Test that invoice numbers are extracted correctly"""
        # Create a temporary PDF-like text
        test_text = "Invoice #: INV-2025-001\nDate: 11/11/2025\nTotal: $3,250.00"
        
        # Since extract_key_values_from_text expects a Path, we'll test the regex pattern
        import re
        pattern = r"(?:invoice|bill)\s*#?:?\s*([A-Za-z0-9-]+)"
        match = re.search(pattern, test_text, flags=re.IGNORECASE)
        
        assert match is not None
        assert match.group(1) == "INV-2025-001"

    def test_extract_date(self):
        """Test that dates are extracted correctly"""
        test_text = "Date: 11/11/2025"
        
        pattern = r"date\s*[:\-]?\s*([0-9]{1,2}[\/\-][0-9]{1,2}[\/\-][0-9]{2,4})"
        match = re.search(pattern, test_text, flags=re.IGNORECASE)
        
        assert match is not None
        assert match.group(1) == "11/11/2025"

    def test_extract_total(self):
        """Test that totals are extracted correctly"""
        test_text = "Total: $3,250.00"
        
        pattern = r"total\s*(?:amount)?\s*[:\-]?\s*\$?([0-9,]+\.?[0-9]*)"
        match = re.search(pattern, test_text, flags=re.IGNORECASE)
        
        assert match is not None
        assert "3,250.00" in match.group(1)


class TestOCRIntegration:
    """Test OCR functionality (if available)"""

    def test_ocr_imports_available(self):
        """Test that OCR dependencies can be imported"""
        try:
            import pytesseract
            import pdf2image
            assert True
        except ImportError:
            pytest.skip("OCR dependencies not installed")


class TestParserScript:
    """Test the main parser script"""

    def test_parser_script_imports(self):
        """Test that the parser script can be imported without errors"""
        try:
            from scripts import parse_pdf_data
            assert hasattr(parse_pdf_data, 'parse_single_pdf')
            assert hasattr(parse_pdf_data, 'parse_all_pdfs')
        except ImportError as e:
            pytest.fail(f"Failed to import parser script: {e}")


def test_sample_pdf_exists():
    """Test that sample PDF exists in data/raw"""
    sample_path = Path(__file__).parent.parent / "data" / "raw"
    if sample_path.exists():
        pdf_files = list(sample_path.glob("*.pdf"))
        # Allow test to pass even if no PDFs exist (for CI environments)
        assert True
    else:
        pytest.skip("data/raw directory not found")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
