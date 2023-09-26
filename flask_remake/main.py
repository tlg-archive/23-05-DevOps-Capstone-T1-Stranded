from flask import Flask, render_template, request, redirect, url_for, session
import os
import json
import secrets
import string


app = Flask(__name__)
app.secret_key = ''.join(secrets.choice(string.ascii_letters + string.digits) for i in range(16))




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
    if "current_room" not in session:
        session["current_room"] = "Room-one"
        session["space_suit_picked_up"] = False
        session["message"] = ""
    
    if request.method == "POST":
        action = request.form['action'].lower()
        

        if session["current_room"] == "Room-one":
            if action == "move room 2":
                session["current_room"] = 'Room-Two'
                session["message"] = ''
            elif action == "look":
                session["message"] = rooms[session["current_room"]]["item"]
            else:
                session["message"] = "Youcantdothat"
                
        elif session["current_room"] == "Room-Two":
            if action == "pickup suit":
                session['space_suit_picked_up'] = True
                session["message"] = "Youve picked up the space suit"
            elif action == "look":
                session["message"] = rooms[session["current_room"]]["item"]
            elif action == "move room 3":
                if session["space_suit_picked_up"]:
                    session["current_room"] = "Room-Three"
                    session["message"] = ""
                else:
                    session["message"] = "you cant board the pod without a space suit"
            else:
                session["message"] = "invalid action"
                
        elif session["current_room"] == "Room-Three":
            session["message"] = "you won!"

    return render_template("index.html", description=rooms[session["current_room"]], room=session["current_room"], message=session["message"])

data = load_data()

@app.route("/", methods=["GET", "POST"])
def start():
    if request.method == "POST":
        return redirect(url_for("game"))
    return render_template("start.html", title=data["title"], desc=data["opening"])

if __name__ == "__main__":
    app.run(debug=True)
