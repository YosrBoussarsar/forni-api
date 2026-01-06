from marshmallow import Schema, fields, validates, ValidationError, pre_load, EXCLUDE
import re

# ============================================================
# USER SCHEMAS
# ============================================================

class PlainUserSchema(Schema):
    id = fields.Int(dump_only=True)
    email = fields.Email(required=True)
    first_name = fields.Str()
    last_name = fields.Str()
    phone = fields.Str()
    role = fields.Str(dump_only=True)
    latitude = fields.Float()
    longitude = fields.Float()
    created_at = fields.DateTime(dump_only=True)


class UserRegisterSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True)
    first_name = fields.Str(required=False)
    last_name = fields.Str(required=False)
    phone = fields.Str(required=False)
    role = fields.Str(required=False)

    @pre_load
    def set_default_role(self, data, **kwargs):
        if "role" not in data or not data["role"]:
            data["role"] = "customer"
        return data

    @validates("password")
    def validate_password(self, value, **kwargs):
        if len(value) < 8:
            raise ValidationError("Password must be at least 8 characters long")
        if not re.search(r"[A-Z]", value):
            raise ValidationError("Password must contain at least one uppercase letter")
        if not re.search(r"[a-z]", value):
            raise ValidationError("Password must contain at least one lowercase letter")
        if not re.search(r"\d", value):
            raise ValidationError("Password must contain at least one digit")

    @validates("role")
    def validate_role(self, value, **kwargs):
        if value not in ["customer", "bakery_owner", "admin"]:
            raise ValidationError("Role must be customer, bakery_owner, or admin")


class UserLoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True)


class UserSchema(PlainUserSchema):
    pass


class UserUpdateSchema(Schema):
    class Meta:
        unknown = EXCLUDE  # Ignore unknown fields
    
    first_name = fields.Str()
    last_name = fields.Str()
    phone = fields.Str()
    latitude = fields.Float()
    longitude = fields.Float()


# ============================================================
# BAKERY SCHEMAS
# ============================================================

class PlainBakerySchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    city = fields.Str()
    governorate = fields.Str()
    rating = fields.Float(dump_only=True)
    image_url = fields.Str()


class BakeryCreateSchema(Schema):
    name = fields.Str(required=True)
    description = fields.Str()
    address = fields.Str()
    city = fields.Str()
    governorate = fields.Str()
    latitude = fields.Float()
    longitude = fields.Float()
    specialties = fields.Str()
    image_url = fields.Str()


class BakeryUpdateSchema(Schema):
    name = fields.Str()
    description = fields.Str()
    address = fields.Str()
    city = fields.Str()
    governorate = fields.Str()
    latitude = fields.Float()
    longitude = fields.Float()
    specialties = fields.Str()
    image_url = fields.Str()


