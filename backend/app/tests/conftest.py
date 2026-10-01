import importlib
import os
import sys
import tempfile

import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def client(monkeypatch):
    """Fresh app backed by a temp DATA_DIR sqlite db per test."""
    tmp = tempfile.mkdtemp()
    monkeypatch.setenv("DATA_DIR", tmp)
    saved = {m: sys.modules[m] for m in list(sys.modules)
             if m == "app" or m.startswith("app.")}
    for m in list(saved):
        sys.modules.pop(m)
    try:
        main = importlib.import_module("app.main")
        history = importlib.import_module("app.repositories.history")
        with TestClient(main.app) as c:  # enters startup -> seed.init_db()
            yield c, history
    finally:
        for m in list(sys.modules):
            if m == "app" or m.startswith("app."):
                sys.modules.pop(m)
        sys.modules.update(saved)
