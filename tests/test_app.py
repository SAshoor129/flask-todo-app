import pytest

import os
import tempfile
import pytest
from app import app, db

@pytest.fixture(scope="module")
def test_client():
    # Use a temporary file for the test database
    db_fd, db_path = tempfile.mkstemp()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    with app.app_context():
        db.create_all()
    with app.test_client() as client:
        yield client
    os.close(db_fd)
    os.unlink(db_path)

def test_app_import():
    assert app is not None

def test_app_responds(test_client):
    rv = test_client.get('/')
    assert rv.status_code in [200, 302]
