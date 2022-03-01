from api.vehicle.models import Vehicle
from .setup import authenticate_user, truncate_db, create_vehicle
from .data import vehicle_one, vehicle_two


def test_vehicle_create_success(client):
    truncate_db()

    authenticated_user = authenticate_user(client)

    response = client.post(
        "/api/vehicle/",
        json=vehicle_one,
        headers={"Authorization": f"Bearer {authenticated_user['token']}"},
    )

    created_vehicle = Vehicle.get_vehicle_by_id(response.json["id"])

    assert response.status == "200 OK"
    assert response.json["name"] == created_vehicle.name
    assert response.json["cost_per_day"] == float(created_vehicle.cost_per_day)
    assert response.json["penalty_per_day"] == float(created_vehicle.penalty_per_day)
    assert response.json["rented"] == created_vehicle.rented
    assert response.json["vehicle_type"][12:] == created_vehicle.vehicle_type.name

    truncate_db()


def test_vehicle_create_validation_error(client):
    truncate_db()

    authenticated_user = authenticate_user(client)

    response = client.post(
        "/api/vehicle/",
        json={
            "cost_per_day": vehicle_one["cost_per_day"],
            "penalty_per_day": vehicle_one["penalty_per_day"],
            "vehicle_type": vehicle_one["vehicle_type"],
            "rented": vehicle_one["rented"],
        },
        headers={"Authorization": f"Bearer {authenticated_user['token']}"},
    )

    assert response.status == "400 BAD REQUEST"
    assert response.json["detail"] == {
        "json": {"name": ["Missing data for required field."]}
    }
    assert response.json["message"] == "Validation error"

    truncate_db()


def test_vehicle_create_authentication_error(client):
    truncate_db()

    authenticated_user = authenticate_user(client)

    response = client.post(
        "/api/vehicle/",
        json=vehicle_one,
    )

    assert response.status == "401 UNAUTHORIZED"
    assert response.json["message"] == "Missing Authorization Header"

    truncate_db()


def test_vehicle_get_by_id_success(client):
    truncate_db()

    # Get the authenticated user and created vehicle
    user_and_vehicle = create_vehicle(client)
    authenticated_user = user_and_vehicle["authenticated_user"]
    vehicle = user_and_vehicle["vehicle"]

    response = client.get(
        f"/api/vehicle/{vehicle['id']}",
        headers={"Authorization": f"Bearer {authenticated_user['token']}"},
    )

    assert response.status == "200 OK"
    assert response.json["cost_per_day"] == vehicle["cost_per_day"]
    assert response.json["name"] == vehicle["name"]
    assert response.json["penalty_per_day"] == vehicle["penalty_per_day"]
    assert response.json["rented"] == vehicle["rented"]

    truncate_db()


def test_vehicle_get_by_id_authentication_error(client):
    truncate_db()

    # Get the authenticated user and created vehicle
    user_and_vehicle = create_vehicle(client)
    authenticated_user = user_and_vehicle["authenticated_user"]
    vehicle = user_and_vehicle["vehicle"]

    response = client.get(f"/api/vehicle/{vehicle['id']}")

    assert response.status == "401 UNAUTHORIZED"
    assert response.json["message"] == "Missing Authorization Header"

    truncate_db()


def test_vehicle_get_by_id_not_found(client):
    truncate_db()

    # Get the authenticated user and created vehicle
    user_and_vehicle = create_vehicle(client)
    authenticated_user = user_and_vehicle["authenticated_user"]
    vehicle = user_and_vehicle["vehicle"]

    response = client.get(
        f"/api/vehicle/{vehicle['id'] + 1}",
        headers={"Authorization": f"Bearer {authenticated_user['token']}"},
    )

    assert response.status == "404 NOT FOUND"
    assert response.json["message"] == "A vehicle with the given ID does not exist"

    truncate_db()


def test_vehicle_get_all_success(client):
    truncate_db()

    # Get the authenticated user and created vehicle
    user_and_vehicle = create_vehicle(client)
    authenticated_user = user_and_vehicle["authenticated_user"]
    vehicle = user_and_vehicle["vehicle"]

    response = client.get(
        f"/api/vehicle/",
        headers={"Authorization": f"Bearer {authenticated_user['token']}"},
    )

    assert response.status == "200 OK"
    assert len(response.json["vehicles"]) == 1

    truncate_db()


def test_vehicle_get_all_authentication_error(client):
    truncate_db()

    # Get the authenticated user and created vehicle
    user_and_vehicle = create_vehicle(client)
    authenticated_user = user_and_vehicle["authenticated_user"]
    vehicle = user_and_vehicle["vehicle"]

    response = client.get("/api/vehicle/")

    assert response.status == "401 UNAUTHORIZED"
    assert response.json["message"] == "Missing Authorization Header"

    truncate_db()


