import pytest

from app.config import ConfigError, load_config
from app.recommendations import RecommendationEngine


def test_health(client):
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}


def test_unknown_route_returns_json_404(client):
    response = client.get("/api/nope")
    assert response.status_code == 404
    assert response.get_json()["error"] == "Not found"


def test_production_requires_secrets(monkeypatch):
    monkeypatch.setenv("APP_ENV", "production")
    monkeypatch.delenv("SECRET_KEY", raising=False)
    monkeypatch.delenv("DATABASE_URL", raising=False)
    with pytest.raises(ConfigError) as error:
        load_config()
    assert "SECRET_KEY" in str(error.value) and "DATABASE_URL" in str(error.value)


# ---- auth ----

def test_register_and_login(client):
    body = {"username": "alice", "email": "Alice@Example.com", "password": "correct-horse"}
    response = client.post("/api/auth/register", json=body)
    assert response.status_code == 201
    assert response.get_json()["user"]["email"] == "alice@example.com"
    assert "password" not in response.get_data(as_text=True)

    login = client.post("/api/auth/login", json={"username": "alice", "password": "correct-horse"})
    assert login.status_code == 200
    token = login.get_json()["token"]
    me = client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert me.get_json()["username"] == "alice"


def test_login_by_email(client, make_user):
    make_user("alice")
    response = client.post("/api/auth/login", json={"email": "alice@example.com", "password": "correct-horse"})
    assert response.status_code == 200


@pytest.mark.parametrize(
    "body",
    [
        {},
        {"username": "ab", "email": "a@b.co", "password": "longenough"},
        {"username": "alice", "email": "not-an-email", "password": "longenough"},
        {"username": "alice", "email": "a@b.co", "password": "short"},
    ],
)
def test_register_validation(client, body):
    assert client.post("/api/auth/register", json=body).status_code == 400


def test_register_duplicate(client, make_user):
    make_user("alice")
    again = client.post(
        "/api/auth/register", json={"username": "alice", "email": "other@example.com", "password": "correct-horse"}
    )
    assert again.status_code == 409


def test_login_wrong_password(client, make_user):
    make_user("alice")
    response = client.post("/api/auth/login", json={"username": "alice", "password": "wrong-password"})
    assert response.status_code == 401


def test_me_requires_valid_token(client):
    assert client.get("/api/auth/me").status_code == 401
    assert client.get("/api/auth/me", headers={"Authorization": "Bearer garbage"}).status_code == 401


# ---- lists ----

def test_create_list_requires_login(client):
    assert client.post("/api/lists/", json={"name": "Parlours"}).status_code == 401


def test_list_crud_and_ownership(client, make_user):
    alice = make_user("alice")
    bob = make_user("bob")

    created = client.post("/api/lists/", json={"name": "Parlours on Adyala Road", "price": "1500"}, headers=alice)
    assert created.status_code == 201
    list_id = created.get_json()["id"]
    assert created.get_json()["price"] == 1500.0

    assert client.get(f"/api/lists/{list_id}").status_code == 200
    assert client.get("/api/lists/9999").status_code == 404

    assert client.put(f"/api/lists/{list_id}", json={"name": "Hijacked"}, headers=bob).status_code == 403
    assert client.delete(f"/api/lists/{list_id}", headers=bob).status_code == 403

    updated = client.put(f"/api/lists/{list_id}", json={"name": "Renamed", "price": 2000}, headers=alice)
    assert updated.get_json()["name"] == "Renamed"

    assert client.delete(f"/api/lists/{list_id}", headers=alice).status_code == 204
    assert client.get(f"/api/lists/{list_id}").status_code == 404


def test_list_validation(client, make_user):
    alice = make_user("alice")
    assert client.post("/api/lists/", json={"name": ""}, headers=alice).status_code == 400
    assert client.post("/api/lists/", json={"name": "x", "price": -5}, headers=alice).status_code == 400
    assert client.post("/api/lists/", json={"name": "x", "price": "abc"}, headers=alice).status_code == 400


def test_private_lists_hidden_from_public(client, make_user):
    alice = make_user("alice")
    created = client.post("/api/lists/", json={"name": "Secret", "is_public": False}, headers=alice)
    list_id = created.get_json()["id"]

    assert client.get(f"/api/lists/{list_id}").status_code == 404
    assert client.get("/api/lists/").get_json()["total"] == 0
    mine = client.get("/api/lists/mine", headers=alice).get_json()["items"]
    assert [item["id"] for item in mine] == [list_id]


def test_pagination(client, make_user):
    alice = make_user("alice")
    for index in range(5):
        client.post("/api/lists/", json={"name": f"List {index}"}, headers=alice)
    page = client.get("/api/lists/?per_page=2&page=2").get_json()
    assert page["total"] == 5 and len(page["items"]) == 2 and page["page"] == 2


# ---- payments ----

def test_payment_uses_server_side_price(client, make_user):
    seller = make_user("seller")
    buyer = make_user("buyer")
    list_id = client.post("/api/lists/", json={"name": "Dentists", "price": 300}, headers=seller).get_json()["id"]

    response = client.post(
        "/api/payments/process", json={"list_id": list_id, "amount": 1, "user_id": 999}, headers=buyer
    )
    assert response.status_code == 201
    assert response.get_json()["amount"] == 300.0
    assert response.get_json()["status"] == "pending"

    mine = client.get("/api/payments/mine", headers=buyer).get_json()["items"]
    assert len(mine) == 1

    assert client.delete(f"/api/lists/{list_id}", headers=seller).status_code == 409


def test_payment_rules(client, make_user):
    seller = make_user("seller")
    list_id = client.post("/api/lists/", json={"name": "Dentists", "price": 300}, headers=seller).get_json()["id"]
    assert client.post("/api/payments/process", json={"list_id": list_id}).status_code == 401
    assert client.post("/api/payments/process", json={"list_id": list_id}, headers=seller).status_code == 400
    assert client.post("/api/payments/process", json={"list_id": 999}, headers=seller).status_code == 404


# ---- recommendations ----

def test_recommendation_engine_ranks_relevant_first():
    engine = RecommendationEngine(
        [
            {"id": 1, "name": "Petrol pumps", "description": "Fuel stations in Islamabad"},
            {"id": 2, "name": "Beauty parlours", "description": "Salons on Adyala road"},
        ]
    )
    result = engine.recommend("fuel stations")
    assert [item["id"] for item in result] == [1]


def test_recommendation_engine_edge_cases():
    assert RecommendationEngine([]).recommend("anything") == []
    assert RecommendationEngine([{"id": 1, "name": "x", "description": "y"}]).recommend("   ") == []
    assert RecommendationEngine([{"id": 1, "name": "", "description": ""}]).recommend("python") == []


def test_recommend_endpoint(client, make_user):
    alice = make_user("alice")
    client.post("/api/lists/", json={"name": "Petrol pumps", "description": "Fuel stations in Islamabad"}, headers=alice)
    client.post("/api/lists/", json={"name": "Parlours", "description": "Salons on Adyala road"}, headers=alice)

    assert client.post("/api/lists/recommend", json={}).status_code == 400
    result = client.post("/api/lists/recommend", json={"input": "fuel"}).get_json()
    assert [item["name"] for item in result] == ["Petrol pumps"]