class BakerySchema(PlainBakerySchema):
    owner_id = fields.Int(dump_only=True)
    description = fields.Str()
    address = fields.Str()
    latitude = fields.Float()
    longitude = fields.Float()
    specialties = fields.Str()
    review_count = fields.Int(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    products = fields.List(fields.Nested(lambda: PlainProductSchema()), dump_only=True)
    surplus_bags = fields.List(fields.Nested(lambda: PlainSurplusBagSchema()), dump_only=True)


# ============================================================
# PRODUCT SCHEMAS
# ============================================================

class PlainProductSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    price = fields.Float(required=True)
    category = fields.Str()
    allergens = fields.Str()
    tags = fields.Str()
    is_available = fields.Bool()
    image_url = fields.Str()


class ProductCreateSchema(Schema):
    bakery_id = fields.Int(required=True)
    name = fields.Str(required=True)
    description = fields.Str()
    category = fields.Str()
    price = fields.Float(required=True)
    allergens = fields.Str()
    tags = fields.Str()
    is_available = fields.Bool()
    image_url = fields.Str()


class ProductUpdateSchema(Schema):
    name = fields.Str()
    description = fields.Str()
    category = fields.Str()
    price = fields.Float()
    allergens = fields.Str()
    tags = fields.Str()
    is_available = fields.Bool()
    image_url = fields.Str()


class ProductSchema(PlainProductSchema):
    bakery_id = fields.Int(required=True, load_only=True)
    description = fields.Str()
    created_at = fields.DateTime(dump_only=True)
    bakery = fields.Nested(PlainBakerySchema(), dump_only=True)


# ============================================================
# SURPLUS BAG SCHEMAS
# ============================================================

class PlainSurplusBagSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    sale_price = fields.Float(required=True)
    original_value = fields.Float(required=True)
    quantity_available = fields.Int()
    status = fields.Str()
    tags = fields.Str()
    image_url = fields.Str()
    pickup_start = fields.DateTime()
    pickup_end = fields.DateTime()


class SurplusBagCreateSchema(Schema):
    bakery_id = fields.Int(required=True)
    title = fields.Str(required=True)
    description = fields.Str()
    category = fields.Str()
    tags = fields.Str()
    original_value = fields.Float(required=True)
    sale_price = fields.Float(required=True)
    quantity_available = fields.Int(required=True)
    pickup_start = fields.DateTime(required=True)
    pickup_end = fields.DateTime(required=True)
    image_url = fields.Str()


class SurplusBagUpdateSchema(Schema):
    title = fields.Str()
    description = fields.Str()
    category = fields.Str()
    tags = fields.Str()
    original_value = fields.Float()
    sale_price = fields.Float()
    quantity_available = fields.Int()
    status = fields.Str()
    pickup_start = fields.DateTime()
    pickup_end = fields.DateTime()
    image_url = fields.Str()


class SurplusBagSchema(PlainSurplusBagSchema):
    bakery_id = fields.Int(load_only=True)
    description = fields.Str()
    category = fields.Str()
    created_at = fields.DateTime(dump_only=True)
    bakery = fields.Nested(PlainBakerySchema(), dump_only=True)


# ============================================================
# ORDER ITEM SCHEMAS
# ============================================================

class OrderItemCreateSchema(Schema):
    class Meta:
        unknown = EXCLUDE  # Ignore unknown fields
    
    product_id = fields.Int()
    surplus_bag_id = fields.Int()
    quantity = fields.Int(required=True)


class OrderItemSchema(Schema):
    id = fields.Int(dump_only=True)
    product_id = fields.Int()
    surplus_bag_id = fields.Int()
    quantity = fields.Int()
    unit_price = fields.Float()
    subtotal = fields.Float()
    product = fields.Nested(PlainProductSchema(), dump_only=True)
    surplus_bag = fields.Nested(PlainSurplusBagSchema(), dump_only=True)


# ============================================================
# ORDER SCHEMAS
# ============================================================

class PlainOrderSchema(Schema):
    id = fields.Int(dump_only=True)
    status = fields.Str()
    total_price = fields.Float()
    pickup_code = fields.Str(dump_only=True)


class OrderCreateSchema(Schema):
    class Meta:
        unknown = EXCLUDE  # Ignore unknown fields
    
    bakery_id = fields.Int(required=True)
    items = fields.List(fields.Nested(OrderItemCreateSchema), required=True)
    pickup_time = fields.Str()  # Changed from DateTime to Str to accept any format
    payment_intent_id = fields.Str()


class OrderStatusSchema(Schema):
    status = fields.Str(required=True)


class OrderSchema(PlainOrderSchema):
    user_id = fields.Int(dump_only=True)
    bakery_id = fields.Int(dump_only=True)
    surplus_bag_id = fields.Int(dump_only=True)
    pickup_time = fields.DateTime()
    payment_intent_id = fields.Str()
    created_at = fields.DateTime(dump_only=True)
    user = fields.Nested(PlainUserSchema(), dump_only=True)
    bakery = fields.Nested(PlainBakerySchema(), dump_only=True)
    surplus_bag = fields.Nested(PlainSurplusBagSchema(), dump_only=True)
    order_items = fields.List(fields.Nested(OrderItemSchema()), dump_only=True)


# ============================================================
# REVIEW SCHEMAS
# ============================================================

class PlainReviewSchema(Schema):
    id = fields.Int(dump_only=True)
    rating = fields.Int(required=True)
    comment = fields.Str()
    created_at = fields.DateTime(dump_only=True)


class ReviewCreateSchema(Schema):
    order_id = fields.Int(required=True)
    rating = fields.Int(required=True)
    comment = fields.Str()


class ReviewUpdateSchema(Schema):
    rating = fields.Int()
    comment = fields.Str()


class ReviewSchema(PlainReviewSchema):
    user_id = fields.Int(dump_only=True)
    bakery_id = fields.Int(dump_only=True)
    surplus_bag_id = fields.Int(dump_only=True)
    user = fields.Nested(PlainUserSchema(), dump_only=True)
    bakery = fields.Nested(PlainBakerySchema(), dump_only=True)

