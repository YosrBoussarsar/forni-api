from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from db import db
from models.order import OrderModel
from models.order_item import OrderItemModel
from models.surplus_bag import SurplusBagModel
from models.product import ProductModel
from models.user import UserModel
from schemas import OrderSchema, OrderCreateSchema, OrderStatusSchema
from decorators import owner_or_admin_required

blp = Blueprint("Orders", __name__, description="Operations on orders")

@blp.route("/order/<int:order_id>")
class Order(MethodView):
    @jwt_required()
    @blp.response(200, OrderSchema)
    def get(self, order_id):
        order = OrderModel.query.get_or_404(order_id)
        user = UserModel.find_by_id(get_jwt_identity())

        if user.role == "customer" and order.user_id != user.id:
            abort(403, message="Forbidden")

        return order

    @jwt_required()
    @owner_or_admin_required(OrderModel)
    @blp.arguments(OrderStatusSchema)
    def put(self, data, order_id):
        order = OrderModel.query.get_or_404(order_id)
        order.status = data["status"]
        db.session.commit()
        return {"message": "Order status updated"}


@blp.route("/order")
class OrderList(MethodView):
    @jwt_required()
    @blp.response(200, OrderSchema(many=True))
    def get(self):
        # Add version marker to confirm new code is loaded
        print("ORDER GET - VERSION 2.0", flush=True)
        user = UserModel.find_by_id(int(get_jwt_identity()))

        if user.role == "customer":
            return OrderModel.query.filter_by(user_id=user.id).all()

        if user.role == "bakery_owner":
            return OrderModel.query.join(SurplusBagModel).filter(
                SurplusBagModel.bakery_id.in_([b.id for b in user.bakeries])
            ).all()

        return OrderModel.query.all()

    @jwt_required()
    def post(self):
        """Create a new order - VERSION 2.0"""
        print("\n" + "="*60, flush=True)
        print("ORDER POST - VERSION 2.0 - STARTED", flush=True)
        print("="*60, flush=True)
        try:
            # Get request data
            from flask import request
            data = request.get_json()
            
            if not data:
                return {"error": "No JSON data provided"}, 400
            
            # Get current user
            user_id = int(get_jwt_identity())
            
            # Extract data
            bakery_id = data.get("bakery_id")
            items_data = data.get("items", [])
            
            if not bakery_id:
                return {"error": "bakery_id is required"}, 400
            
            if not items_data:
                return {"error": "Order must contain at least one item"}, 400
            
            # Parse pickup_time if provided
            pickup_time = None
            if data.get("pickup_time"):
                try:
                    pickup_time_str = data.get("pickup_time").replace('Z', '+00:00')
                    pickup_time = datetime.fromisoformat(pickup_time_str)
                except Exception as e:
                    return {"error": f"Invalid pickup_time format: {str(e)}"}, 400
            
            # Create the order
            order = OrderModel(
                user_id=user_id,
                bakery_id=bakery_id,
                total_price=0,
                status="pending",
                pickup_time=pickup_time,
                payment_intent_id=data.get("payment_intent_id")
            )
            
            total_price = 0
            
            # Process each item
            for item_data in items_data:
                quantity = item_data["quantity"]
                
                if "product_id" in item_data and item_data["product_id"]:
                    # Handle product order
                    product = ProductModel.query.get(item_data["product_id"])
                    if not product:
                        return {"error": f"Product {item_data['product_id']} not found"}, 404
                    
                    if product.bakery_id != bakery_id:
                        return {"error": f"Product {product.name} does not belong to bakery {bakery_id}"}, 400
                    
                    if not product.is_available:
                        return {"error": f"Product {product.name} is not available"}, 400
                    
                    unit_price = float(product.price)
                    subtotal = unit_price * quantity
                    
                    order_item = OrderItemModel(
                        product_id=product.id,
                        quantity=quantity,
                        unit_price=unit_price,
                        subtotal=subtotal
                    )
                    order.order_items.append(order_item)
                    total_price += subtotal
                    
                elif "surplus_bag_id" in item_data and item_data["surplus_bag_id"]:
                    # Handle surplus bag order
                    bag = SurplusBagModel.query.get(item_data["surplus_bag_id"])
                    if not bag:
                        return {"error": f"Surplus bag {item_data['surplus_bag_id']} not found"}, 404
                    
                    if bag.bakery_id != bakery_id:
                        return {"error": f"Surplus bag {bag.title} does not belong to bakery {bakery_id}"}, 400
                    
                    if bag.quantity_available < quantity:
                        return {"error": f"Not enough {bag.title} available. Only {bag.quantity_available} left"}, 400
                    
                    unit_price = float(bag.sale_price)
                    subtotal = unit_price * quantity
                    
                    order_item = OrderItemModel(
                        surplus_bag_id=bag.id,
                        quantity=quantity,
                        unit_price=unit_price,
                        subtotal=subtotal
                    )
                    order.order_items.append(order_item)
                    bag.quantity_available -= quantity
                    
                    if len(items_data) == 1:
                        order.surplus_bag_id = bag.id
                    
                    total_price += subtotal
                else:
                    return {"error": "Each item must have either product_id or surplus_bag_id"}, 400
            
            order.total_price = total_price
            
            # Save to database
            db.session.add(order)
            db.session.commit()
            
            # Return success response
            from schemas import OrderSchema
            schema = OrderSchema()
            return schema.dump(order), 201
            
        except Exception as e:
            db.session.rollback()
            import traceback
            error_details = {
                "error": str(e),
                "type": type(e).__name__,
                "traceback": traceback.format_exc()
            }
            return error_details, 500
