from flask import Flask, render_template, request, jsonify
import json
import os

app = Flask(__name__)

MEDICINES_FILE = 'medicines.json'

def load_medicines():
    if os.path.exists(MEDICINES_FILE):
        with open(MEDICINES_FILE, 'r') as f:
            return json.load(f)
    return []

def save_medicines(medicines):
    with open(MEDICINES_FILE, 'w') as f:
        json.dump(medicines, f, indent=2)

@app.route('/')
def index():
    medicines = load_medicines()
    return render_template('index.html', medicines=medicines)

@app.route('/add', methods=['POST'])
def add_medicine():
    data = request.json
    medicines = load_medicines()
    medicines.append({
        'id': len(medicines) + 1,
        'name': data['name'],
        'price': data['price'],
        'quantity': data['quantity']
    })
    save_medicines(medicines)
    return jsonify({'status': 'success', 'message': 'Medicine added successfully'})

@app.route('/get-medicines', methods=['GET'])
def get_medicines():
    return jsonify(load_medicines())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)