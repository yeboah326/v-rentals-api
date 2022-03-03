from api.rental.models import Rental
from .setup import (
    create_rental,
    truncate_db,
    create_user,
    authenticate_user,
    create_customer,
    create_vehicle,
)
from .data import rental_one, rental_two


def test_rental_create_success(client):
    truncate_db()

    create_user(client)
    authenticated_user = authenticate_user(client)
    customer = create_customer(client, authenticated_user["token"])
    vehicle = create_vehicle(client, authenticated_user["token"])

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
        headers={"Authorization": f"Bearer {authenticated_user['token']}"},
    )

    assert response.status == "200 OK"
    assert response.json["actual_charge"]
    assert response.json["actual_return_date"]
    assert response.json["customer_id"]
    assert response.json["id"]
    assert response.json["penalty_charge"]
    assert response.json["proposed_return_date"]
    assert response.json["start_date"]
    assert response.json["vehicle_id"]

    truncate_db()


def test_rental_create_validation_error(client):
    truncate_db()

    create_user(client)
    authenticated_user = authenticate_user(client)
    customer = create_customer(client, authenticated_user["token"])
    vehicle = create_vehicle(client, authenticated_user["token"])

    response = client.post(
        "/api/rental/",
        json={
            "vehicle_id": vehicle["id"],
            "start_date": rental_one["start_date"].strftime("%Y-%m-%d"),
            "proposed_return_date": rental_one["proposed_return_date"].strftime(
                "%Y-%m-%d"
            ),
            "actual_return_date": rental_one["actual_return_date"].strftime("%Y-%m-%d"),
        },
        headers={"Authorization": f"Bearer {authenticated_user['token']}"},
    )

    assert response.status == "400 BAD REQUEST"
    assert response.json["detail"] == {
        "json": {"customer_id": ["Missing data for required field."]}
    }
    assert response.json["message"] == "Validation error"

    truncate_db()


def test_rental_create_authentication_error(client):
    truncate_db()

    create_user(client)
    authenticated_user = authenticate_user(client)
    customer = create_customer(client, authenticated_user["token"])
    vehicle = create_vehicle(client, authenticated_user["token"])

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
    )

    assert response.status == "401 UNAUTHORIZED"
    assert response.json["message"] == "Missing Authorization Header"

    truncate_db()


def test_rental_get_by_id_success(client):
    truncate_db()

    create_user(client)
    authenticated_user = authenticate_user(client)
    customer = create_customer(client, authenticated_user["token"])
    vehicle = create_vehicle(client, authenticated_user["token"])
    rental = create_rental(client, vehicle, customer, authenticated_user["token"])

    response = client.get(
        f"/api/rental/{rental['id']}",
        headers={"Authorization": f"Bearer {authenticated_user['token']}"},
    )

    assert response.status == "200 OK"
    assert response.json == rental

    truncate_db()


def test_rental_get_by_id_authentication_error(client):
    truncate_db()

    create_user(client)
    authenticated_user = authenticate_user(client)
    customer = create_customer(client, authenticated_user["token"])
    vehicle = create_vehicle(client, authenticated_user["token"])
    rental = create_rental(client, vehicle, customer, authenticated_user["token"])

    response = client.get(f"/api/rental/{rental['id']}")

    assert response.status == "401 UNAUTHORIZED"
    assert response.json["message"] == "Missing Authorization Header"

    truncate_db()


def test_rental_get_by_id_not_found(client):
    truncate_db()

    create_user(client)
    authenticated_user = authenticate_user(client)
    customer = create_customer(client, authenticated_user["token"])
    vehicle = create_vehicle(client, authenticated_user["token"])
    rental = create_rental(client, vehicle, customer, authenticated_user["token"])

    response = client.get(
        f"/api/rental/{rental['id'] + 1}",
        headers={"Authorization": f"Bearer {authenticated_user['token']}"},
    )

    assert response.status == "404 NOT FOUND"
    assert response.json["message"] == "A rental with the given ID does not exist"

    truncate_db()


def test_rental_get_all_success(client):
    truncate_db()

    create_user(client)
    authenticated_user = authenticate_user(client)
    customer = create_customer(client, authenticated_user["token"])
    vehicle = create_vehicle(client, authenticated_user["token"])
    rental = create_rental(client, vehicle, customer, authenticated_user["token"])

    response = client.get(
        "/api/rental/",
        headers={"Authorization": f"Bearer {authenticated_user['token']}"},
    )

    assert response.status == "200 OK"
    assert response.json["rentals"][0] == rental

    truncate_db()


def test_rental_get_all_authentication_error(client):
    truncate_db()

    create_user(client)
    authenticated_user = authenticate_user(client)
    customer = create_customer(client, authenticated_user["token"])
    vehicle = create_vehicle(client, authenticated_user["token"])
    rental = create_rental(client, vehicle, customer, authenticated_user["token"])

    response = client.get("/api/rental/")

    assert response.status == "401 UNAUTHORIZED"
    assert response.json["message"] == "Missing Authorization Header"

    truncate_db()


