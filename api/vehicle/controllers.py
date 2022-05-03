from apiflask import APIBlueprint, input, output, doc, HTTPError
from api.extensions import db
from api.generic import GenericResponse
from flask_jwt_extended import jwt_required
from .models import Vehicle, VehicleType
from .schemas import VehicleSchema, VehiclesSchema, VehicleTypesSchema

vehicle = APIBlueprint("vehicle", __name__, url_prefix="/api/vehicle")


@vehicle.post("/")
@input(VehicleSchema)
@output(VehicleSchema, status_code=201)
@doc(
    summary="Create a vehicle",
    description="An endpoint for the creation of vehicles",
    responses=[201, 400, 401],
)
@jwt_required()
def vehicle_create(data):
    vehicle = Vehicle(**data)

    # Save to the database
    db.session.add(vehicle)
    db.session.commit()

    return vehicle, 200


@vehicle.get("/<int:id>")
@output(VehicleSchema)
@doc(
    summary="Get a vehicle by id",
    description="An endpoint to get a vehicle by id",
    responses=[200, 401, 404],
)
@jwt_required()
def vehicle_get_by_id(id):
    vehicle = Vehicle.get_vehicle_by_id(id)

    if vehicle:
        return vehicle, 200
    raise HTTPError(404, "A vehicle with the given ID does not exist")


@vehicle.get("/")
@output(VehiclesSchema)
@doc(
    summary="Get all vehicles",
    description="An endpoint to get all vehicles",
    responses=[200, 401],
)
@jwt_required()
def vehicle_get_all():
    vehicles = Vehicle.get_all_rentals()

    return {"vehicles": vehicles}, 200

# TODO: Add test for this endpoint
@vehicle.get("/types")
@output(VehicleTypesSchema)
@doc(
    summary="Get all vehicle types",
    description="An endpoint to get all vehicle types",
    responses=[200, 401]
)
@jwt_required()
def vehicle_get_all_types():
    return VehicleType.to_list()


@vehicle.put("/<int:id>")
@input(VehicleSchema)
@output(VehicleSchema)
@doc(
    summary="Modify a vehicle by id",
    description="An endpoint to modify a vehicle by id",
    responses=[200, 400, 401, 404],
)
@jwt_required()
def vehicle_modify_by_id(id, data):
    vehicle = Vehicle.get_vehicle_by_id(id)

    if vehicle:
        for key, value in data.items():
            setattr(vehicle, key, value)

        db.session.commit()

        return vehicle, 200
    raise HTTPError(404, "A vehicle with the given ID does not exist")


@vehicle.delete("/<int:id>")
@output(GenericResponse)
@doc(
    summary="Delete vehicle by id",
    description="An endpoint to delete a vehicle by id",
    responses=[200, 400, 401, 404],
)
@jwt_required()
def vehicle_delete_by_id(id):
    vehicle = Vehicle.get_vehicle_by_id(id)

    if vehicle:
        db.session.delete(vehicle)
        db.session.commit()

        return {"message": "Vehicle deleted successfully"}, 200
    raise HTTPError(404, "A vehicle with the given ID does not exist")
