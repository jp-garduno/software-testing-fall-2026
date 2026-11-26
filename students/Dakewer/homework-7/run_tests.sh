#!/usr/bin/env bash
# Run the whole suite with coverage and regenerate the result files.
set -euo pipefail
cd "$(dirname "$0")"

python tools/validate_test_data.py
python tools/generate_orders.py >/dev/null   # reproducible (seeded)

python -m pytest -v \
  --cov=src --cov-report=term-missing --cov-report=html:htmlcov \
  | tee test_results.txt

python tools/inline_coverage.py
