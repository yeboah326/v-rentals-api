from apiflask import APIBlueprint, input, output, doc, HTTPError
from flask_jwt_extended import jwt_required
from api.extensions import db
from .models import Rental
from .schemas import RentalSchema, RentalsSchema

rental = APIBlueprint("rental", __name__, url_prefix="/api/rental")


@rental.post("/")
@input(RentalSchema)
@output(RentalSchema, status_code=201)
@doc(
    summary="Create rental",
    description="An endpoint to create a new rental",
    responses=[201, 400, 401],
)
@jwt_required()
def rental_create(data):
    rental = Rental(**data)

    rental.set_actual_and_penalty_charges()

    # Save to the database
    db.session.add(rental)
    db.session.commit()

    return rental


@rental.get("/<int:id>")
@output(RentalSchema)
@doc(
    summary="Get rental by id",
    description="An endpoint to get a rental by id",
    responses=[200, 401, 404],
)
@jwt_required()
def rental_get_by_id(id):
    rental = Rental.get_rental_by_id(id)

    if rental:
        return rental, 200
    raise HTTPError(404, "A rental with the given ID does not exist")


@rental.get("/")
@output(RentalsSchema)
@doc(
    summary="Get all rentals",
    description="An endpoint to get all rentals",
    responses=[200, 401],
)
@jwt_required()
def rental_get_all():
    rentals = Rental.get_all_rentals()

    return {"rentals": rentals}, 200


@rental.put("/<int:id>")
@input(RentalSchema)
@output(RentalSchema)
@doc(
    summary="Modify rental by id",
    description="An endpoint to modify a rental by id",
    responses=[200, 400, 401, 404],
)
@jwt_required()
def rental_modify_by_id(id, data):
    rental = Rental.get_rental_by_id(id)

    if rental:
        for key, value in data.items():
            setattr(rental, key, value)
        db.session.commit()
        return rental, 200
    raise HTTPError(404, "A rental with the given ID does not exist")


@rental.delete("/<int:id>")
@doc(
    summary="Delete a rental by id",
    description="An endpoint to delete a rental by id",
    responses=[200, 400, 401, 404],
)
@jwt_required
def rental_delete_by_id(id):
    rental = Rental.get_rental_by_id(id)

    if rental:
        db.session.delete(rental)
        db.session.commit()
        return {"message": "Rental deleted successfully"}
    raise HTTPError(404, "A rental with the given ID does not exist")
