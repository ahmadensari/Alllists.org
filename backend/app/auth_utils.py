from datetime import datetime, timedelta, timezone
from functools import wraps

import jwt
from flask import current_app, g, jsonify, request

from .models import User, db


def create_token(user):
    expires = datetime.now(timezone.utc) + timedelta(hours=current_app.config["JWT_EXPIRY_HOURS"])
    payload = {"sub": str(user.id), "exp": expires}
    return jwt.encode(payload, current_app.config["SECRET_KEY"], algorithm="HS256")


def login_required(view):
    @wraps(view)
    def wrapper(*args, **kwargs):
        header = request.headers.get("Authorization", "")
        if not header.startswith("Bearer "):
            return jsonify({"error": "Authentication required"}), 401
        try:
            payload = jwt.decode(
                header[len("Bearer "):], current_app.config["SECRET_KEY"], algorithms=["HS256"]
            )
            user = db.session.get(User, int(payload["sub"]))
        except (jwt.PyJWTError, KeyError, ValueError):
            return jsonify({"error": "Invalid or expired token"}), 401
        if user is None:
            return jsonify({"error": "Invalid or expired token"}), 401
        g.current_user = user
        return view(*args, **kwargs)

    return wrapper
