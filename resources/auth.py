#resources\auth.py
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import (
    create_access_token, create_refresh_token,
    jwt_required, get_jwt_identity, get_jwt
)
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta

from db import db
from models.user import UserModel
from schemas import UserRegisterSchema, UserLoginSchema, UserSchema

blp = Blueprint("Auth", __name__,  description="Authentication operations")

@blp.route("/register")
class Register(MethodView):
    @blp.arguments(UserRegisterSchema)
    @blp.response(201, UserSchema)
    def post(self, user_data):
        if UserModel.query.filter_by(email=user_data["email"]).first():
            abort(409, message="Email already exists")

        user = UserModel(
            email=user_data["email"],
            password_hash=generate_password_hash(user_data["password"]),
            role=user_data.get("role", "customer"),
            first_name=user_data.get("first_name"),
            last_name=user_data.get("last_name"),
            phone=user_data.get("phone"),
        )

        db.session.add(user)
        db.session.commit()
        return user


@blp.route("/login")
class Login(MethodView):
    @blp.arguments(UserLoginSchema)
    def post(self, data):
        user = UserModel.query.filter_by(email=data["email"]).first()

        if not user or not check_password_hash(user.password_hash, data["password"]):
            abort(401, message="Invalid credentials")

        access = create_access_token(identity=str(user.id), expires_delta=timedelta(hours=1))
        refresh = create_refresh_token(identity=str(user.id))

        return {
            "access_token": access,
            "refresh_token": refresh,
            "user": {
                "id": user.id,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "role": user.role,
                "phone": user.phone
            }
        }


@blp.route("/refresh")
class Refresh(MethodView):
    @jwt_required(refresh=True)
    def post(self):
        user_id = get_jwt_identity()
        new_access = create_access_token(identity=str(user_id))
        return {"access_token": new_access}


@blp.route("/logout")
class Logout(MethodView):
    @jwt_required()
    def post(self):
        jti = get_jwt()["jti"]
        # Add to blocklist (you must implement blocklist storage)
        return {"message": "Logged out"}
