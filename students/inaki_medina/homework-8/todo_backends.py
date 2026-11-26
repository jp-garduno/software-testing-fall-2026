import importlib.util
import sys
from pathlib import Path


HOMEWORK_ROOT = Path(__file__).resolve().parent
BACKENDS = ("selenium", "playwright")


def load_todo_backend(name):
    if name not in BACKENDS:
        raise ValueError(
            f"Unknown todo backend {name!r}; choose one of: {', '.join(BACKENDS)}"
        )

    module_name = f"_homework8_{name}_todo_page"
    if module_name in sys.modules:
        return sys.modules[module_name]

    module_path = HOMEWORK_ROOT / name / "pages" / "todo_page.py"
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load todo backend from {module_path}")

    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module
