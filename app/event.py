from app.container import Container
from app.entity import Entity
from app.game_object import GameObject

class Event(Entity):
    def __init__(
        self,
        obj_id: int,
        name: str,
        description: str,
        state: str,
        triggers: list[dict],  # List of trigger dictionaries
        affected_objects: list[dict],  # List of affected object dictionaries
        change: dict  # Change dictionary
    ) -> None:
        """
        Initialize an Event object.

        Args:
            obj_id (int): The unique identifier for the event.
            name (str): The name of the event.
            description (str): A description of the event.
            triggers (list[dict]): List of trigger dictionaries.
            affected_objects (list[dict]): List of affected object dictionaries.
            change (dict): Change dictionary.
        """
        super().__init__(obj_id, name, description, state)
        self.triggers: list[Trigger] = []

        # Convert trigger dictionaries into Trigger objects
        for trigger_data in triggers:
            trigger = Trigger(trigger_data)
            self.triggers.append(trigger)

        # Convert affected object dictionaries into tuples
        self.affected_objects: list[tuple[str, int]] = [(obj['kind'], obj['obj_id']) for obj in affected_objects]

        # Convert change dictionary into Change object
        self.change: Change = Change(
            state=change.get('state'),
            inventory=change.get('inventory')
        )

class Trigger:
    def __init__(self, trigger_data: dict) -> None:
        """
        Initialize a Trigger object.

        Args:
            trigger_data (dict): Trigger data dictionary.
        """
        trigger_object: tuple[str, int] = (trigger_data['object']['kind'], trigger_data['object']['obj_id'])
        conditions: dict = trigger_data['conditions']
        
        # Convert 'item' and 'no_item' conditions
        if 'inventory' in conditions.keys():
            conditions['inventory'] = {key: [(item['kind'], item['obj_id']) for item in value] for key, value in conditions['inventory'].items()}
        
        self.object: tuple[str, int] = trigger_object
        self.conditions: dict = conditions





class Change:
    def __init__(self, state: str = None, inventory: dict = None) -> None:
        """
        Initialize a Change object.

        Args:
            state (str, optional): The new state value. Defaults to None.
            inventory (dict, optional): Inventory change dictionary. Defaults to None.
        """
        self.state: str = state
        self.inventory: dict = inventory
