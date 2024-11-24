from flask import Blueprint, request, jsonify
from models.transaction import Transaction
from main import db

payment_routes = Blueprint('payment', __name__)

@payment_routes.route('/process', methods=['POST'])
def process_payment():
    data = request.json
    if not data or not data.get('user_id') or not data.get('list_id') or not data.get('amount') or not data.get('transaction_type'):
        return jsonify({"error": "user_id, list_id, amount, and transaction_type are required"}), 400
    
    new_transaction = Transaction(
        user_id=data['user_id'],
        list_id=data['list_id'],
        amount=data['amount'],
        transaction_type=data['transaction_type']
    )
    
    db.session.add(new_transaction)
    db.session.commit()
    
    return jsonify({"message": "Transaction processed successfully!"}), 201
