# UPDATED models/bakery.py
from datetime import datetime
from db import db

class BakeryModel(db.Model):
    __tablename__ = "bakeries"

    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    address = db.Column(db.String(255))
    phone = db.Column(db.String(50))
    opening_hours = db.Column(db.String(100))
    city = db.Column(db.String(100))
    governorate = db.Column(db.String(100))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    specialties = db.Column(db.String(255))
    image_url = db.Column(db.String(500))  # NEW FIELD

    rating = db.Column(db.Float, default=0.0)
    review_count = db.Column(db.Integer, default=0)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    owner = db.relationship("UserModel", back_populates="bakeries")
    products = db.relationship("ProductModel", back_populates="bakery", lazy="dynamic")
    surplus_bags = db.relationship("SurplusBagModel", back_populates="bakery", lazy="dynamic")
    orders = db.relationship("OrderModel", back_populates="bakery", lazy="dynamic")
    reviews = db.relationship("ReviewModel", back_populates="bakery", lazy="dynamic")