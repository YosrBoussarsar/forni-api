from datetime import datetime
from db import db

class SurplusBagModel(db.Model):
    __tablename__ = "surplus_bags"

    id = db.Column(db.Integer, primary_key=True)
    bakery_id = db.Column(db.Integer, db.ForeignKey("bakeries.id"), nullable=False)

    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(50))
    tags = db.Column(db.String(500))  # e.g., "sweet,savory,vegan"
    image_url = db.Column(db.String(500))  # NEW FIELD

    original_value = db.Column(db.Numeric(10, 2), nullable=False)
    sale_price = db.Column(db.Numeric(10, 2), nullable=False)

    quantity_available = db.Column(db.Integer, nullable=False)
    pickup_start = db.Column(db.DateTime, nullable=False)
    pickup_end = db.Column(db.DateTime, nullable=False)

    status = db.Column(db.String(20), default="active")

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    bakery = db.relationship("BakeryModel", back_populates="surplus_bags")
    orders = db.relationship("OrderModel", back_populates="surplus_bag", lazy="dynamic")
    reviews = db.relationship("ReviewModel", back_populates="surplus_bag", lazy="dynamic")