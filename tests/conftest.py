import copy
import pytest

from app import create_app
from app import data as data_module

_INITIAL_INVENTORY = copy.deepcopy(data_module.inventory)
_INITIAL_NEXT_ID = data_module.next_id