from apiflask import APIBlueprint
from api.extensions import limiter

auth = APIBlueprint("auth", __name__, url_prefix="/api/auth")

@auth.get("/home")
@limiter.limit("1/minute")
def go_home():
    return "Go home"