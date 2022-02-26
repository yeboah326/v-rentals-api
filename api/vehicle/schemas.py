from apiflask import Schema
from apiflask.fields import Integer, String, Float, Boolean, List, Nested
from apiflask.validators import Length, OneOf, Range


class VehicleSchema(Schema):
    id = Integer(
        required=True,
        dump_only=True,
        metadata={"description": "A unique id generated for every vehicle"},
    )
    name = String(
        required=True,
        validate=Length(min=1, max=50),
        metadata={
            "description": "A name of the vehicle that can be used to identify it. Does not have to be unique"
        },
    )
    cost_per_day = Float(
        required=True,
        validate=Range(min=0.00, max=9999.99),
        metadata={
            "description": "The cost of renting the vehicle per day before the proposed return date"
        },
    )
    penalty_per_day = Float(
        required=True,
        validate=Range(min=0.00, max=9999.99),
        metadata={
            "description": "The cost of renting the vehicle per day after the proposed return date"
        },
    )
    vehicle_type = String(
        required=True,
        validate=OneOf(["saloon", "bus", "motorcycle", "bicycle"]),
        metadata={"description": "The type of the vehicle"},
    )
    rented = Boolean(
        required=True,
        metadata={
            "description": "A value to show whether the vehicle has been rented or not"
        },
    )


class VehiclesSchema(Schema):
    vehicles = List(Nested(VehicleSchema))
