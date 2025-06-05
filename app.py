from flask import Flask, render_template, jsonify, request
import json
import os
import random

app = Flask(__name__)

# ----------------------------
# Quote storage: JSON-based
# ----------------------------

# Load quotes from file
def load_quotes():
    if os.path.exists("quotes.json"):
        with open("quotes.json", "r") as f:
            return json.load(f)
    return []

# Save quotes to file
def save_quotes(quotes):
    with open("quotes.json", "w") as f:
        json.dump(quotes, f, indent=2)

# Initialize quotes
quotes = load_quotes()

# ----------------------------
# Routes
# ----------------------------

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/quote')
def get_quote():
    return jsonify(random.choice(quotes))

@app.route('/submit', methods=['POST'])
def submit_quote():
    data = request.json
    new_quote = {
        "text": data.get("text", ""),
        "author": data.get("author", "Unknown")
    }

    if new_quote["text"]:
        quotes.append(new_quote)
        save_quotes(quotes)
        print(f"Added new quote: {new_quote}")
        return jsonify({"message": "Quote added successfully!"})
    else:
        return jsonify({"message": "Quote text cannot be empty."}), 400

# ----------------------------
# Run Server
# ----------------------------

if __name__ == '__main__':
    app.run(debug=True)
