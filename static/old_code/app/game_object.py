
class GameObject:
    def __init__(self, obj_id: str, name: str, description: str):
        self.obj_id = obj_id
        self.name = name
        self._description = description
    
    @property
    def description(self) -> str:
        description = self._description.split(sep= '\\n')
        text = ''
        for line in description:
            text = f"{text}{line}\n"
        return text
