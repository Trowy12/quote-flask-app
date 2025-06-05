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

@app.route('/quotes')
def get_all_quotes():
    return jsonify(quotes)

@app.route('/quote/<int:index>', methods=['DELETE'])
def delete_quote(index):
    if 0 <= index < len(quotes):
        removed = quotes.pop(index)
        save_quotes(quotes)
        return jsonify({"message": "Quote deleted", "quote": removed})
    return jsonify({"error": "Quote not found"}), 404

@app.route('/quote/<int:index>', methods=['PUT'])
def update_quote(index):
    if 0 <= index < len(quotes):
        data = request.json
        quotes[index] = {
            "text": data.get("text", quotes[index]["text"]),
            "author": data.get("author", quotes[index]["author"])
        }
        save_quotes(quotes)
        return jsonify({"message": "Quote updated", "quote": quotes[index]})
    return jsonify({"error": "Quote not found"}), 404

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

# Updated to bind to 0.0.0.0 for Render deployment
if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)



