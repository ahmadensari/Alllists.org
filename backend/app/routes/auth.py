import logging
import re

from flask import Blueprint, g, jsonify, request
from sqlalchemy import or_
from sqlalchemy.exc import IntegrityError

from ..auth_utils import create_token, login_required
from ..models import User, db

bp = Blueprint("auth", __name__)

USERNAME_RE = re.compile(r"^[A-Za-z0-9_.-]{3,50}$")
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


@bp.post("/register")
def register():
    data = request.get_json(silent=True) or {}
    username = str(data.get("username", "")).strip()
    email = str(data.get("email", "")).strip().lower()
    password = str(data.get("password", ""))

    if not username or not email or not password:
        return jsonify({"error": "Username, email, and password are required"}), 400
    if not USERNAME_RE.match(username):
        return jsonify({"error": "Username must be 3-50 letters, numbers, dots, dashes or underscores"}), 400
    if len(email) > 100 or not EMAIL_RE.match(email):
        return jsonify({"error": "Email address is not valid"}), 400
    if len(password) < 8:
        return jsonify({"error": "Password must be at least 8 characters"}), 400

    if User.query.filter(or_(User.username == username, User.email == email)).first():
        return jsonify({"error": "Username or email already exists"}), 409

    user = User(username=username, email=email)
    user.set_password(password)
    db.session.add(user)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Username or email already exists"}), 409

    logging.info("Registered user %s", user.id)
    return jsonify({"message": "User registered successfully", "user": user.to_dict()}), 201


@bp.post("/login")
def login():
    data = request.get_json(silent=True) or {}
    identifier = str(data.get("username") or data.get("email") or "").strip()
    password = str(data.get("password", ""))

    user = User.query.filter(
        or_(User.username == identifier, User.email == identifier.lower())
    ).first()
    if user is None or not user.check_password(password):
        return jsonify({"error": "Invalid credentials"}), 401

    return jsonify({"token": create_token(user), "user": user.to_dict()})


@bp.get("/me")
@login_required
def me():
    return jsonify(g.current_user.to_dict())
