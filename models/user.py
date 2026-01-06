#models/user.py
from datetime import datetime
from db import db



class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    phone = db.Column(db.String(8))
    role = db.Column(db.String(20), nullable=False, default="customer")
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    bakeries = db.relationship("BakeryModel", back_populates="owner", lazy="dynamic")
    orders = db.relationship("OrderModel", back_populates="user", lazy="dynamic")
    reviews = db.relationship("ReviewModel", back_populates="user", lazy="dynamic")

    @classmethod
    def find_by_id(cls, user_id):
        return cls.query.get(user_id)
