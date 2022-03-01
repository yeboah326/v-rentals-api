from sqlalchemy import Enum
from api.extensions import db
import enum


class VehicleType(enum.Enum):
    saloon = 1
    bus = 2
    motor_cycle = 3
    bicycle = 4


class Vehicle(db.Model):
    __tablename__ = "vr_vehicle"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    cost_per_day = db.Column(db.Numeric(precision=6, scale=2), nullable=False)
    penalty_per_day = db.Column(db.Numeric(precision=6, scale=2), nullable=False)
    vehicle_type = db.Column(Enum(VehicleType), nullable=False)
    rented = db.Column(db.Boolean, default=False, nullable=False)
    rentals = db.relationship(
        "Rental",
        backref="vehicle",
        lazy=True,
        cascade="all, delete",
        passive_deletes=True,
    )

    @classmethod
    def get_vehicle_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def get_all_rentals(cls):
        return cls.query.all()