def test_rental_modify_by_id_success(client):
    truncate_db()

    create_user(client)
    authenticated_user = authenticate_user(client)
    customer = create_customer(client, authenticated_user["token"])
    vehicle = create_vehicle(client, authenticated_user["token"])
    rental = create_rental(client, vehicle, customer, authenticated_user["token"])

    response = client.put(
        f"/api/rental/{rental['id']}",
        json={
            "vehicle_id": vehicle["id"],
            "customer_id": customer["id"],
            "start_date": rental_two["start_date"].strftime("%Y-%m-%d"),
            "proposed_return_date": rental_two["proposed_return_date"].strftime(
                "%Y-%m-%d"
            ),
            "actual_return_date": rental_two["actual_return_date"].strftime("%Y-%m-%d"),
        },
        headers={"Authorization": f"Bearer {authenticated_user['token']}"},
    )

    modified_rental = Rental.get_rental_by_id(rental['id'])

    assert response.status ==  "200 OK"
    assert response.json['actual_charge'] == float(modified_rental.actual_charge)
    assert response.json['actual_return_date'] == modified_rental.actual_return_date.strftime("%Y-%m-%d")
    assert response.json['customer_id'] == modified_rental.customer_id
    assert response.json['penalty_charge'] == float(modified_rental.penalty_charge)
    assert response.json['proposed_return_date'] == modified_rental.proposed_return_date.strftime("%Y-%m-%d")
    assert response.json['start_date'] == modified_rental.start_date.strftime("%Y-%m-%d")
    assert response.json['vehicle_id'] == modified_rental.vehicle_id

    truncate_db()


def test_rental_modify_by_id_validation_error(client):
    truncate_db()

    create_user(client)
    authenticated_user = authenticate_user(client)
    customer = create_customer(client, authenticated_user["token"])
    vehicle = create_vehicle(client, authenticated_user["token"])
    rental = create_rental(client, vehicle, customer, authenticated_user["token"])

    response = client.put(
        f"/api/rental/{rental['id']}",
        json={
            "vehicle_id": vehicle["id"],
            "start_date": rental_two["start_date"].strftime("%Y-%m-%d"),
            "proposed_return_date": rental_two["proposed_return_date"].strftime(
                "%Y-%m-%d"
            ),
            "actual_return_date": rental_two["actual_return_date"].strftime("%Y-%m-%d"),
        }
    )
    
    assert response.status ==  "400 BAD REQUEST"
    assert response.json['message'] == "Validation error"
    assert response.json['detail'] == {'json': {'customer_id': ['Missing data for required field.']}}

    truncate_db()


def test_rental_modify_by_id_authentication_error(client):
    truncate_db()

    create_user(client)
    authenticated_user = authenticate_user(client)
    customer = create_customer(client, authenticated_user["token"])
    vehicle = create_vehicle(client, authenticated_user["token"])
    rental = create_rental(client, vehicle, customer, authenticated_user["token"])

    response = client.put(
        f"/api/rental/{rental['id']}",
        json={
            "vehicle_id": vehicle["id"],
            "customer_id": customer["id"],
            "start_date": rental_two["start_date"].strftime("%Y-%m-%d"),
            "proposed_return_date": rental_two["proposed_return_date"].strftime(
                "%Y-%m-%d"
            ),
            "actual_return_date": rental_two["actual_return_date"].strftime("%Y-%m-%d"),
        }
    )

    assert response.status ==  "401 UNAUTHORIZED"
    assert response.json['message'] == "Missing Authorization Header"

    truncate_db()


def test_rental_modify_by_id_not_found(client):
    truncate_db()

    create_user(client)
    authenticated_user = authenticate_user(client)
    customer = create_customer(client, authenticated_user["token"])
    vehicle = create_vehicle(client, authenticated_user["token"])
    rental = create_rental(client, vehicle, customer, authenticated_user["token"])

    response = client.put(
        f"/api/rental/{rental['id'] + 1}",
        json={
            "vehicle_id": vehicle["id"],
            "customer_id": customer["id"],
            "start_date": rental_two["start_date"].strftime("%Y-%m-%d"),
            "proposed_return_date": rental_two["proposed_return_date"].strftime(
                "%Y-%m-%d"
            ),
            "actual_return_date": rental_two["actual_return_date"].strftime("%Y-%m-%d"),
        },
        headers={"Authorization": f"Bearer {authenticated_user['token']}"},
    )

    assert response.status ==  "404 NOT FOUND"
    assert response.json['message'] == "A rental with the given ID does not exist"

    truncate_db()
