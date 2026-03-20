from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

DATA_FOLDER = "data"

# -----------------------------
# Hilfsfunktionen
# -----------------------------
def load_json(filename):
    path = os.path.join(DATA_FOLDER, filename)
    
    if not os.path.exists(path):
        return {}
    
    with open(path, "r") as f:
        return json.load(f)

def save_json(filename, data):
    path = os.path.join(DATA_FOLDER, filename)
    
    with open(path, "w") as f:
        json.dump(data, f, indent=4)

# -----------------------------
# USERS
# -----------------------------
@app.route("/users", methods=["GET"])
def get_users():
    data = load_json("users.json")
    return jsonify(data)

# -----------------------------
# APPS PRO USER
# -----------------------------
@app.route("/apps/<user>", methods=["GET", "POST"])
def apps(user):
    data = load_json("apps.json")

    if request.method == "GET":
        return jsonify(data.get(user, []))

    # POST → speichern
    new_data = request.json
    data[user] = new_data
    save_json("apps.json", data)

    return jsonify({"status": "ok"})

# -----------------------------
# PINNED (FAVORITEN)
# -----------------------------
@app.route("/pinned/<user>", methods=["GET", "POST"])
def pinned(user):
    data = load_json("pinned.json")

    if request.method == "GET":
        return jsonify(data.get(user, []))

    new_data = request.json
    data[user] = new_data
    save_json("pinned.json", data)

    return jsonify({"status": "ok"})

# -----------------------------
# SERVER START
# -----------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
