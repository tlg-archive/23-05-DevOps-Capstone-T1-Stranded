from flask import Flask, render_template, request, redirect, url_for
import os
import json

app = Flask(__name__)

current_room = "Room-one"
space_suit_picked_up = False
message = ""

def load_data():
    data = {}
    with open(
        f"{'/'.join(os.path.abspath(__file__).split('/')[:-1])}./data/title.txt", 
        'r',
        encoding="utf-8"
        ) as title_file:
        data['title'] = title_file.read()
    with open(
        f"{'/'.join(os.path.abspath(__file__).split('/')[:-1])}./data/description.txt",
        "r",
        encoding="utf-8"
        ) as plot:
        plot = plot.read()
    data['opening'] = plot
    
    return data


rooms = {
    "Room-one": {
        "description": "You are in Room 1. This is where you start.",
        "next_room": "Room-Two",
        "item": ["item1", "item2" , "item3"]
    },
    "Room-Two": {
        "description": "You are in Room 2",
        "next_room": "Room-Three",
        "item": ["Space Suit"]
    },
    "Room-Three": {
        "description": "Congratulations! You are in the space pod with the space suit. You've won!",
        "next_room": None,
        "item": ["item1", "item2" , "item3"]
    },
}

@app.route("/game", methods=["GET", "POST"])
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
                message = "Youve picked up the space suit"
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

data = load_data()

@app.route("/", methods=["GET", "POST"])
def start():
    if request.method == "POST":
        return redirect(url_for("game"))
    return render_template("start.html", title=data["title"], desc=data["opening"])

if __name__ == "__main__":
    app.run(debug=True)
