#resources/users.py
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from db import db
from models.user import UserModel
from schemas import UserSchema, UserUpdateSchema

blp = Blueprint("Users", __name__, description="User profile operations")

@blp.route("/profile")
class UserProfile(MethodView):
    @jwt_required()
    def get(self):
        try:
            from flask import jsonify
            user = UserModel.find_by_id(get_jwt_identity())
            if not user:
                abort(404, message="User not found")
            
            # Manual serialization
            result = {
                "id": user.id,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "phone": user.phone,
                "role": user.role,
                "latitude": user.latitude,
                "longitude": user.longitude,
                "created_at": user.created_at.isoformat() if user.created_at else None
            }
            return jsonify(result), 200
        except Exception as e:
            print(f"DEBUG ERROR in profile GET: {type(e).__name__}: {str(e)}")
            import traceback
            traceback.print_exc()
            raise

    @jwt_required()
    @blp.arguments(UserUpdateSchema)
    @blp.response(200, UserSchema)
    def put(self, data):
        user = UserModel.find_by_id(get_jwt_identity())
        if not user:
            abort(404, message="User not found")

        user.first_name = data.get("first_name", user.first_name)
        user.last_name = data.get("last_name", user.last_name)
        user.phone = data.get("phone", user.phone)
        
        # Update location if provided
        if "latitude" in data:
            user.latitude = data["latitude"]
        if "longitude" in data:
            user.longitude = data["longitude"]

        db.session.commit()
        return user

