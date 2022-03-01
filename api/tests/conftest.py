import pytest
from api import create_app, db


@pytest.fixture
def app():
    flask_app = create_app()
    flask_app.app_context().push()
    yield flask_app


@pytest.fixture
def client(app):
    yield app.test_client()
