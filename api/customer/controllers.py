from apiflask import APIBlueprint, doc, HTTPError, input, output
from flask_jwt_extended import jwt_required
from api.extensions import db
from .models import Customer
from .schemas import CustomerSchema, CustomersSchema
from api.generic import GenericResponse

customer = APIBlueprint("customer", __name__, url_prefix="/api/customer")


@customer.post("/")
@input(CustomerSchema)
@output(CustomerSchema, status_code=201)
@doc(
    summary="Create customer",
    description="An endpoint to create a new customer",
    responses=[201, 400, 401],
)
@jwt_required()
def customer_create(data):
    customer = Customer(**data)

    # Save to the database
    db.session.add(customer)
    db.session.commit()

    return customer


@customer.get("/<int:id>")
@output(CustomerSchema)
@doc(
    summary="Get customer by id",
    description="An endpoint to a customer by id",
    responses=[200, 401, 404],
)
@jwt_required()
def customer_get_by_id(id):
    customer = Customer.find_customer_by_id(id)

    if customer:
        return customer, 200
    raise HTTPError(404, "A customer with the given ID does not exist")


@customer.get("/")
@output(CustomersSchema)
@doc(
    summary="Get all customers",
    description="An endpoint to get all customers",
    responses=[200, 401],
)
@jwt_required()
def customer_get_all():
    customers = Customer.get_all_customers()

    return {"customers": customers}


@customer.put("/<int:id>")
@input(CustomerSchema)
@output(CustomerSchema)
@doc(
    summary="Modify customer",
    description="An endpoint to modify customer by id",
    responses=[200, 400, 401, 404],
)
@jwt_required()
def customer_modify_by_id(id, data):
    customer = Customer.find_customer_by_id(id)

    if customer:
        for attribute, value in data.items():
            setattr(customer, attribute, value)

        # Save changes to the database
        db.session.commit()

        return customer, 200
    raise HTTPError(404, "A customer with the given ID does not exist")


@customer.delete("/<int:id>")
@output(GenericResponse)
@doc(
    summary="Delete customer",
    description="An endpoint to delete a user by id",
    responses=[200, 401, 404],
)
@jwt_required()
def customer_delete_by_id(id):
    customer = Customer.find_customer_by_id(id)

    if customer:
        db.session.delete(customer)
        db.session.commit()

        return {"message": "Customer deleted successfully"}
    raise HTTPError(404, "A customer with the given ID does not exist")
