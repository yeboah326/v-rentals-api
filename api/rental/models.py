from api.extensions import db
from api.vehicle.models import Vehicle


class Rental(db.Model):
    __tablename__ = "vr_rental"

    id = db.Column(db.Integer, primary_key=True)
    vehicle_id = db.Column(
        db.Integer, db.ForeignKey("vr_vehicle.id", ondelete="cascade"), nullable=False
    )
    customer_id = db.Column(
        db.Integer, db.ForeignKey("vr_customer.id", ondelete="cascade"), nullable=False
    )
    start_date = db.Column(db.Date, nullable=False)
    proposed_return_date = db.Column(db.Date, nullable=False)
    actual_return_date = db.Column(db.Date, nullable=True)
    actual_charge = db.Column(db.Numeric(precision=7, scale=2))
    penalty_charge = db.Column(db.Numeric(precision=6, scale=2))

    @classmethod
    def get_rental_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def get_all_rentals(cls):
        return cls.query.all()

    def set_actual_and_penalty_charges(self):
        if self.actual_return_date == None:
            self.actual_charge = 0
            self.penalty_charge = 0
        else:
            vehicle = Vehicle.get_vehicle_by_id(self.vehicle_id)

            total_days = (self.actual_return_date - self.start_date).days
            proposed_days = (self.proposed_return_date - self.start_date).days
            penalty_days = (
                0 if proposed_days >= total_days else total_days - proposed_days
            )
            non_penalty_days = total_days - penalty_days

            self.actual_charge = vehicle.cost_per_day * non_penalty_days
            self.penalty_charge = vehicle.penalty_per_day * penalty_days
