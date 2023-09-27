# Events in Your Game

Events in your game are a crucial mechanism for triggering actions and interactions based on various conditions within the game world. Events can be used to create dynamic and engaging experiences for players. In this guide, we'll explore the different features of events and how to use them effectively.

## Event Features

### 1. Triggering Events

Events are triggered by specific conditions associated with game objects. These conditions are defined using YAML data within the event definition.

#### Example:

```yaml
# Example Event
- obj_id: 1
  name: "Event 1"
  description: "Description of Event 1"
  triggers:
    - object:               # Object to listen to
        kind: "npc"         # Type of object (e.g., npc, location, item)
        obj_id: 1           # ID of the object to listen to
      conditions:
        current_location:
          is: 1             # Trigger when the object is in location 1
          is_not: 2         # Don't trigger when the object is in location 2
        state:
          is: 'state'       # Trigger when the object's state is 'state'
          is_not: 'not_state' # Don't trigger when the object's state is 'not_state'
        inventory:
          item:              # Trigger when all specified items are in inventory
            - kind: "item"  
              obj_id: 2
          no_item:           # Trigger when none of the specified items are in inventory
            - kind: "item"
              obj_id: 3
```

### 2. Affected Objects

Events can affect other game objects when triggered. You can specify which objects are affected by an event using YAML data.

#### Example:

```yaml
affected_objects:
  - kind: "npc"           # Type of objects to affect (e.g., npc, item, location)
    obj_id: 2             # ID of the object to affect
```

### 3. Changes

Events can bring about changes in the game world. You can define these changes using YAML data within the event definition.

#### Example:

```yaml
change:
  state: 'new_state'     # Change the state of affected objects to 'new_state'
  inventory:
    add:                 # Add items to affected objects' inventory
      - kind: 'item'
        id: 4
    remove:              # Remove items from affected objects' inventory
      - kind: 'item'
        id: 5
```

### 4. Activation and Deactivation

Events can be activated or deactivated by changing their state. This provides flexibility in controlling when events should occur.

#### Example:

```yaml
# Initially, the event is deactivated (state: 'inactive')
state: 'inactive'

# Later in the game, you can activate the event by changing its state to 'active'
state: 'active'
```

### 5. Changing Event States

You can create events that change the state of other events, transitioning them from inactive to active when certain conditions are met.

#### Example:

```yaml
# Example Event to Activate Another Event
- obj_id: 2
  name: "Activate Event 1"
  description: "Activates Event 1 when conditions are met"
  triggers:
    - object:               # Object to listen to
        kind: "npc"         # Type of object (e.g., npc, location, item)
        obj_id: 1           # ID of the object to listen to
      conditions:
        inventory:
          item:              # Trigger when item 2 is in the inventory
            - kind: "item"  
              obj_id: 2
  affected_objects:
    - kind: "event"         # Activate Event 1
      obj_id: 1
  change:
    state: 'active'         # Change the state of Event 1 to 'active'
```

## How to Use Events

To use events effectively in your game, follow these steps:

1. **Define Events**: Create event definitions using YAML data, specifying the trigger conditions, affected objects, and desired changes.

2. **Trigger Events**: Within your game logic, implement a mechanism to process events. When trigger conditions are met, call the event processing function.

3. **Apply Changes**: When an event is triggered, apply the defined changes to affected game objects. Update their states, inventory, or other attributes as needed.

4. **Activate/Deactivate**: Control the activation and deactivation of events by changing their states in response to in-game events or player actions.

5. **Test and Iterate**: Test your events thoroughly to ensure they work as intended. Make adjustments and iterate as needed to create engaging gameplay experiences.

Events add depth and interactivity to your game world. By mastering event creation and management, you can create dynamic and immersive gameplay for your players.

---

Feel free to adapt and expand upon this example to suit your game's specific needs.