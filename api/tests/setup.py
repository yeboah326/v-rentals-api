from api import db
from .data import user_one, user_two, customer_one


def truncate_db():
    meta = db.metadata
    for table in meta.sorted_tables[::-1]:
        db.session.execute(table.delete())
    db.session()


def create_user(client):
    client.post(
        "/api/auth/",
        json={
            "email": user_one["email"],
            "username": user_one["username"],
            "password": user_one["password"],
        },
    )


def authenticate_user(client):
    create_user(client)

    response = client.post(
        "/api/auth/authenticate",
        json={"email": user_one["email"], "password": user_one["password"]},
    )

    return response.json


def create_customer(client):
    authenticated_user = authenticate_user(client)

    response = client.post(
        "/api/customer/",
        json={
            "company": customer_one["company"],
            "email": customer_one["email"],
            "name": customer_one["name"],
            "telephone": customer_one["telephone"],
        },
        headers={"Authorization": f"Bearer {authenticated_user['token']}"},
    )

    return authenticated_user
