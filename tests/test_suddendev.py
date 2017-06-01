import pytest


def test_get_index(app):
    test_app = app.test_client()
    response = test_app.get('/')
    assert response.status_code == 200
