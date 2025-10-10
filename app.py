from flask import Flask, render_template, request, redirect, jsonify
import json
from datetime import datetime
import os

app = Flask(__name__)

MESSAGES_FILE = "messages.json"

def load_messages():
    if os.path.exists(MESSAGES_FILE):
        with open(MESSAGES_FILE, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

def save_messages(messages):
    with open(MESSAGES_FILE, "w", encoding="utf-8") as f:
        json.dump(messages, f, ensure_ascii=False, indent=4)

@app.route("/")
def index():
    messages = load_messages()
    messages.reverse()
    return render_template("index.html", messages=messages)

@app.route("/", methods=["POST"])
def add_message():
    name = request.form.get("name")
    email = request.form.get("email")
    phone = request.form.get("phone")
    comment = request.form.get("comment")
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    new_message = {
        "name": name,
        "email": email,
        "phone": phone,
        "comment": comment,
        "time": time
    }

    messages = load_messages()
    messages.append(new_message)
    save_messages(messages)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)