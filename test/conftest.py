import os
import tempfile

import pytest

from typo import create_app
from config import TestConfig


@pytest.fixture
def application():
    db_fd, db_path = tempfile.mkstemp()
    app = create_app(TestConfig)

    yield app

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(application):
    with application.test_client() as client:
        yield client
