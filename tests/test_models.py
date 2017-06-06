import pytest
from suddendev.models import User


def test_create_user_has_empty_script(session):
    user = User()
    assert user.script == None
