from api.extensions import db


class Customer(db.Model):
    __tablename__ = "vr_customer"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(30), nullable=False, unique=True)
    telephone = db.Column(db.String(10), nullable=False)
    company = db.Column(db.String(40), nullable=False)
    rentals = db.relationship(
        "Rental",
        backref="customer",
        lazy=True,
        cascade="all, delete",
        passive_deletes=True,
    )

    @classmethod
    def find_customer_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_customer_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def get_all_customer_rentals(cls, id):
        return cls.query.filter_by(id=id).first().rentals

    @classmethod
    def get_all_customers(cls):
        return cls.query.all()
