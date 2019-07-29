import pytest
from server import create_app


@pytest.yield_fixture
def app():
    app = create_app()
    yield app


@pytest.fixture
def test_cli(loop, app, sanic_client):
    return loop.run_until_complete(sanic_client(app))
