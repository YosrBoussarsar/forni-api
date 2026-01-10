from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request
from db import db
from models.bakery import BakeryModel
from models.user import UserModel
from models.product import ProductModel
from schemas import BakerySchema, BakeryDetailSchema, BakeryCreateSchema, BakeryUpdateSchema
from decorators import owner_or_admin_required
import math

blp = Blueprint("Bakeries",__name__,description="Operations on bakeries")

@blp.route("/bakery/<int:bakery_id>")
class Bakery(MethodView):

    # PUBLIC: Get bakery by ID with products and surplus bags
    @blp.response(200, BakeryDetailSchema)
    def get(self, bakery_id):
        return BakeryModel.query.get_or_404(bakery_id)

    # OWNER or ADMIN: Update bakery
    @jwt_required()
    @owner_or_admin_required(BakeryModel)
    @blp.arguments(BakeryUpdateSchema)
    @blp.response(200, BakerySchema)
    def put(self, data, bakery_id):
        bakery = BakeryModel.query.get_or_404(bakery_id)

        for field, value in data.items():
            setattr(bakery, field, value)

        db.session.commit()
        return bakery

    # OWNER or ADMIN: Delete bakery
    @jwt_required()
    @owner_or_admin_required(BakeryModel)
    def delete(self, bakery_id):
        bakery = BakeryModel.query.get_or_404(bakery_id)
        db.session.delete(bakery)
        db.session.commit()
        return {"message": "Bakery deleted"}


@blp.route("/bakery/my")
class MyBakery(MethodView):
    
    # Get current user's bakery with products and surplus bags
    @jwt_required()
    @blp.response(200, BakeryDetailSchema)
    def get(self):
        user_id = int(get_jwt_identity())
        bakery = BakeryModel.query.filter_by(owner_id=user_id).first()
        
        if not bakery:
            abort(404, message="You don't have a bakery yet")
        
        return bakery


@blp.route("/bakery")
class BakeryList(MethodView):

    # PUBLIC: Get all bakeries
    @blp.response(200, BakerySchema(many=True))
    def get(self):
        """
        Get all bakeries with optional product tag filtering
        Query params: product_tags (comma-separated, e.g., ?product_tags=croissant,bread)
        """
        tags_param = request.args.get('product_tags')
        
        if tags_param:
            # Split tags and find bakeries with matching products
            search_tags = [tag.strip().lower() for tag in tags_param.split(',')]
            
            # Find all products with matching tags
            products = ProductModel.query.all()
            bakery_ids = set()
            
            for product in products:
                if product.tags:
                    product_tags = [tag.strip().lower() for tag in product.tags.split(',')]
                    if any(tag in product_tags for tag in search_tags):
                        bakery_ids.add(product.bakery_id)
            
            # Get bakeries with matching products
            if bakery_ids:
                return BakeryModel.query.filter(BakeryModel.id.in_(bakery_ids)).all()
            else:
                return []
        
        return BakeryModel.query.all()

    # OWNER or ADMIN: Create bakery
    @jwt_required()
    @blp.arguments(BakeryCreateSchema)
    @blp.response(201, BakerySchema)
    def post(self, data):
        user_id = int(get_jwt_identity())
        user = UserModel.find_by_id(user_id)

        if user.role not in ["bakery_owner", "admin"]:
            abort(403, message="Only bakery owners or admins can create bakeries")

        bakery = BakeryModel(owner_id=user.id, **data)
        db.session.add(bakery)
        db.session.commit()
        return bakery


@blp.route("/bakery/nearby")
class NearbyBakeries(MethodView):
    @blp.response(200, BakerySchema(many=True))
    def get(self):
        """
        Find bakeries near a given location
        Query params: lat, lng, radius (in km, default 10)
        """
        try:
            lat = float(request.args.get('lat'))
            lng = float(request.args.get('lng'))
        except (TypeError, ValueError):
            abort(400, message="Invalid lat/lng parameters")

        radius = float(request.args.get('radius', 10))  # default 10km

        # Get all bakeries with coordinates
        bakeries = BakeryModel.query.filter(
            BakeryModel.latitude.isnot(None),
            BakeryModel.longitude.isnot(None)
        ).all()

        # Filter by distance
        nearby = []
        for bakery in bakeries:
            distance = calculate_distance(lat, lng, bakery.latitude, bakery.longitude)
            if distance <= radius:
                nearby.append(bakery)

        return nearby


def calculate_distance(lat1, lon1, lat2, lon2):
    """Calculate distance between two points using Haversine formula (in km)"""
    R = 6371  # Earth's radius in kilometers

    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    delta_lat = math.radians(lat2 - lat1)
    delta_lon = math.radians(lon2 - lon1)

    a = math.sin(delta_lat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon/2)**2
    c = 2 * math.asin(math.sqrt(a))

    return R * c