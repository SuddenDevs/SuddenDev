import pytest

def test_get_index(app):
    test_app = app.test_client()
    response = test_app.get('/')
    assert response.status_code == 200


def test_get_its_a_prank_bro(app):
    test_app = app.test_client()
    response = test_app.get('/itsaprankbro')
    assert response.status_code == 200
