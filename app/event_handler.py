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
                return (False, f"{trigger_obj.name} is {trigger_obj.state} expected not {state_conditions['is']}")
            if 'is_not' in state_conditions and trigger_obj.state == state_conditions['is_not']:
                return (False, f"{trigger_obj.name} is {trigger_obj.state} expected not {state_conditions['is_not']}")
        if trigger_data.conditions.get('inventory', False) and isinstance(trigger_obj, Container):
            inventory_conditions = trigger_data.conditions['inventory']
            if 'item' in inventory_conditions:
                items = inventory_conditions['item']
                if not trigger_obj.inventory:
                    return (False, f'{trigger_obj.name} is empty and does not have {items}')
                if not all(item in trigger_obj.inventory for item in items):
                    return (False, f'{trigger_obj.name} has {trigger_obj.inventory} does not have {items}')
            if 'no_item' in inventory_conditions:
                no_items = inventory_conditions['no_item']
                if any(item in trigger_obj.inventory for item in no_items):
                    return (False, f"{trigger_obj.name} has {trigger_obj.inventory} should not have {no_items}")
        
        if trigger_data.conditions.get('current_location', False):
            location_conditions = trigger_data.conditions['current_location']
            if 'is' in location_conditions and player_location != location_conditions['is']:
                return (False, f'Location is {player_location} expected {location_conditions["is"]}')
            if 'is_not' in location_conditions and player_location == location_conditions['is_not']:
                return (False, f'Location is {player_location} expected not {location_conditions["is_not"]}')
        return (True, None)

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
        passed = True
        for trigger_data in event.triggers:
            trigger_object_kind, trigger_object_id = trigger_data.object
            trigger_obj = self.game_objs[f'{trigger_object_kind}s'][trigger_object_id]
            
            passed, message = self.validate_event_trigger(trigger_data, trigger_obj, current_location)
            if not passed:
                if god_mode:
                    return f'\n{event.name}|{event.obj_id}, failed because {message}'
                return ''
        
        self.apply_event_changes(event)
        if god_mode:
            return f'\n{event.name}, {event.description}'
        return f'\n{event.description}'
