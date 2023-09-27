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
    with open(
              f"{'/'.join(os.path.abspath(__file__).split('/')[:-1])}./data/help.txt",
              "r",
              encoding="utf-8"
              ) as help_file:
        data['help'] = help_file.read()
     
    
    return data


rooms = {
    "Escape-Pod": {
        "description": "Your thoughts were of fear before settling into a growing sense of elation. The pods' alarms were blaring and the interface before you both told you the same thing: you had crashed. You had lived..",
        "next_room": "Room-Two",
        "item": ["item1", "item2" , "item3"],
        "look": "You look around and see the Space Plaza"
    },
    "Space-Plaza": {
        "description": "You stumble upon a settlement. As you enter the main plaza, a profound stillness blankets the area. The only sound that disturbs this silence is the sound of your feet echoing on the pavement and the\\ngentle, soothing sounds of the central fountain gracing the plaza. From here is a path back to the jungle. Nearby you notice signs to various places important to the colony. The one closest is a sign\\nwith the words \"Arquebus Interplanetary Spaceport\" leading onto a high way ramp. Its catapult noticeable from here. Farther away in another direction you can see a collapsed bridge with a sign marking\\nit as the \"Residential District.\" Finally the last sign of note was in the direction of a large tunnel you can see is flooded with the words \"Schneider Research Laboratories overhead",
        "next_room": "Room-Three",
        "item": ["Space Suit"],
        "look": "you can see the ship bay in the distance and a space suit" 
    },
    "Ship-Bay": {
        "description": "Congratulations! You are in the space pod with the space suit. You've won!",
        "next_room": None,
        "item": ["item1", "item2" , "item3"]
    },
}

@app.route("/game", methods=["GET", "POST"])
def game():
    if "current_room" not in session:
        session["current_room"] = "Escape-Pod"
        session["space_suit_picked_up"] = False
        session["message"] = ""
        session["inventory"] = []
        session["help"] = data["help"]
    
    if request.method == "POST":
        action = request.form['action'].lower()
        

        if session["current_room"] == "Escape-Pod":################################################################################
            if action == "move space plaza":
                session["current_room"] = 'Space-Plaza'
                session["message"] = ''
            elif action == "look":
                session["message"] = rooms[session["current_room"]]["look"]
            else:
                session["message"] = "Youcantdothat"
                
        elif session["current_room"] == "Space-Plaza":################################################################################
            if action == "pickup suit":
                session['space_suit_picked_up'] = True
                session["inventory"].append('space suit')
                session["message"] = "Youve picked up the space suit"
            elif action == "look":
                session["message"] = rooms[session["current_room"]]["look"]
            elif action == "move ship bay":
                if session["space_suit_picked_up"]:
                    session["current_room"] = "Ship-Bay"
                    session["message"] = ""
                else:
                    session["message"] = "you cant board the pod without a space suit"
            else:
                session["message"] = "invalid action"
                
        elif session["current_room"] == "Ship Bay":
            session["message"] = "you won!"

    return render_template("index.html", description=rooms[session["current_room"]], stuff=session)

data = load_data()

@app.route("/", methods=["GET", "POST"])
def start():
    if request.method == "POST":
        return redirect(url_for("game"))
    return render_template("start.html", title=data["title"], desc=data["opening"])

if __name__ == "__main__":
    app.run(debug=True)
