"""Make the submission root importable so ``src`` resolves under pytest.

``pytest.ini`` already sets ``pythonpath``; this file is the fallback for a
runner whose pytest predates that option.
"""

import sys
from pathlib import Path

ROOT = str(Path(__file__).resolve().parent)
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
