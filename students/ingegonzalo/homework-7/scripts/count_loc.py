"""Cuenta lineas de codigo (sin vacias ni comentarios). Uso: python scripts/count_loc.py a.py b.py"""
import sys
from pathlib import Path


def count(path):
    return sum(
        1 for line in Path(path).read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.strip().startswith("#")
    )


if __name__ == "__main__":
    for file in sys.argv[1:]:
        print(f"{count(file):4d}  {file}")