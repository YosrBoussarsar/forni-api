from flask.views import MethodView
from flask_smorest import Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import func
from db import db

from models.user import UserModel
from models.order import OrderModel
from models.surplus_bag import SurplusBagModel
from models.bakery import BakeryModel

from schemas import SurplusBagSchema

blp = Blueprint(
    "Recommendations",
    __name__,
    description="Personalized recommendations for users"
)


@blp.route("/recommendation")
class Recommendations(MethodView):

    @jwt_required()
    @blp.response(200, SurplusBagSchema(many=True))
    def get(self):
        """
        Recommend surplus bags based on:
        - User’s past orders
        - Favorite bakery categories
        - Bags still available and active
        """

        user_id = get_jwt_identity()
        user = UserModel.find_by_id(user_id)

        if not user:
            return []

        # 1. Get bakeries the user ordered from before
        past_bakery_ids = (
            db.session.query(OrderModel.bakery_id)
            .filter(OrderModel.user_id == user.id)
            .distinct()
            .all()
        )
        past_bakery_ids = [row[0] for row in past_bakery_ids]

        # 2. If user has no history → fallback to popular bags
        if not past_bakery_ids:
            return (
                SurplusBagModel.query
                .filter(
                    SurplusBagModel.status == "active",
                    SurplusBagModel.quantity_available > 0
                )
                .order_by(SurplusBagModel.pickup_start.asc())
                .limit(10)
                .all()
            )

        # 3. Recommend bags from bakeries the user likes
        recommended_bags = (
            SurplusBagModel.query
            .filter(
                SurplusBagModel.bakery_id.in_(past_bakery_ids),
                SurplusBagModel.status == "active",
                SurplusBagModel.quantity_available > 0
            )
            .order_by(SurplusBagModel.pickup_start.asc())
            .all()
        )

        # 4. If no bags available from favorite bakeries → fallback
        if not recommended_bags:
            return (
                SurplusBagModel.query
                .filter(
                    SurplusBagModel.status == "active",
                    SurplusBagModel.quantity_available > 0
                )
                .order_by(SurplusBagModel.pickup_start.asc())
                .limit(10)
                .all()
            )

        return recommended_bags
