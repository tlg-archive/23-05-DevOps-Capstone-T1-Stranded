#imports

from app.entity import Entity


class Intractable(Entity):
    def __init__(self,
                 obj_id: str,
                 name: str,
                 description: str,
                 state: bool,
                 state_descriptions: dict[str, str],
                 state_transitions: dict[str, str],
                 state_list: list[str],
                 key_info: dict[str, dict[str, int or str] or str]
                 ):
        super().__init__(obj_id, name, description, state)
        self.state_descriptions = state_descriptions
        self.state_transitions = state_transitions
        self.state_list = state_list
        if not key_info:
            key_info = {'key': '', 'message': '', 'state': ''}
        else:
            key_info['key'] = (key_info['key']['kind'], key_info['key']['obj_id'])
        self.key = key_info['key']
        self.key_message = key_info['message']
        self.key_state = key_info['state']

    @property
    def description(self) -> str:
        return f"{self._description} {self.state_descriptions[self.state]}"

    def cycle(self) -> str:
        if self.state in self.state_list:
            self.state = self.state_list.pop(0)
            self.state_list.append(self.state)
            return self.state_transitions[self.state]
        return f'The {self.name} remains {self.state}. Perhaps you are missing something?'

    def unlock(self, key: tuple[str, int], name: str) -> str:
        if self.key:
            if key == self.key:
                self.state = self.key_state
                return self.key_message
            return f"The {name} seem to work here..."
        return f"I don't think I can use anything on the {self.name}"
    