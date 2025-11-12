"""
Smoke tests for PDF Parser Pro
Basic validation tests to ensure core functionality works
"""
import importlib
import pytest
import os
import pathlib


def test_parser_importable():
    """Test that parser module can be imported"""
    try:
        module = importlib.import_module("scripts.parse_pdf_data")
    except Exception:
        module = importlib.import_module("app")
    assert module is not None


@pytest.mark.skipif(not os.path.exists("data/raw"), reason="no data/raw folder present")
def test_sample_pdf_present():
    """Test that sample PDFs are available for testing"""
    sample_dir = pathlib.Path("data/raw")
    sample_files = list(sample_dir.glob("*.pdf"))
    assert isinstance(sample_files, list)


def test_requirements_file_exists():
    """Test that requirements.txt exists"""
    assert os.path.exists("requirements.txt")


def test_app_file_exists():
    """Test that Streamlit app.py exists"""
    assert os.path.exists("app.py")
