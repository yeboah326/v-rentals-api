from apiflask import Schema
from apiflask.fields import Integer, Float, Date, List, Nested


class RentalSchema(Schema):
    id = Integer(dump_only=True, required=True)
    vehicle_id = Integer(required=True)
    customer_id = Integer(required=True)
    start_date = Date(required=True)
    proposed_return_date = Date(required=True)
    actual_return_date = Date(required=False)
    actual_charge = Float(required=False)
    penalty_charge = Float(required=False)


class RentalsSchema(Schema):
    rentals = List(Nested(RentalSchema))
