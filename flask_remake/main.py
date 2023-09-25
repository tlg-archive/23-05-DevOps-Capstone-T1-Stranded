from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

current_room = "Room-one"
space_suit_picked_up = False
message = ""

rooms = {
    "Room-one": {
        "description": "You are in Room 1. This is where you start.",
        "next_room": "Room-Two",
        "item": ["item1", "item2" , "item3"]
    },
    "Room-Two": {
        "description": "You are in Room 2. You see a space suit here.",
        "next_room": "Room-Three",
        "item": ["item1", "item2" , "item3"]
    },
    "Room-Three": {
        "description": "Congratulations! You are in Room 3 with the space suit. You've won!",
        "next_room": None,
        "item": ["item1", "item2" , "item3"]
    },
}

@app.route("/", methods=["GET", "POST"])
def game():
    global current_room
    global space_suit_picked_up
    global message
    
    if request.method == "POST":
        action = request.form['action'].lower()
        
        
        
        
        if current_room == "Room-one":
            if action == "move room 2":
                current_room = 'Room-Two'
                message=''
            elif action == "look":
                message = rooms[current_room]["item"]
            else:
                message = "Youcantdothat"
                
        elif current_room == "Room-Two":
            if action == "pickup suit":
                space_suit_picked_up = True
            elif action == "look":
                message = rooms[current_room]["item"]
            elif action == "move room 3":
                if space_suit_picked_up:
                    current_room = "Room-Three"
                    message = ""
                else:
                    message = "you cant board the pod without a space suit"
            else:
                message = "invalid action"
                
        elif current_room == "Room-Three":
            message = "you won!"

    return render_template("index.html", description=rooms[current_room], room=current_room, message=message)

if __name__ == "__main__":
    app.run(debug=True)