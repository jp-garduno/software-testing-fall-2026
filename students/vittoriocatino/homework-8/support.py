"""Shared configuration, Page Object loading and real operation measurements."""

from functools import wraps
import importlib.util
import os
from pathlib import Path
from time import perf_counter

ROOT = Path(__file__).resolve().parent
BASE_URL = os.environ.get("TODO_URL", "https://todomvc.com/examples/react/dist/")
STATS = {"setup": {}, "tests": [], "operations": []}
SESSION_STARTED = perf_counter()


def chrome_launch_options():
    """Use an explicit CI binary when provided, otherwise installed Chrome."""
    binary = os.environ.get("CHROME_BINARY")
    return {"executable_path": binary} if binary else {"channel": "chrome"}


def measured(method):
    """Record successful/failed operation wall time without changing its outcome."""

    @wraps(method)
    def wrapped(self, *args, **kwargs):
        started = perf_counter()
        succeeded = False
        try:
            result = method(self, *args, **kwargs)
            succeeded = True
            return result
        finally:
            STATS["operations"].append(
                {
                    "engine": self.engine,
                    "operation": method.__name__,
                    "seconds": perf_counter() - started,
                    "success": succeeded,
                }
            )

    return wrapped


def page_type(engine):
    """Load same-named POM files without shadowing installed browser packages."""
    path = ROOT / engine / "pages/todo_page.py"
    spec = importlib.util.spec_from_file_location(f"{engine}_todo_page", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.TodoPage
