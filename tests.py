import pytest
from main import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'e a pilot of a transport ship' in response.data  
def test_game_initialization(client):
    response = client.get('/game')
    assert response.status_code == 200
    assert b'Escape-Pod' in response.data 
    
    
    
    
def test_move_to_space_plaza(client):
    response = client.post('/game', data={'action': 'move space plaza'}, follow_redirects=True)
    assert response.status_code == 200
    assert b'Space-Plaza' in response.data  # Check if the new room is displayed

def test_invalid_action(client):
    response = client.post('/game', data={'action': 'move room2 3'}, follow_redirects=True)
    assert response.status_code == 200
    assert b'Youcantdothat' in response.data  # Check if an error message is displayed for invalid action

def test_pickup_suit(client):
    client.post('/game', data={'action': 'move space plaza'}, follow_redirects=True)
    response = client.post('/game', data={'action': 'pickup suit'}, follow_redirects=True)
    assert response.status_code == 200
    assert b'Youve picked up the space suit' in response.data  # Check if the message is displayed
    # You can also check if the space suit is in the inventory

def test_cant_board_pod_without_suit(client):
    client.post('/game', data={'action': 'move space plaza'}, follow_redirects=True)
    response = client.post('/game', data={'action': 'move ship bay'}, follow_redirects=True)
    assert response.status_code == 200
    assert b'you cant board the pod without a space suit' in response.data  # Check if the error message is displayed
