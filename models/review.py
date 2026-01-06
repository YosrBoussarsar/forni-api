from datetime import datetime
from db import db

class ReviewModel(db.Model):
    __tablename__ = "reviews"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    bakery_id = db.Column(db.Integer, db.ForeignKey("bakeries.id"))
    surplus_bag_id = db.Column(db.Integer, db.ForeignKey("surplus_bags.id"))

    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship("UserModel", back_populates="reviews")
    bakery = db.relationship("BakeryModel", back_populates="reviews")
    surplus_bag = db.relationship("SurplusBagModel", back_populates="reviews")
