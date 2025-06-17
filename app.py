from flask import Flask, render_template, request, jsonify
import json, random, datetime

app = Flask(__name__)

# Load intents
with open("intents.json", "r", encoding="utf-8") as file:
    intents = json.load(file)

# Chatbot logic
def get_response(user_input):
    user_input = user_input.lower()
    for intent, data in intents.items():
        if intent == "fallback":
            continue
        for pattern in data["patterns"]:
            if pattern in user_input:
                response = random.choice(data["responses"])
                if intent == "time":
                    now = datetime.datetime.now()
                    time_str = now.strftime("%H:%M")
                    return f"{response} Sekarang jam {time_str}"
                return response
    return random.choice(intents["fallback"]["responses"])

# Routes
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get", methods=["GET"])
def get_bot_response():
    user_text = request.args.get("msg")
    return get_response(user_text)

if __name__ == "__main__":
    app.run(debug=True)
