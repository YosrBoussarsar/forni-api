from functools import wraps
from flask_jwt_extended import get_jwt_identity
from flask_smorest import abort
from models.user import UserModel
from db import db


def admin_required():
    """Allow only admin users."""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            user = UserModel.find_by_id(get_jwt_identity())
            if not user or user.role != "admin":
                abort(403, message="Admin privileges required")
            return fn(*args, **kwargs)
        return wrapper
    return decorator


def owner_required(model):
    """
    Allow only the owner of the resource.
    Works for BakeryModel, ProductModel, SurplusBagModel, OrderModel.
    """
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            user = UserModel.find_by_id(get_jwt_identity())
            resource_id = kwargs.get("bakery_id") or kwargs.get("product_id") or kwargs.get("bag_id") or kwargs.get("order_id")

            resource = model.query.get_or_404(resource_id)

            # BakeryModel → owner_id
            # ProductModel → bakery.owner_id
            # SurplusBagModel → bakery.owner_id
            # OrderModel → bakery.owner_id
            owner_id = None

            if hasattr(resource, "owner_id"):
                owner_id = resource.owner_id
            elif hasattr(resource, "bakery") and hasattr(resource.bakery, "owner_id"):
                owner_id = resource.bakery.owner_id

            if user.id != owner_id:
                abort(403, message="Only the owner can perform this action")

            return fn(*args, **kwargs)
        return wrapper
    return decorator


def owner_or_admin_required(model):
    """
    Allow only:
    - the owner of the resource
    - OR an admin
    """
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            user = UserModel.find_by_id(get_jwt_identity())
            resource_id = (
                kwargs.get("bakery_id")
                or kwargs.get("product_id")
                or kwargs.get("bag_id")
                or kwargs.get("order_id")
            )

            resource = model.query.get_or_404(resource_id)

            # Determine owner
            owner_id = None
            if hasattr(resource, "owner_id"):
                owner_id = resource.owner_id
            elif hasattr(resource, "bakery") and hasattr(resource.bakery, "owner_id"):
                owner_id = resource.bakery.owner_id

            # Check permissions
            if user.role != "admin" and user.id != owner_id:
                abort(403, message="Only the owner or an admin can perform this action")

            return fn(*args, **kwargs)
        return wrapper
    return decorator
