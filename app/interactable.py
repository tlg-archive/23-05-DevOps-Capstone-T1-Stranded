#imports

from app.entity import Entity


class Interactable(Entity):
    def __init__(self,
                 obj_id: str,
                 name: str,
                 description: str,
                 state: bool,
                 state_descriptions: dict[str, str],
                 state_transitions: dict[str, str],
                 state_list: list[str]
                 ):
        super().__init__(obj_id, name, description, state)
        self.state_descriptions = state_descriptions
        self.state_transitions = state_transitions
        self.state_list = state_list

    @property
    def description(self) -> str:
        return f"{self._description} {self.state_descriptions[self.state]}"

    def cycle(self) -> str:
        if self.state in self.state_list:
            self.state = self.state_list.pop(0)
            self.state_list.append(self.state)
            return self.state_transitions[self.state]
        return f'The {self.name} ramains {self.state}. Perhaps you are missing something?'
