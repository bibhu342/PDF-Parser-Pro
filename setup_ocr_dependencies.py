"""
Setup script to configure OCR dependencies for Windows
This script helps set up Tesseract and Poppler paths for the PDF parser
"""

import os
import sys
import requests
import zipfile
from pathlib import Path
import shutil

def download_poppler():
    """Download and extract Poppler for Windows"""
    poppler_dir = Path("C:/poppler")
    poppler_bin = poppler_dir / "bin"
    
    if poppler_bin.exists() and any(poppler_bin.glob("*.exe")):
        print("✅ Poppler already installed")
        return str(poppler_bin)
    
    print("📥 Downloading Poppler for Windows...")
    
    # Poppler for Windows download URL (latest release)
    url = "https://github.com/oschwartz10612/poppler-windows/releases/download/v23.08.0-0/Release-23.08.0-0.zip"
    
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        zip_path = poppler_dir / "poppler.zip"
        poppler_dir.mkdir(exist_ok=True)
        
        with open(zip_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        print("📦 Extracting Poppler...")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(poppler_dir)
        
        # Find the extracted directory (it might be nested)
        extracted_dirs = [d for d in poppler_dir.iterdir() if d.is_dir() and d.name.startswith("poppler")]
        if extracted_dirs:
            extracted_dir = extracted_dirs[0]
            bin_dir = extracted_dir / "bin"
            if bin_dir.exists():
                # Move bin contents to poppler/bin
                if not poppler_bin.exists():
                    poppler_bin.mkdir()
                for item in bin_dir.iterdir():
                    shutil.move(str(item), str(poppler_bin))
        
        # Clean up
        zip_path.unlink(missing_ok=True)
        
        print("✅ Poppler installed successfully")
        return str(poppler_bin)
        
    except Exception as e:
        print(f"❌ Error downloading Poppler: {e}")
        return None

def find_tesseract():
    """Find Tesseract installation"""
    common_paths = [
        "C:/Program Files/Tesseract-OCR/tesseract.exe",
        "C:/Program Files (x86)/Tesseract-OCR/tesseract.exe",
        "C:/Users/{}/AppData/Local/Programs/Tesseract-OCR/tesseract.exe".format(os.getenv('USERNAME')),
    ]
    
    # Check if already in PATH
    if shutil.which("tesseract"):
        print("✅ Tesseract found in PATH")
        return shutil.which("tesseract")
    
    # Check common installation paths
    for path in common_paths:
        if Path(path).exists():
            print(f"✅ Tesseract found at: {path}")
            return path
    
    print("❌ Tesseract not found. Please install Tesseract OCR:")
    print("   Download from: https://github.com/UB-Mannheim/tesseract/wiki")
    print("   Or run: winget install --id UB-Mannheim.TesseractOCR")
    return None

def update_ocr_verify_script():
    """Update the ocr_verify.py script with proper paths"""
    script_path = Path("scripts/ocr_verify.py")
    
    if not script_path.exists():
        print("❌ ocr_verify.py not found")
        return
    
    tesseract_path = find_tesseract()
    poppler_path = download_poppler()
    
    if not tesseract_path:
        return
    
    # Read the current script
    with open(script_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Add path configuration at the top
    path_config = f'''"""
OCR Verification Script
Verifies that pdf2image and pytesseract are working correctly
"""

import os
import sys
from pathlib import Path

# Configure paths for Windows
TESSERACT_PATH = r"{tesseract_path}"
'''
    
    if poppler_path:
        path_config += f'POPPLER_PATH = r"{poppler_path}"\n'
        path_config += '''
# Add poppler to PATH
if POPPLER_PATH not in os.environ.get("PATH", ""):
    os.environ["PATH"] = POPPLER_PATH + os.pathsep + os.environ.get("PATH", "")
'''
    
    path_config += '''
# Configure pytesseract
import pytesseract
pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH

'''
    
    # Replace the existing imports section
    lines = content.split('\n')
    new_lines = []
    skip_until_imports = True
    
    for line in lines:
        if skip_until_imports and (line.startswith('import ') or line.startswith('from ')):
            skip_until_imports = False
            new_lines.append(path_config)
        
        if not skip_until_imports:
            new_lines.append(line)
    
    # Write the updated script
    with open(script_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(new_lines))
    
    print("✅ Updated ocr_verify.py with proper paths")

if __name__ == "__main__":
    print("🔧 Setting up OCR dependencies...")
    update_ocr_verify_script()
    print("\n🎉 Setup complete! Now try running: python scripts\\ocr_verify.py")