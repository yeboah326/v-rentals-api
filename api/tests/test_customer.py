from math import trunc
from api.customer.models import Customer
from .setup import create_user, truncate_db, authenticate_user, create_customer
from .data import customer_one, customer_two


def test_customer_create_success(client):
    truncate_db()

    # Authenticate created user
    create_user(client)
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

    # Created customer
    created_customer = Customer.find_customer_by_email(customer_one["email"])

    assert response.status == "200 OK"
    assert response.json["company"] == created_customer.company
    assert response.json["email"] == created_customer.email
    assert response.json["id"] == created_customer.id
    assert response.json["name"] == created_customer.name
    assert response.json["telephone"] == created_customer.telephone

    truncate_db()


def test_customer_create_validation_error(client):
    truncate_db()

    # Authenticate created user
    create_user(client)
    authenticated_user = authenticate_user(client)

    response = client.post(
        "/api/customer/",
        json={
            "company": customer_one["company"],
            "email": customer_one["email"],
            "telephone": customer_one["telephone"],
        },
        headers={"Authorization": f"Bearer {authenticated_user['token']}"},
    )

    assert response.status == "400 BAD REQUEST"
    assert response.json["detail"] == {
        "json": {"name": ["Missing data for required field."]}
    }
    assert response.json["message"] == "Validation error"

    truncate_db()


def test_customer_create_authentication_error(client):
    truncate_db()

    # Authenticate created user
    create_user(client)
    authenticated_user = authenticate_user(client)

    response = client.post(
        "/api/customer/",
        json={
            "company": customer_one["company"],
            "email": customer_one["email"],
            "name": customer_one["name"],
            "telephone": customer_one["telephone"],
        },
    )

    assert response.status == "401 UNAUTHORIZED"
    assert response.json["message"] == "Missing Authorization Header"

    truncate_db()


def test_customer_get_by_id_success(client):
    truncate_db()

    # Authenticated user
    create_user(client)
    authenticated_user = authenticate_user(client)
    create_customer(client, authenticated_user['token'])

    # Created customer
    created_customer = Customer.find_customer_by_email(customer_one["email"])

    response = client.get(
        f"/api/customer/{created_customer.id}",
        headers={"Authorization": f"Bearer {authenticated_user['token']}"},
    )

    assert response.status == "200 OK"
    assert response.json["company"] == created_customer.company
    assert response.json["email"] == created_customer.email
    assert response.json["id"] == created_customer.id
    assert response.json["name"] == created_customer.name
    assert response.json["telephone"] == created_customer.telephone

    truncate_db()


def test_customer_get_by_id_authentication_error(client):
    truncate_db()

    # Authenticated user
    create_user(client)
    authenticated_user = authenticate_user(client)
    create_customer(client, authenticated_user['token'])

    # Created customer
    created_customer = Customer.find_customer_by_email(customer_one["email"])

    response = client.get(f"/api/customer/{created_customer.id}")

    assert response.status == "401 UNAUTHORIZED"
    assert response.json["message"] == "Missing Authorization Header"

    truncate_db()


def test_customer_get_by_id_not_found(client):
    truncate_db()

    # Authenticated user
    create_user(client)
    authenticated_user = authenticate_user(client)
    create_customer(client, authenticated_user['token'])

    # Created customer
    created_customer = Customer.find_customer_by_email(customer_one["email"])

    response = client.get(
        f"/api/customer/{created_customer.id + 1}",
        headers={"Authorization": f"Bearer {authenticated_user['token']}"},
    )

    assert response.status == "404 NOT FOUND"
    assert response.json["message"] == "A customer with the given ID does not exist"

    truncate_db()


def test_customer_get_all_success(client):
    truncate_db()

    # Authenticated user
    create_user(client)
    authenticated_user = authenticate_user(client)
    create_customer(client, authenticated_user['token'])

    response = client.get(
        f"/api/customer/",
        headers={"Authorization": f"Bearer {authenticated_user['token']}"},
    )

    assert response.status == "200 OK"
    assert response.json["customers"][0]["company"] == customer_one["company"]
    assert response.json["customers"][0]["email"] == customer_one["email"]
    assert response.json["customers"][0]["name"] == customer_one["name"]
    assert response.json["customers"][0]["telephone"] == customer_one["telephone"]

    truncate_db()


