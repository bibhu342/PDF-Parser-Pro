import runpy
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / 'scripts'
sys.path.insert(0, str(SCRIPTS))

def find_parser_module():
    # prefer explicit module name if present
    try:
        import parse_pdf_data as mod
        return 'module', mod
    except Exception:
        pass
    # fallback: search for any scripts with 'pdf' in filename
    for p in SCRIPTS.glob('*pdf*.py'):
        return 'path', p
    # also accept parse_pdf.py or pdf_parser.py variants
    for p in SCRIPTS.glob('*parse*.py'):
        if 'pdf' in p.name.lower() or 'parse' in p.name.lower():
            return 'path', p
    raise FileNotFoundError(f'No PDF parser script/module found in {SCRIPTS}')

def test_pdf_parser_smoke():
    kind, obj = find_parser_module()
    sample_pdf = ROOT / 'tests' / 'sample.pdf'
    # if no sample PDF, just ensure module/script loads
    if not sample_pdf.exists():
        if kind == 'module':
            assert obj is not None
        else:
            ns = runpy.run_path(str(obj))
            assert isinstance(ns, dict)
        return

    # if we have a sample, try to call a parser function
    if kind == 'module':
        mod = obj
        # find a callable that looks like a parser
        fn = None
        for name, val in vars(mod).items():
            if callable(val) and ('parse' in name.lower() or 'pdf' in name.lower()):
                fn = val
                break
        assert fn is not None, 'No callable parse function found in module'
        out = fn(sample_pdf)
        assert out is not None
    else:
        path = obj
        ns = runpy.run_path(str(path))
        # try to find callable in namespace
        fn = None
        for name, val in ns.items():
            if callable(val) and ('parse' in name.lower() or 'pdf' in name.lower()):
                fn = val
                break
        # If no callable, at least namespace must load
        if fn is None:
            assert isinstance(ns, dict)
        else:
            out = fn(sample_pdf)
            assert out is not None
