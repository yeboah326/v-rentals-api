from secrets import token_hex
from api.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    __tablename__ = "vr_user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True, nullable=False)
    email = db.Column(db.String(25), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)

    @property
    def password():
        return "Password can only be set"

    @property().setter
    def password(self, password) -> None:
        self.password_hash = generate_password_hash(password=password, salt_length=32)
        self.public_id = token_hex(32)

    def check_password(self, password) -> bool:
        return check_password_hash(self.password_hash, password)

    @classmethod
    def find_user_by_id(cls, public_id):
        return cls.query.filter_by(public_id=public_id).first()

    @classmethod
    def find_user_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_user_by_email(cls, email):
        return cls.query.filter_by(email=email).first()
