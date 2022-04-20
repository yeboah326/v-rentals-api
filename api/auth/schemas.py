from apiflask import Schema
from apiflask.fields import Integer, Float, Date, String
from apiflask.validators import Regexp, Length, Email


class UserSchemaLoad(Schema):
    username = String(
        required=True,
        validate=Length(min=5, max=15),
        metadata={"description": "Username should have 5 to 15 characters"},
    )
    email = String(
        required=True,
        validate=Email(),
        metadata={"description": "Email should have a valid format"},
    )
    password = String(
        required=True,
        validate=Regexp(
            r"^(?=.*[0-9].*[0-9])(?=.*[a-z].*[a-z].*[a-z])(?=.*[A-Z]).{8,}$"
        ),
        metadata={
            "description": "Password should contain a minimum of eight characters, at least two numbers, two lowercase characters and one uppercase character"
        },
        error_messages={"null": "Field may not be null"}
    )
# TODO: Fix metadata error message

class UserSchemaDump(Schema):
    public_id = String(required=True, validate=Length(equal=64))
    username = String(
        required=True,
        validate=Length(min=5, max=15),
    )
    email = String(required=True, validate=Email())


class UserSchemaLoginLoad(Schema):
    email = String(
        required=True,
        validate=Email(),
        metadata={"description": "Email should have a valid format"},
        error_messages={"required": "Email is required to login"}
    )
    password = String(
        required=True,
        metadata={
            "description": "Password should contain a minimum of eight characters, at least one letter and one number"
        },
        error_messages={"required": "Password is required to login"}
    )


class UserSchemaLoginDump(Schema):
    public_id = String(required=True, validate=Length(equal=64))
    username = String(
        required=True,
        validate=Length(min=5, max=15),
    )
    email = String(required=True, validate=Email())
    token = String(required=True)
