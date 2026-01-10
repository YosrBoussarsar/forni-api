from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request
from db import db
from models.product import ProductModel
from models.bakery import BakeryModel
from models.user import UserModel
from schemas import ProductSchema, ProductCreateSchema, ProductUpdateSchema
from decorators import owner_or_admin_required
from sqlalchemy import func

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
        Get all products with optional filtering
        Query params: 
        - bakery_id: filter by bakery
        - tags: comma-separated tags (e.g., ?tags=croissant,pastry)
        """
        bakery_id = request.args.get('bakery_id', type=int)
        tags_param = request.args.get('tags')
        
        # Start with base query
        query = ProductModel.query
        
        # Filter by bakery if specified
        if bakery_id:
            query = query.filter_by(bakery_id=bakery_id)
        
        # Filter by tags if specified
        if tags_param:
            search_tags = [tag.strip().lower() for tag in tags_param.split(',')]
            products = query.all()
            
            # Filter products that contain any of the search tags
            filtered_products = []
            for product in products:
                if product.tags:
                    product_tags = [tag.strip().lower() for tag in product.tags.split(',')]
                    if any(tag in product_tags for tag in search_tags):
                        filtered_products.append(product)
            
            return filtered_products
        
        return query.all()

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


@blp.route("/product/recommendations")
class ProductRecommendations(MethodView):
    @jwt_required()
    def get(self):
        """
        Get product recommendations for bakery owners
        Shows popular products from other bakeries that can be used as templates
        Query params: 
        - exclude_bakery_id: exclude products from specific bakery (usually the owner's bakery)
        - category: filter by category
        """
        user_id = int(get_jwt_identity())
        user = UserModel.find_by_id(user_id)
        
        # Get bakery_id to exclude (owner's bakery)
        exclude_bakery_id = request.args.get('exclude_bakery_id', type=int)
        category = request.args.get('category')
        
        # Build query
        query = ProductModel.query
        
        if exclude_bakery_id:
            query = query.filter(ProductModel.bakery_id != exclude_bakery_id)
        
        if category:
            query = query.filter(ProductModel.category == category)
        
        products = query.all()
        
        # Group products by name to find common products
        product_groups = {}
        for product in products:
            name_lower = product.name.lower().strip()
            if name_lower not in product_groups:
                product_groups[name_lower] = {
                    'name': product.name,
                    'count': 0,
                    'example': product,
                    'categories': set(),
                    'avg_price': []
                }
            
            product_groups[name_lower]['count'] += 1
            if product.category:
                product_groups[name_lower]['categories'].add(product.category)
            if product.price:
                product_groups[name_lower]['avg_price'].append(float(product.price))
        
        # Convert to recommendation list (sorted by popularity)
        recommendations = []
        for group in product_groups.values():
            if group['count'] >= 1:  # Show products that appear at least once
                avg_price = sum(group['avg_price']) / len(group['avg_price']) if group['avg_price'] else None
                
                recommendations.append({
                    'template_product_id': group['example'].id,
                    'name': group['name'],
                    'description': group['example'].description,
                    'category': group['example'].category,
                    'allergens': group['example'].allergens,
                    'tags': group['example'].tags,
                    'image_url': group['example'].image_url,
                    'popularity': group['count'],
                    'avg_price': round(avg_price, 2) if avg_price else None,
                    'categories': list(group['categories'])
                })
        
        # Sort by popularity
        recommendations.sort(key=lambda x: x['popularity'], reverse=True)
        
        return {'recommendations': recommendations[:50]}  # Limit to top 50


@blp.route("/product/from-template/<int:template_product_id>")
class ProductFromTemplate(MethodView):
    @jwt_required()
    @blp.response(201, ProductSchema)
    def post(self, template_product_id):
        """
        Create a new product based on an existing product template
        Body: { "bakery_id": int, "price": float, "quantity_available": int, "is_available": bool }
        """
        user_id = int(get_jwt_identity())
        user = UserModel.find_by_id(user_id)
        
        # Get the template product
        template = ProductModel.query.get_or_404(template_product_id)
        
        # Get data from request
        data = request.get_json()
        
        if not data or 'bakery_id' not in data:
            abort(400, message="bakery_id is required")
        
        bakery_id = data['bakery_id']
        bakery = BakeryModel.query.get_or_404(bakery_id)
        
        # Verify ownership
        if user.role == "bakery_owner" and bakery.owner_id != user.id:
            abort(403, message="You can only create products for your own bakery")
        
        # Check if product with same name already exists for this bakery
        existing = ProductModel.query.filter_by(
            bakery_id=bakery_id,
            name=template.name
        ).first()
        
        if existing:
            abort(409, message=f"Product '{template.name}' already exists in your bakery")
        
        # Create new product copying template fields
        new_product = ProductModel(
            bakery_id=bakery_id,
            name=template.name,
            description=template.description,
            category=template.category,
            allergens=template.allergens,
            tags=template.tags,
            image_url=template.image_url,
            # Bakery-specific fields from request
            price=data.get('price', template.price),
            quantity_available=data.get('quantity_available'),
            is_available=data.get('is_available', True)
        )
        
        db.session.add(new_product)
        db.session.commit()
        
        return new_product
