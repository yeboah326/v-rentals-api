from apiflask import Schema
from apiflask.fields import String, List, Nested, Integer, Number
from apiflask.validators import Email, Length


class CustomerSchema(Schema):
    id = Number(dump_only=True)
    name = String(
        required=True,
        validate=Length(min=1, max=60),
        metadata={"description": "Name should have a valid format"},
    )
    email = String(
        required=True,
        validate=[Email, Length(max=30)],
        metadata={"description": "Email should have a valid format"},
    )
    telephone = String(
        required=True,
        validate=Length(equal=10),
        metadata={
            "description": "Name should have a valid format and should contain only ten characters"
        },
    )
    company = String(
        required=True,
        validate=Length(min=4, max=40),
        metadata={"description": "Company should have a valid format"},
    )


class CustomersSchema(Schema):
    customers = List(Nested(CustomerSchema))
