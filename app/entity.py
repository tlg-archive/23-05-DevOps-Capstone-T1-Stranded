#imports
from app.game_object import game_object

class entity(game_object): 
    def __init__(self, id: str, state: bool):
        super().__init__(id)
        self.state = state