from flask import Flask, request, jsonify, render_template
import json

app = Flask(__name__)

# File to store input data
DATA_FILE = 'data.json'

# Helper function to load data
def load_data():
    try:
        with open(DATA_FILE, 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

# Helper function to save data
def save_data(data):
    with open(DATA_FILE, 'w') as file:
        json.dump(data, file, indent=4)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form.get('name')
    email = request.form.get('email')

    if not name or not email:
        return jsonify({"error": "Name and email are required"}), 400

    data = load_data()
    data.append({"name": name, "email": email})
    save_data(data)

    return jsonify({"message": "Data saved successfully!"})

@app.route('/data', methods=['GET'])
def get_data():
    return render_template('data.html', data=load_data())

if __name__ == '__main__':
    app.run(debug=True)
