from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
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
        user = UserModel.find_by_id(get_jwt_identity())

        if user.role == "customer":
            return OrderModel.query.filter_by(user_id=user.id).all()

        if user.role == "bakery_owner":
            return OrderModel.query.join(SurplusBagModel).filter(
                SurplusBagModel.bakery_id.in_([b.id for b in user.bakeries])
            ).all()

        return OrderModel.query.all()

    @jwt_required()
    @blp.arguments(OrderCreateSchema)
    @blp.response(201, OrderSchema)
    def post(self, data):
        # Debug: Print received data
        print("=" * 50)
        print("RECEIVED ORDER DATA:")
        print(f"Type: {type(data)}")
        print(f"Data: {data}")
        print("=" * 50)
        
        # Validate that all items belong to the same bakery
        bakery_id = data["bakery_id"]
        items_data = data["items"]
        
        if not items_data:
            abort(400, message="Order must contain at least one item")
        
        # Create the order
        order = OrderModel(
            user_id=get_jwt_identity(),
            bakery_id=bakery_id,
            total_price=0,
            status="pending",
            pickup_time=data.get("pickup_time"),
            payment_intent_id=data.get("payment_intent_id")
        )
        
        total_price = 0
        
        # Process each item
        for item_data in items_data:
            quantity = item_data["quantity"]
            
            if "product_id" in item_data and item_data["product_id"]:
                # Handle product order
                product = ProductModel.query.get_or_404(item_data["product_id"])
                
                if product.bakery_id != bakery_id:
                    abort(400, message=f"Product {product.name} does not belong to the specified bakery")
                
                if not product.is_available:
                    abort(400, message=f"Product {product.name} is not available")
                
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
                bag = SurplusBagModel.query.get_or_404(item_data["surplus_bag_id"])
                
                if bag.bakery_id != bakery_id:
                    abort(400, message=f"Surplus bag {bag.title} does not belong to the specified bakery")
                
                if bag.quantity_available < quantity:
                    abort(400, message=f"Not enough {bag.title} available. Only {bag.quantity_available} left")
                
                unit_price = float(bag.sale_price)
                subtotal = unit_price * quantity
                
                order_item = OrderItemModel(
                    surplus_bag_id=bag.id,
                    quantity=quantity,
                    unit_price=unit_price,
                    subtotal=subtotal
                )
                order.order_items.append(order_item)
                
                # Reduce available quantity
                bag.quantity_available -= quantity
                
                # For backward compatibility: if only one surplus bag, set it as the main surplus_bag_id
                if len(items_data) == 1:
                    order.surplus_bag_id = bag.id
                
                total_price += subtotal
            else:
                abort(400, message="Each item must have either product_id or surplus_bag_id")
        
        order.total_price = total_price
        
        db.session.add(order)
        db.session.commit()

        return order
