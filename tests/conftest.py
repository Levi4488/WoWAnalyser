import pytest
from app import app

@pytest.fixture()
def application():
    application = app
    application.config.update({
        "TESTING": True,
    })

    # other setup can go here

    yield application

    # clean up / reset resources here


@pytest.fixture()
def client(application):
    return application.test_client()


@pytest.fixture()
def runner(application):
    return application.test_cli_runner()