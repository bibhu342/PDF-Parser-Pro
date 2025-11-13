import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

# detect parser file
pdf_parser_path = ROOT / 'scripts' / 'pdf_parser.py'
if not pdf_parser_path.exists():
    raise FileNotFoundError(f'Missing parser script: {pdf_parser_path}')

import runpy

def test_parse_pdf_smoke():
    # run script in isolated namespace
    ns = runpy.run_path(str(pdf_parser_path))
    assert isinstance(ns, dict), 'runpy should return namespace dict'

    # find parse function
    parse_fn = None
    for key, val in ns.items():
        if callable(val) and 'pdf' in key.lower():
            parse_fn = val
            break

    assert parse_fn is not None, 'No parse_pdf function detected'

    sample_pdf = ROOT / 'tests' / 'sample.pdf'
    assert sample_pdf.exists(), 'Missing sample.pdf for smoke test'

    # Call parser; result must be non-crashing
    output = parse_fn(sample_pdf)
    assert output is not None, 'Parser returned None'
