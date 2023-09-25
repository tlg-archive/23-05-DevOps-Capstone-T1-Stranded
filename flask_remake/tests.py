from pytest import *
from flask import Flask
from main import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_initial_room(client):
    response = client.get('/')
    assert b'You are in Room 1' in response.data

def test_invalid_action(client):
    response = client.post('/', data={'action': 'move3 kio'})
    assert b'Youcantdothat' in response.data


def test_move_to_room_two(client):
    response = client.post('/', data={'action': 'move room 2'})
    assert b'You are in Room 2. You see a space suit here.' in response.data
