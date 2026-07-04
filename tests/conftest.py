import copy
import pytest

from app import create_app
from app import data as data_module

_INITIAL_INVENTORY = copy.deepcopy(data_module.inventory)
_INITIAL_NEXT_ID = data_module.next_id

@pytest.fixture
def app():
    flask_app = create_app()
    flask_app.config.update({"TESTING": True})
    return flask_app


@pytest.fixture
def client(app):
    data_module.inventory.clear()
    data_module.inventory.extend(copy.deepcopy(_INITIAL_INVENTORY))
    data_module.next_id = _INITIAL_NEXT_ID

    return app.test_client()