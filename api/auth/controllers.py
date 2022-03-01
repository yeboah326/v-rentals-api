from apiflask import APIBlueprint, doc, input, output, HTTPError
from flask_jwt_extended import create_access_token
from api.extensions import db, limiter
from .models import User
from .schemas import (
    UserSchemaDump,
    UserSchemaLoad,
    UserSchemaLoginDump,
    UserSchemaLoginLoad,
)

auth = APIBlueprint("auth", __name__, url_prefix="/api/auth")

# @auth.get("/home")
# @limiter.limit("1/minute")
# def go_home():
#     return "Go home"


@auth.post("/authenticate")
@input(UserSchemaLoginLoad)
@output(UserSchemaLoginDump)
@doc(
    summary="Authenticate user",
    description="An endpoint to generate a token for the user",
    responses=[200, 400, 404],
)
def user_authenticate(data):
    user = User.find_user_by_email(data["email"])

    if user:
        # Check user password
        password_correct = user.check_password(data["password"])
        if password_correct:
            user.token = create_access_token(user.public_id)
            return user
        raise HTTPError(400, message="Either the username or password is wrong")
    raise HTTPError(404, message="A user with the given email does not exist")


@auth.post("/")
@input(UserSchemaLoad)
@output(UserSchemaDump)
@doc(summary="Create user", description="An endpoint to create a new user")
def user_create(data):
    user = User(**data)

    # Save to the database
    db.session.add(user)
    db.session.commit()

    return user, 200
