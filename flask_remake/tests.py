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