"""
Copyright (C) 2025 Aseem Athale

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

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
