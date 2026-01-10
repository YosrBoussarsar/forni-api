#resources\surplus_bags.py
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required
from flask import request
from db import db
from models.surplus_bag import SurplusBagModel
from models.bakery import BakeryModel
from schemas import SurplusBagSchema, SurplusBagCreateSchema, SurplusBagUpdateSchema
from decorators import owner_or_admin_required

blp = Blueprint("SurplusBags", __name__, description="Operations on surplus bags")

@blp.route("/surplus_bag/<int:surplus_bag_id>")
class SurplusBag(MethodView):
    @blp.response(200, SurplusBagSchema)
    def get(self, surplus_bag_id):
        return SurplusBagModel.query.get_or_404(surplus_bag_id)

    @jwt_required()
    @owner_or_admin_required(SurplusBagModel)
    @blp.arguments(SurplusBagUpdateSchema)
    @blp.response(200, SurplusBagSchema)
    def put(self, data, surplus_bag_id):
        bag = SurplusBagModel.query.get_or_404(surplus_bag_id)
        for field, value in data.items():
            setattr(bag, field, value)
        db.session.commit()
        return bag

    @jwt_required()
    @owner_or_admin_required(SurplusBagModel)
    def delete(self, surplus_bag_id):
        bag = SurplusBagModel.query.get_or_404(surplus_bag_id)
        db.session.delete(bag)
        db.session.commit()
        return {"message": "Surplus bag deleted"}


@blp.route("/surplus_bag")
class SurplusBagList(MethodView):
    @blp.response(200, SurplusBagSchema(many=True))
    def get(self):
        """
        Get all surplus bags with optional filtering
        Query params: 
        - bakery_id: filter by bakery
        - tags: comma-separated tags (e.g., ?tags=sweet,savory)
        """
        bakery_id = request.args.get('bakery_id', type=int)
        tags_param = request.args.get('tags')
        
        # Start with base query
        query = SurplusBagModel.query
        
        # Filter by bakery if specified
        if bakery_id:
            query = query.filter_by(bakery_id=bakery_id)
        
        # Filter by tags if specified
        if tags_param:
            search_tags = [tag.strip().lower() for tag in tags_param.split(',')]
            bags = query.all()
            
            # Filter bags that contain any of the search tags
            filtered_bags = []
            for bag in bags:
                if bag.tags:
                    bag_tags = [tag.strip().lower() for tag in bag.tags.split(',')]
                    if any(tag in bag_tags for tag in search_tags):
                        filtered_bags.append(bag)
            
            return filtered_bags
        
        return query.all()

    @jwt_required()
    @blp.arguments(SurplusBagCreateSchema)
    @blp.response(201, SurplusBagSchema)
    def post(self, data):
        bakery = BakeryModel.query.get(data["bakery_id"])
        if not bakery:
            abort(404, message="Bakery not found")

        bag = SurplusBagModel(**data)
        db.session.add(bag)
        db.session.commit()
        return bag
