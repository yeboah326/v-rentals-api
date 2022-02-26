from apiflask import Schema
from apiflask.fields import String


class GenericResponse(Schema):
    message = String()
    detail = String()
