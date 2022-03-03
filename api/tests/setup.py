from api import db
from .data import user_one, customer_one, vehicle_one, rental_one


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
    response = client.post(
        "/api/auth/authenticate",
        json={"email": user_one["email"], "password": user_one["password"]},
    )

    return response.json


def create_customer(client, token):
    response = client.post(
        "/api/customer/",
        json={
            "company": customer_one["company"],
            "email": customer_one["email"],
            "name": customer_one["name"],
            "telephone": customer_one["telephone"],
        },
        headers={"Authorization": f"Bearer {token}"},
    )

    return response.json


def create_vehicle(client, token):
    response = client.post(
        "/api/vehicle/",
        json=vehicle_one,
        headers={"Authorization": f"Bearer {token}"},
    )

    return response.json


def create_rental(client, vehicle, customer, token):
    response = client.post(
        "/api/rental/",
        json={
            "vehicle_id": vehicle["id"],
            "customer_id": customer["id"],
            "start_date": rental_one["start_date"].strftime("%Y-%m-%d"),
            "proposed_return_date": rental_one["proposed_return_date"].strftime(
                "%Y-%m-%d"
            ),
            "actual_return_date": rental_one["actual_return_date"].strftime("%Y-%m-%d"),
        },
        headers={"Authorization": f"Bearer {token}"},
    )

    return response.json
