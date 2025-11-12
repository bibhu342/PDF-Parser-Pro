# Contributing to PDF-Parser-Pro

Thank you for your interest in contributing to PDF-Parser-Pro! This document provides guidelines and instructions for contributing to the project.

## 🤝 Ways to Contribute

- **Report bugs** — Submit detailed bug reports via GitHub Issues
- **Suggest features** — Propose new features or enhancements
- **Improve documentation** — Fix typos, add examples, or clarify instructions
- **Submit code** — Fix bugs or implement new features via Pull Requests
- **Test and provide feedback** — Try the tool and share your experience

## 🐛 Reporting Bugs

When reporting a bug, please include:

1. **Clear description** of the issue
2. **Steps to reproduce** the problem
3. **Expected behavior** vs. **actual behavior**
4. **Environment details** (OS, Python version, dependencies)
5. **Sample PDF** (if applicable and not confidential)
6. **Error messages** or logs

**Template:**
```
**Bug Description:**
[Clear description of the bug]

**Steps to Reproduce:**
1. Step one
2. Step two
3. ...

**Expected Behavior:**
[What should happen]

**Actual Behavior:**
[What actually happens]

**Environment:**
- OS: Windows 10 / Ubuntu 22.04 / macOS 13
- Python: 3.11.5
- PDF-Parser-Pro version: main branch / v1.0.0

**Additional Context:**
[Screenshots, error logs, sample files]
```

## 💡 Suggesting Features

Feature requests are welcome! Please:

1. **Check existing issues** to avoid duplicates
2. **Clearly describe** the feature and its use case
3. **Explain why** it would be valuable
4. **Provide examples** of how it would work

## 🔧 Development Setup

### 1. Fork and Clone

```bash
# Fork the repo on GitHub, then:
git clone https://github.com/YOUR_USERNAME/PDF-Parser-Pro.git
cd PDF-Parser-Pro
```

### 2. Create Virtual Environment

```bash
# Windows
python -m venv .venv
.\.venv\Scripts\Activate

# macOS/Linux
python -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Install OCR Dependencies (Optional)

```bash
# Windows
winget install --id UB-Mannheim.TesseractOCR
python setup_ocr_dependencies.py

# macOS
brew install tesseract poppler

# Ubuntu/Debian
sudo apt-get install tesseract-ocr poppler-utils
```

### 5. Run Tests

```bash
pytest tests/ -v
```

## 📝 Code Style

- Follow **PEP 8** Python style guidelines
- Use **meaningful variable names**
- Add **docstrings** to functions and classes
- Keep functions **small and focused**
- Add **type hints** where appropriate

**Example:**
```python
def parse_invoice_total(text: str) -> float | None:
    """
    Extract invoice total from text using regex.
    
    Args:
        text: Raw text content from PDF
        
    Returns:
        Extracted total as float, or None if not found
    """
    pattern = r"total\s*[:\-]?\s*\$?([0-9,]+\.?[0-9]*)"
    match = re.search(pattern, text, flags=re.IGNORECASE)
    if match:
        return float(match.group(1).replace(",", ""))
    return None
```

## 🔀 Pull Request Process

### 1. Create a Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/bug-description
```

### 2. Make Changes

- Write clean, well-documented code
- Add tests for new functionality
- Update documentation as needed
- Ensure all tests pass

### 3. Commit Changes

Use clear, descriptive commit messages:

```bash
git add .
git commit -m "feat: add support for multi-page invoice parsing"
# or
git commit -m "fix: handle missing invoice numbers gracefully"
# or
git commit -m "docs: update README with deployment instructions"
```

**Commit message format:**
- `feat:` — New feature
- `fix:` — Bug fix
- `docs:` — Documentation changes
- `test:` — Adding or updating tests
- `refactor:` — Code refactoring
- `style:` — Code style/formatting changes
- `ci:` — CI/CD changes

### 4. Push and Create PR

```bash
git push origin feature/your-feature-name
```

Then create a Pull Request on GitHub with:
- **Clear title** describing the change
- **Detailed description** of what was changed and why
- **Reference to related issues** (e.g., "Closes #123")
- **Test results** or screenshots if applicable

### 5. PR Review

- Respond to feedback promptly
- Make requested changes if needed
- Keep the conversation professional and constructive

## ✅ Testing Guidelines

- **Write tests** for new features
- **Ensure existing tests pass** before submitting PR
- **Test edge cases** (empty PDFs, malformed data, missing fields)
- **Test OCR functionality** if modifying OCR-related code

Run tests locally:
```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_parser.py -v

# Run with coverage
pytest tests/ --cov=scripts --cov-report=html
```

## 📚 Documentation

When adding features, please update:
- **README.md** — If adding user-facing features
- **Docstrings** — For all new functions/classes
- **Code comments** — For complex logic
- **Examples** — In the `notebooks/` directory if applicable

## 🏷️ Versioning

This project follows [Semantic Versioning](https://semver.org/):
- **MAJOR** version: Incompatible API changes
- **MINOR** version: New features (backward compatible)
- **PATCH** version: Bug fixes (backward compatible)

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

## 💬 Questions?

Feel free to:
- Open a GitHub Issue for questions
- Email: [your-email@example.com]
- Connect on [LinkedIn](https://www.linkedin.com/in/bibhudendu-behera)

## 🙏 Thank You!

Your contributions help make PDF-Parser-Pro better for everyone. We appreciate your time and effort!

---

**Happy Contributing!** 🚀
