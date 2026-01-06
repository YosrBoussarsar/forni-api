from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required
from flask import request
from db import db
from models.product import ProductModel
from models.bakery import BakeryModel
from schemas import ProductSchema, ProductCreateSchema, ProductUpdateSchema
from decorators import owner_or_admin_required

blp = Blueprint("Products", __name__, description="Operations on products")

@blp.route("/product/<int:product_id>")
class Product(MethodView):
    @blp.response(200, ProductSchema)
    def get(self, product_id):
        return ProductModel.query.get_or_404(product_id)

    @jwt_required()
    @owner_or_admin_required(ProductModel)
    @blp.arguments(ProductUpdateSchema)
    @blp.response(200, ProductSchema)
    def put(self, data, product_id):
        product = ProductModel.query.get_or_404(product_id)
        for field, value in data.items():
            setattr(product, field, value)
        db.session.commit()
        return product

    @jwt_required()
    @owner_or_admin_required(ProductModel)
    def delete(self, product_id):
        product = ProductModel.query.get_or_404(product_id)
        db.session.delete(product)
        db.session.commit()
        return {"message": "Product deleted"}


@blp.route("/product")
class ProductList(MethodView):
    @blp.response(200, ProductSchema(many=True))
    def get(self):
        """
        Get all products with optional tag filtering
        Query params: tags (comma-separated, e.g., ?tags=croissant,pastry)
        """
        tags_param = request.args.get('tags')
        
        if tags_param:
            # Split tags and filter products
            search_tags = [tag.strip().lower() for tag in tags_param.split(',')]
            products = ProductModel.query.all()
            
            # Filter products that contain any of the search tags
            filtered_products = []
            for product in products:
                if product.tags:
                    product_tags = [tag.strip().lower() for tag in product.tags.split(',')]
                    if any(tag in product_tags for tag in search_tags):
                        filtered_products.append(product)
            
            return filtered_products
        
        return ProductModel.query.all()

    @jwt_required()
    @blp.arguments(ProductCreateSchema)
    @blp.response(201, ProductSchema)
    def post(self, data):
        bakery = BakeryModel.query.get(data["bakery_id"])
        if not bakery:
            abort(404, message="Bakery not found")

        product = ProductModel(**data)
        db.session.add(product)
        db.session.commit()
        return product
