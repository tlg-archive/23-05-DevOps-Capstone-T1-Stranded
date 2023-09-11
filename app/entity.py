#imports
from app.game_object import game_object

class entity(game_object): 
<<<<<<< HEAD
    def __init__(self, id: str, state: bool):
        super().__init__(id)
=======
    def __init__(self, id: str, name: str, description: str, state: bool):
        super().__init__(id, name, description)
>>>>>>> 512d614a96574da0d408736bc7457b14753eeec6
        self.state = state