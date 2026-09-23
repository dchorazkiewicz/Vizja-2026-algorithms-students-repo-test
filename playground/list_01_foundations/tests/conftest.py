import importlib.util
import os
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]


def solution_path() -> Path:
    configured = os.environ.get("SOLUTION_FILE")
    if configured:
        return Path(configured).resolve()
    return ROOT / "reference_solution.py"


def load_solution():
    path = solution_path()
    spec = importlib.util.spec_from_file_location("list01_solution", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load solution from {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="session")
def solution():
    return load_solution()


@pytest.fixture(scope="session")
def source_path():
    return solution_path()
