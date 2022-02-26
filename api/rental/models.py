from api.extensions import db


class Rental(db.Model):
    __tablename__ = "vr_rental"

    id = db.Column(db.Integer, primary_key=True)
    vehicle_id = db.Column(db.Integer, db.ForeignKey("vr_vehicle.id"))
    customer_id = db.Column(db.Integer, db.ForeignKey("vr_customer.id"))
    start_date = db.Column(db.Date, nullable=False)
    proposed_return_date = db.Column(db.Date, nullable=False)
    actual_return_date = db.Column(db.Date, nullable=True)
    actual_charge = db.Column(db.Numeric(precision=7, scale=2))
    penalty_charge = db.Column(db.Numeric(precision=6, scale=2))

    @classmethod
    def get_rental_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def get_all_rentals(cls, id):
        return cls.query.all()
