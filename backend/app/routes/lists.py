from decimal import Decimal, InvalidOperation

from flask import Blueprint, g, jsonify, request

from ..auth_utils import login_required
from ..models import List, Transaction, db
from ..recommendations import RecommendationEngine

bp = Blueprint("lists", __name__)

MAX_PER_PAGE = 100
RECOMMENDATION_POOL = 2000


def _parse_price(value):
    try:
        price = Decimal(str(value))
    except InvalidOperation:
        return None
    if price < 0 or price > Decimal("99999999.99"):
        return None
    return price.quantize(Decimal("0.01"))


def _can_manage(lst):
    return g.current_user.id == lst.creator_id or g.current_user.role == "admin"


@bp.get("/", strict_slashes=False)
def get_lists():
    page = max(request.args.get("page", 1, type=int), 1)
    per_page = min(max(request.args.get("per_page", 20, type=int), 1), MAX_PER_PAGE)
    query = List.query.filter_by(is_public=True).order_by(List.id.desc())
    total = query.count()
    items = query.offset((page - 1) * per_page).limit(per_page).all()
    return jsonify(
        {"items": [item.to_dict() for item in items], "page": page, "per_page": per_page, "total": total}
    )


@bp.get("/<int:list_id>")
def get_list(list_id):
    lst = db.session.get(List, list_id)
    if lst is None or not lst.is_public:
        # Private lists are only visible to their owner, through /mine.
        return jsonify({"error": "List not found"}), 404
    return jsonify(lst.to_dict())


@bp.get("/mine")
@login_required
def my_lists():
    items = List.query.filter_by(creator_id=g.current_user.id).order_by(List.id.desc()).all()
    return jsonify({"items": [item.to_dict() for item in items]})


@bp.post("/", strict_slashes=False)
@login_required
def create_list():
    data = request.get_json(silent=True) or {}
    name = str(data.get("name", "")).strip()
    if not name or len(name) > 100:
        return jsonify({"error": "Name is required and must be at most 100 characters"}), 400

    price = _parse_price(data.get("price", 0))
    if price is None:
        return jsonify({"error": "Price must be a number of zero or more"}), 400

    lst = List(
        name=name,
        description=str(data.get("description", "")).strip(),
        price=price,
        is_public=bool(data.get("is_public", True)),
        creator_id=g.current_user.id,
    )
    db.session.add(lst)
    db.session.commit()
    return jsonify(lst.to_dict()), 201


@bp.put("/<int:list_id>")
@login_required
def update_list(list_id):
    lst = db.session.get(List, list_id)
    if lst is None:
        return jsonify({"error": "List not found"}), 404
    if not _can_manage(lst):
        return jsonify({"error": "You do not own this list"}), 403

    data = request.get_json(silent=True) or {}
    if "name" in data:
        name = str(data["name"]).strip()
        if not name or len(name) > 100:
            return jsonify({"error": "Name is required and must be at most 100 characters"}), 400
        lst.name = name
    if "description" in data:
        lst.description = str(data["description"]).strip()
    if "price" in data:
        price = _parse_price(data["price"])
        if price is None:
            return jsonify({"error": "Price must be a number of zero or more"}), 400
        lst.price = price
    if "is_public" in data:
        lst.is_public = bool(data["is_public"])

    db.session.commit()
    return jsonify(lst.to_dict())


@bp.delete("/<int:list_id>")
@login_required
def delete_list(list_id):
    lst = db.session.get(List, list_id)
    if lst is None:
        return jsonify({"error": "List not found"}), 404
    if not _can_manage(lst):
        return jsonify({"error": "You do not own this list"}), 403
    if Transaction.query.filter_by(list_id=lst.id).first():
        return jsonify({"error": "A list with sales cannot be deleted; make it private instead"}), 409

    db.session.delete(lst)
    db.session.commit()
    return "", 204


@bp.post("/recommend")
def recommend():
    data = request.get_json(silent=True) or {}
    query = str(data.get("input", "")).strip()
    if not query:
        return jsonify({"error": "Input is required"}), 400

    pool = List.query.filter_by(is_public=True).order_by(List.id.desc()).limit(RECOMMENDATION_POOL).all()
    engine = RecommendationEngine([item.to_dict() for item in pool])
    return jsonify(engine.recommend(query))
