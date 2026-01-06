from db import db

class OrderItemModel(db.Model):
    __tablename__ = "order_items"

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"), nullable=False)
    
    # Either product_id or surplus_bag_id will be set, not both
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=True)
    surplus_bag_id = db.Column(db.Integer, db.ForeignKey("surplus_bags.id"), nullable=True)
    
    quantity = db.Column(db.Integer, nullable=False, default=1)
    unit_price = db.Column(db.Numeric(10, 2), nullable=False)
    subtotal = db.Column(db.Numeric(10, 2), nullable=False)

    order = db.relationship("OrderModel", back_populates="order_items")
    product = db.relationship("ProductModel", backref="order_items")
    surplus_bag = db.relationship("SurplusBagModel", backref="order_items")
