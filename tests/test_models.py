import pytest
from suddendev.models import GameSetup


def test_create_game(session):
    game_setup = GameSetup('ASDF')
    assert game_setup.player_count == 0
