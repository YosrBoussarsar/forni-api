from datetime import datetime
from db import db

class OrderModel(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    bakery_id = db.Column(db.Integer, db.ForeignKey("bakeries.id"), nullable=False)
    
    # Deprecated: kept for backward compatibility, use order_items instead
    surplus_bag_id = db.Column(db.Integer, db.ForeignKey("surplus_bags.id"))

    total_price = db.Column(db.Numeric(10, 2), nullable=False)
    status = db.Column(db.String(20), default="pending")

    pickup_code = db.Column(db.String(10))
    pickup_confirmed_at = db.Column(db.DateTime)
    pickup_time = db.Column(db.DateTime)
    payment_intent_id = db.Column(db.String(255))

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship("UserModel", back_populates="orders")
    bakery = db.relationship("BakeryModel", back_populates="orders")
    surplus_bag = db.relationship("SurplusBagModel", back_populates="orders")
    order_items = db.relationship("OrderItemModel", back_populates="order", cascade="all, delete-orphan")