def test_vehicle_modify_by_id_success(client):
    truncate_db()

    # Get the authenticated user and created vehicle
    user_and_vehicle = create_vehicle(client)
    authenticated_user = user_and_vehicle["authenticated_user"]
    vehicle = user_and_vehicle["vehicle"]

    response = client.put(
        f"/api/vehicle/{vehicle['id']}",
        json=vehicle_two,
        headers={"Authorization": f"Bearer {authenticated_user['token']}"},
    )

    assert response.status == "200 OK"
    assert response.json["cost_per_day"] == vehicle_two["cost_per_day"]
    assert response.json["name"] == vehicle_two["name"]
    assert response.json["penalty_per_day"] == vehicle_two["penalty_per_day"]
    assert response.json["rented"] == vehicle_two["rented"]

    truncate_db()


def test_vehicle_modify_by_id_validation_error(client):
    truncate_db()

    # Get the authenticated user and created vehicle
    user_and_vehicle = create_vehicle(client)
    authenticated_user = user_and_vehicle["authenticated_user"]
    vehicle = user_and_vehicle["vehicle"]

    response = client.put(
        f"/api/vehicle/{vehicle['id']}",
        json={
            "cost_per_day": vehicle_two["cost_per_day"],
            "penalty_per_day": vehicle_two["penalty_per_day"],
            "vehicle_type": vehicle_two["vehicle_type"],
            "rented": vehicle_two["rented"],
        },
        headers={"Authorization": f"Bearer {authenticated_user['token']}"},
    )

    assert response.status == "400 BAD REQUEST"
    assert response.json["detail"] == {
        "json": {"name": ["Missing data for required field."]}
    }
    assert response.json["message"] == "Validation error"

    truncate_db()


def test_vehicle_modify_by_id_authentication_error(client):
    truncate_db()

    # Get the authenticated user and created vehicle
    user_and_vehicle = create_vehicle(client)
    authenticated_user = user_and_vehicle["authenticated_user"]
    vehicle = user_and_vehicle["vehicle"]

    response = client.put(
        f"/api/vehicle/{vehicle['id']}",
        json=vehicle_two,
    )

    assert response.status == "401 UNAUTHORIZED"
    assert response.json["message"] == "Missing Authorization Header"

    truncate_db()


def test_vehicle_modify_by_id_not_found(client):
    truncate_db()

    # Get the authenticated user and created vehicle
    user_and_vehicle = create_vehicle(client)
    authenticated_user = user_and_vehicle["authenticated_user"]
    vehicle = user_and_vehicle["vehicle"]

    response = client.put(
        f"/api/vehicle/{vehicle['id'] + 1}",
        json=vehicle_two,
        headers={"Authorization": f"Bearer {authenticated_user['token']}"},
    )

    assert response.status == "404 NOT FOUND"
    assert response.json["message"] == "A vehicle with the given ID does not exist"

    truncate_db()


def test_vehicle_delete_by_id_success(client):
    truncate_db()

    # Get the authenticated user and created vehicle
    user_and_vehicle = create_vehicle(client)
    authenticated_user = user_and_vehicle["authenticated_user"]
    vehicle = user_and_vehicle["vehicle"]

    response = client.delete(
        f"/api/vehicle/{vehicle['id']}",
        headers={"Authorization": f"Bearer {authenticated_user['token']}"},
    )

    print(response.status)
    print(response.json)

    assert response.status == "200 OK"
    assert response.json["message"] == "Vehicle deleted successfully"

    truncate_db()


def test_vehicle_delete_by_id_authentication_error(client):
    truncate_db()

    # Get the authenticated user and created vehicle
    user_and_vehicle = create_vehicle(client)
    authenticated_user = user_and_vehicle["authenticated_user"]
    vehicle = user_and_vehicle["vehicle"]

    response = client.delete(
        f"/api/vehicle/{vehicle['id']}",
    )

    print(response.status)
    print(response.json)

    assert response.status == "401 UNAUTHORIZED"
    assert response.json["message"] == "Missing Authorization Header"

    truncate_db()


def test_vehicle_delete_by_id_not_found(client):
    truncate_db()

    # Get the authenticated user and created vehicle
    user_and_vehicle = create_vehicle(client)
    authenticated_user = user_and_vehicle["authenticated_user"]
    vehicle = user_and_vehicle["vehicle"]

    response = client.delete(
        f"/api/vehicle/{vehicle['id'] + 1}",
        headers={"Authorization": f"Bearer {authenticated_user['token']}"},
    )

    assert response.status == "404 NOT FOUND"
    assert response.json["message"] == "A vehicle with the given ID does not exist"

    truncate_db()
