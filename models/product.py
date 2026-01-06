from datetime import datetime
from db import db

class ProductModel(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    bakery_id = db.Column(db.Integer, db.ForeignKey("bakeries.id"), nullable=False)

    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(50))
    price = db.Column(db.Numeric(10, 2), nullable=False)
    allergens = db.Column(db.String(255))
    tags = db.Column(db.String(500))  # e.g., "croissant,pastry,breakfast"
    is_available = db.Column(db.Boolean, default=True)
    image_url = db.Column(db.String(500))  # NEW FIELD

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    bakery = db.relationship("BakeryModel", back_populates="products")