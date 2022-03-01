from .setup import truncate_db, create_user
from .data import user_one, user_two
from api.auth.models import User


def test_create_user_success(client):
    truncate_db()

    response = client.post(
        "/api/auth/",
        json={
            "email": user_one["email"],
            "username": user_one["username"],
            "password": user_one["password"],
        },
    )

    assert response.status == "200 OK"
    assert response.json["email"] == user_one["email"]
    assert response.json["username"] == user_one["username"]

    truncate_db()


def test_create_user_validation_error(client):
    truncate_db()

    response = client.post(
        "/api/auth/",
        json={
            "email": user_one["email"],
            "password": user_one["password"],
        },
    )
    print(response.json)
    assert response.status == "400 BAD REQUEST"
    assert response.json["detail"] == {
        "json": {"username": ["Missing data for required field."]}
    }
    assert response.json["message"] == "Validation error"

    truncate_db()


def test_user_authenticate_success(client):
    truncate_db()

    # Create user
    create_user(client)

    response = client.post(
        "/api/auth/authenticate",
        json={
            "email": user_one["email"],
            "password": user_one["password"],
        },
    )

    # Retrieve created user
    created_user = User.find_user_by_email(user_one["email"])

    assert response.status == "200 OK"
    assert response.json["email"] == created_user.email
    assert response.json["public_id"] == created_user.public_id
    assert response.json["username"] == created_user.username
    assert response.json["token"]

    truncate_db()


def test_user_authenticate_validation_error(client):
    truncate_db()

    # Create user
    create_user(client)

    response = client.post(
        "/api/auth/authenticate",
        json={
            "email": user_one["email"],
        },
    )

    assert response.status == "400 BAD REQUEST"
    assert response.json["detail"] == {
        "json": {"password": ["Missing data for required field."]}
    }
    assert response.json["message"] == "Validation error"

    truncate_db()


def test_user_authenticate_not_found(client):
    truncate_db()

    # Create user
    create_user(client)

    response = client.post(
        "/api/auth/authenticate",
        json={
            "email": user_two["email"],
            "password": user_two["password"],
        },
    )

    # Retrieve created user
    created_user = User.find_user_by_email(user_one["email"])

    assert response.status == "404 NOT FOUND"
    assert response.json["message"] == "A user with the given email does not exist"

    truncate_db()
