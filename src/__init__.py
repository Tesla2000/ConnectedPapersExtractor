import importlib
from pathlib import Path

__all__ = [
    (
        module.with_suffix("").name,
        importlib.import_module("." + module.with_suffix("").name, __name__),
    )[0]
    for module in Path(__file__).parent.iterdir()
    if module.name not in ("__init__.py", "pycache")
]
