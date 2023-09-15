from app.container import Container
from app.event import Event, Trigger
from app.game_object import GameObject


class EventHandler:
    def __init__(self, game_objs):
        self.game_objs = game_objs

    def validate_event_trigger(self, trigger_data: Trigger, trigger_obj: GameObject, player_location: int) -> bool:
        # Check if the event trigger conditions are met
        if trigger_data.conditions.get('state', False):
            state_conditions = trigger_data.conditions['state']
            if 'is' in state_conditions and trigger_obj.state != state_conditions['is']:
                return False
            if 'is_not' in state_conditions and trigger_obj.state == state_conditions['is_not']:
                return False
        if trigger_data.conditions.get('inventory', False) and isinstance(trigger_obj, Container):
            inventory_conditions = trigger_data.conditions['inventory']
            if 'item' in inventory_conditions:
                items = inventory_conditions['item']
                if not trigger_obj.inventory:
                    return False 
                if not all(item in trigger_obj.inventory for item in items):
                    return False
            if 'no_item' in inventory_conditions:
                no_items = inventory_conditions['no_item']
                if any(item in trigger_obj.inventory for item in no_items):
                    return False
        
        if trigger_data.conditions.get('current_location', False):
            state_conditions = trigger_data.conditions['current_location']
            if 'is' in state_conditions and player_location != state_conditions['is']:
                return False
            if 'is_not' in state_conditions and player_location == state_conditions['is_not']:
                return False
        return True

    def apply_event_changes(self, event: Event):
        # Apply changes to affected objects
        for affected_kind, affected_id in event.affected_objects:
            affected = self.game_objs[f'{affected_kind}s'][affected_id]
            if event.change.state:
                affected.state = event.change.state
            if event.change.inventory and isinstance(affected, Container):
                inventory_change = event.change.inventory
                for add_item in inventory_change.add:
                    affected.inventory.append(add_item)
                for remove_item in inventory_change.remove:
                    if remove_item in affected.inventory:
                        affected.inventory.remove(remove_item)

    def process_event(self, event: Event, current_location: int, god_mode: bool) -> str:
        for trigger_data in event.triggers:
            trigger_object_kind, trigger_object_id = trigger_data.object
            trigger_obj = self.game_objs[f'{trigger_object_kind}s'][trigger_object_id]
            
            if not self.validate_event_trigger(trigger_data, trigger_obj, current_location):
                if god_mode:
                    return f'{event.name} failed'
                return ''

        self.apply_event_changes(event)
        return f'{event.name}, {event.description}'
