from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from db import db
from models.review import ReviewModel
from models.order import OrderModel
from models.bakery import BakeryModel
from schemas import ReviewSchema, ReviewCreateSchema, ReviewUpdateSchema
from decorators import admin_required

blp = Blueprint("Reviews", __name__, description="Operations on reviews")

@blp.route("/review/<int:review_id>")
class Review(MethodView):
    @blp.response(200, ReviewSchema)
    def get(self, review_id):
        return ReviewModel.query.get_or_404(review_id)

    @jwt_required()
    @blp.arguments(ReviewUpdateSchema)
    @blp.response(200, ReviewSchema)
    def put(self, data, review_id):
        review = ReviewModel.query.get_or_404(review_id)
        if review.user_id != int(get_jwt_identity()):
            abort(403, message="Forbidden")

        for field, value in data.items():
            setattr(review, field, value)

        # Update bakery rating
        if review.bakery_id:
            update_bakery_rating(review.bakery_id)

        db.session.commit()
        return review

    @jwt_required()
    def delete(self, review_id):
        review = ReviewModel.query.get_or_404(review_id)
        user_id = int(get_jwt_identity())

        if review.user_id != user_id:
            abort(403, message="Forbidden")

        bakery_id = review.bakery_id
        db.session.delete(review)
        db.session.commit()

        # Update bakery rating after deletion
        if bakery_id:
            update_bakery_rating(bakery_id)

        return {"message": "Review deleted"}


@blp.route("/review")
class ReviewList(MethodView):
    @blp.response(200, ReviewSchema(many=True))
    def get(self):
        return ReviewModel.query.all()

    @jwt_required()
    @blp.arguments(ReviewCreateSchema)
    @blp.response(201, ReviewSchema)
    def post(self, data):
        order = OrderModel.query.get_or_404(data["order_id"])

        if order.user_id != int(get_jwt_identity()):
            abort(403, message="Forbidden")

        if order.status != "completed":
            abort(400, message="Order not completed")

        # Check if review already exists for this order
        existing_review = ReviewModel.query.filter_by(
            user_id=order.user_id,
            bakery_id=order.bakery_id,
            surplus_bag_id=order.surplus_bag_id
        ).first()

        if existing_review:
            abort(400, message="Review already exists for this order")

        review = ReviewModel(
            user_id=order.user_id,
            bakery_id=order.bakery_id,
            surplus_bag_id=order.surplus_bag_id,
            rating=data["rating"],
            comment=data.get("comment"),
        )

        db.session.add(review)
        db.session.commit()

        # Update bakery rating
        if review.bakery_id:
            update_bakery_rating(review.bakery_id)

        return review


@blp.route("/bakery/<int:bakery_id>/reviews")
class BakeryReviews(MethodView):
    @blp.response(200, ReviewSchema(many=True))
    def get(self, bakery_id):
        """Get all reviews for a specific bakery"""
        bakery = BakeryModel.query.get_or_404(bakery_id)
        return ReviewModel.query.filter_by(bakery_id=bakery_id).order_by(ReviewModel.created_at.desc()).all()


def update_bakery_rating(bakery_id):
    """Helper function to update bakery's average rating"""
    bakery = BakeryModel.query.get(bakery_id)
    if bakery:
        reviews = ReviewModel.query.filter_by(bakery_id=bakery_id).all()
        if reviews:
            bakery.rating = sum(r.rating for r in reviews) / len(reviews)
            bakery.review_count = len(reviews)
        else:
            bakery.rating = 0.0
            bakery.review_count = 0
        db.session.commit()