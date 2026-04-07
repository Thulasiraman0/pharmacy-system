from flask import Flask, render_template, request, jsonify
import json
import os
from datetime import datetime

app = Flask(__name__)

MEDICINES_FILE = 'medicines.json'
BILLS_FILE = 'bills.json'

def load_medicines():
    if os.path.exists(MEDICINES_FILE):
        with open(MEDICINES_FILE, 'r') as f:
            return json.load(f)
    return []

def load_bills():
    if os.path.exists(BILLS_FILE):
        with open(BILLS_FILE, 'r') as f:
            return json.load(f)
    return []

def save_bills(bills):
    with open(BILLS_FILE, 'w') as f:
        json.dump(bills, f, indent=2)

@app.route('/')
def index():
    medicines = load_medicines()
    bills = load_bills()
    return render_template('index.html', medicines=medicines, bills=bills)

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
    with open(MEDICINES_FILE, 'w') as f:
        json.dump(medicines, f)
    return jsonify({'status': 'success'})

@app.route('/get-medicines', methods=['GET'])
def get_medicines():
    return jsonify(load_medicines())

@app.route('/generate-bill', methods=['POST'])
def generate_bill():
    data = request.json
    medicines = load_medicines()
    
    bill_items = []
    total = 0
    
    for item in data['items']:
        medicine = next((m for m in medicines if m['id'] == item['id']), None)
        if medicine:
            amount = medicine['price'] * item['quantity']
            total += amount
            bill_items.append({
                'name': medicine['name'],
                'price': medicine['price'],
                'quantity': item['quantity'],
                'amount': amount
            })
    
    bill = {
        'id': len(load_bills()) + 1,
        'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'items': bill_items,
        'total': round(total, 2)
    }
    
    bills = load_bills()
    bills.append(bill)
    save_bills(bills)
    
    return jsonify({'status': 'success', 'bill': bill})

@app.route('/get-bills', methods=['GET'])
def get_bills():
    return jsonify(load_bills())

@app.route('/get-bill/<int:bill_id>', methods=['GET'])
def get_bill(bill_id):
    bills = load_bills()
    bill = next((b for b in bills if b['id'] == bill_id), None)
    if bill:
        return jsonify(bill)
    return jsonify({'error': 'Bill not found'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)