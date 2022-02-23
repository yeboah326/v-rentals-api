from apiflask import APIBlueprint

customer = APIBlueprint("customer", __name__, url_prefix="/api/customer")