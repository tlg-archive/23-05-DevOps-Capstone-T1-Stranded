from app.interactable import Interactable


class Transition(Interactable):
    def __init__(self,
                 obj_id: str,
                 name: str,
                 description: str,
                 state: bool,
                 state_descriptions: dict[str,str],
                 state_transitions: dict[str,str],
                 state_list: list[str],
                 target: tuple[str, int],
                 blocking_states: list[str]
                 ):
        super().__init__(obj_id, name, description, state, state_descriptions, state_transitions, state_list)
        self.target = target
        if not blocking_states:
            blocking_states = []
        self.blocking_states = blocking_states

    @property
    def blocked(self):
        if not self.blocking_states:
            return False
        return self.state in self.blocking_states