def test_customer_get_all_authentication_error(client):
    truncate_db()

    create_user(client)
    authenticated_user = authenticate_user(client)
    create_customer(client, authenticated_user['token'])

    response = client.get(f"/api/customer/")

    assert response.status == "401 UNAUTHORIZED"
    assert response.json["message"] == "Missing Authorization Header"

    truncate_db()


def test_customer_modify_by_id_success(client):
    truncate_db()

    # Authenticated user
    create_user(client)
    authenticated_user = authenticate_user(client)
    create_customer(client, authenticated_user['token'])

    # Created customer
    created_customer = Customer.find_customer_by_email(customer_one["email"])

    response = client.put(
        f"/api/customer/{created_customer.id}",
        headers={"Authorization": f"Bearer {authenticated_user['token']}"},
        json=customer_two,
    )

    assert response.status == "200 OK"
    assert response.json["company"] == customer_two["company"]
    assert response.json["email"] == customer_two["email"]
    assert response.json["name"] == customer_two["name"]
    assert response.json["telephone"] == customer_two["telephone"]

    truncate_db()


def test_customer_modify_by_id_validation_error(client):
    truncate_db()

    # Authenticated user
    create_user(client)
    authenticated_user = authenticate_user(client)
    create_customer(client, authenticated_user['token'])

    # Created customer
    created_customer = Customer.find_customer_by_email(customer_one["email"])

    response = client.put(
        f"/api/customer/{created_customer.id}",
        headers={"Authorization": f"Bearer {authenticated_user['token']}"},
        json={
            "company": customer_two["company"],
            "email": customer_two["email"],
            "telephone": customer_two["telephone"],
        },
    )

    assert response.status == "400 BAD REQUEST"
    assert response.json["detail"] == {
        "json": {"name": ["Missing data for required field."]}
    }
    assert response.json["message"] == "Validation error"

    truncate_db()


def test_customer_modify_by_id_authentication_error(client):
    truncate_db()

    # Authenticated user
    create_user(client)
    authenticated_user = authenticate_user(client)
    create_customer(client, authenticated_user['token'])

    # Created customer
    created_customer = Customer.find_customer_by_email(customer_one["email"])

    response = client.put(f"/api/customer/{created_customer.id}", json=customer_two)

    assert response.status == "401 UNAUTHORIZED"
    assert response.json["message"] == "Missing Authorization Header"

    truncate_db()


def test_customer_modify_by_id_not_found(client):
    truncate_db()

    # Authenticated user
    create_user(client)
    authenticated_user = authenticate_user(client)
    create_customer(client, authenticated_user['token'])

    # Created customer
    created_customer = Customer.find_customer_by_email(customer_one["email"])

    response = client.put(
        f"/api/customer/{created_customer.id + 1}",
        headers={"Authorization": f"Bearer {authenticated_user['token']}"},
        json=customer_two,
    )

    assert response.status == "404 NOT FOUND"
    assert response.json["message"] == "A customer with the given ID does not exist"

    truncate_db()


def test_customer_delete_by_id_success(client):
    truncate_db()

    # Authenticated user
    create_user(client)
    authenticated_user = authenticate_user(client)
    create_customer(client, authenticated_user['token'])

    # Created customer
    created_customer = Customer.find_customer_by_email(customer_one["email"])

    response = client.delete(
        f"/api/customer/{created_customer.id}",
        headers={"Authorization": f"Bearer {authenticated_user['token']}"},
    )

    assert response.status == "200 OK"
    assert response.json["message"] == "Customer deleted successfully"

    truncate_db()


def test_customer_delete_by_id_authentication_error(client):
    truncate_db()

    # Authenticated user
    create_user(client)
    authenticated_user = authenticate_user(client)
    create_customer(client, authenticated_user['token'])

    # Created customer
    created_customer = Customer.find_customer_by_email(customer_one["email"])

    response = client.delete(f"/api/customer/{created_customer.id}")

    assert response.status == "401 UNAUTHORIZED"
    assert response.json["message"] == "Missing Authorization Header"

    truncate_db()


def test_customer_delete_by_id_not_found(client):
    truncate_db()

    # Authenticated user
    create_user(client)
    authenticated_user = authenticate_user(client)
    create_customer(client, authenticated_user['token'])

    # Created customer
    created_customer = Customer.find_customer_by_email(customer_one["email"])

    response = client.delete(
        f"/api/customer/{created_customer.id + 1}",
        headers={"Authorization": f"Bearer {authenticated_user['token']}"},
    )

    assert response.status == "404 NOT FOUND"
    assert response.json["message"] == "A customer with the given ID does not exist"

    truncate_db()
