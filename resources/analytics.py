from flask.views import MethodView
from flask_smorest import Blueprint, abort 
from flask_jwt_extended import jwt_required, get_jwt_identity
from db import db
from models.order import OrderModel
from models.surplus_bag import SurplusBagModel
from models.user import UserModel
from decorators import admin_required

blp = Blueprint("Analytics", __name__, description="Analytics operations")

@blp.route("/waste-prevented")
class WastePrevented(MethodView):
    @jwt_required()
    def get(self):
        user = UserModel.find_by_id(int(get_jwt_identity()))

        if user.role not in ["bakery_owner", "admin"]:
            abort(403, message="Forbidden")

        orders = OrderModel.query.all()
        total = 0

        for o in orders:
            if o.surplus_bag:
                total += float(o.surplus_bag.original_value - o.surplus_bag.sale_price)

        return {"total_waste_prevented": total}
