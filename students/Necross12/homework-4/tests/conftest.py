import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from banking_system import BankAccount


@pytest.fixture
def cuenta_estandar():
    return BankAccount("Estándar", 10000)


@pytest.fixture
def cuenta_ahorro():
    return BankAccount("Ahorro", 10000)

"""
import pytest

from banking_system import BankAccount

@pytest.fixture
def cuenta_estandar():
    return BankAccount("Estándar", 10000)

@pytest.fixture
def cuenta_ahorro():
    return BankAccount("Ahorro", 10000)

python -m pytest -v
python -m pytest --cov=src --cov-report=html --cov-report=term

"""
