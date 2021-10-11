import os
import sys

import pytest

src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, src_path)
os.chdir(src_path)


@pytest.fixture
def client():
    from app.main import app
    app.config["TESTING"] = True
    return app.test_client()
