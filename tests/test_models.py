import pytest
from suddendev.models import ChatRoom


def test_create_chat_room(session):

    room_key = "ASDF"

    chat_room = ChatRoom(room_key=room_key)
    session.add(chat_room)
    session.commit()

    assert chat_room.id > 0
    assert chat_room.room_key == room_key
