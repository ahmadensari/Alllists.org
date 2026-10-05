from flask import Blueprint, g, jsonify, request

from ..auth_utils import login_required
from ..models import List, Transaction, db

bp = Blueprint("payments", __name__)

ALLOWED_TYPES = ("purchase", "subscription")


@bp.post("/process")
@login_required
def process_payment():
    """Record a purchase request for the signed-in user.

    The amount comes from the list's price, never from the client. No payment gateway is
    connected yet, so the transaction stays "pending" until a gateway or an admin confirms it.
    """
    data = request.get_json(silent=True) or {}
    transaction_type = str(data.get("transaction_type", "purchase"))
    if transaction_type not in ALLOWED_TYPES:
        return jsonify({"error": "transaction_type must be one of: " + ", ".join(ALLOWED_TYPES)}), 400

    list_id = data.get("list_id")
    lst = db.session.get(List, list_id) if isinstance(list_id, int) else None
    if lst is None or not lst.is_public:
        return jsonify({"error": "List not found"}), 404
    if lst.creator_id == g.current_user.id:
        return jsonify({"error": "You cannot buy your own list"}), 400

    transaction = Transaction(
        user_id=g.current_user.id,
        list_id=lst.id,
        amount=lst.price,
        transaction_type=transaction_type,
    )
    db.session.add(transaction)
    db.session.commit()
    return jsonify(transaction.to_dict()), 201


@bp.get("/mine")
@login_required
def my_transactions():
    items = Transaction.query.filter_by(user_id=g.current_user.id).order_by(Transaction.id.desc()).all()
    return jsonify({"items": [item.to_dict() for item in items]})
