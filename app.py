import os
from flask import Flask, send_from_directory
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_swagger_ui import get_swaggerui_blueprint
from flask_smorest import Api
from datetime import timedelta
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash, check_password_hash
from db import db, migrate

load_dotenv()

# Import models to register them with SQLAlchemy
from models.user import UserModel
from models.bakery import BakeryModel
from models.product import ProductModel
from models.surplus_bag import SurplusBagModel
from models.order import OrderModel
from models.order_item import OrderItemModel
from models.review import ReviewModel
from models.token_blacklist import TokenBlacklist

# Import resources
from resources.auth import blp as AuthBlueprint
from resources.users import blp as UsersBlueprint
from resources.products import blp as ProductsBlueprint
from resources.orders import blp as OrdersBlueprint
from resources.reviews import blp as ReviewsBlueprint
from resources.bakeries import blp as BakeriesBlueprint
from resources.surplus_bags import blp as SurplusBagsBlueprint
from resources.recommendations import blp as RecommendationsBlueprint
from resources.analytics import blp as AnalyticsBlueprint

app = Flask(__name__)

# Configuration
app.config["API_TITLE"] = "Forni API"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.3"
app.config["OPENAPI_URL_PREFIX"] = "/"
app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI", "sqlite:///forni.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# JWT Configuration
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "jwt-secret-key-change-in-production")
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)

# Initialize extensions
db.init_app(app)
migrate.init_app(app, db)
api = Api(app)
jwt = JWTManager(app)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

# Add error handler for better debugging
@app.errorhandler(422)
def handle_unprocessable_entity(err):
    # Get validation errors from flask-smorest
    exc = err.data.get("errors", {})
    print("=" * 50)
    print("422 VALIDATION ERROR:")
    print(f"Errors: {exc}")
    print(f"Full error data: {err.data}")
    print("=" * 50)
    return {"errors": exc, "message": "Validation failed"}, 422

# Serve swagger.json
@app.route('/swagger.json')
def swagger_json():
    return send_from_directory('.', 'swagger.json')

# Serve frontend
@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

# Serve uploaded images
@app.route('/static/uploads/<folder>/<filename>')
def uploaded_file(folder, filename):
    return send_from_directory(f'static/uploads/{folder}', filename)

# Swagger UI configuration
SWAGGER_URL = '/api/docs'
API_URL = '/swagger.json'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={'app_name': "Forni API"}
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

# JWT token blacklist loader
@jwt.token_in_blocklist_loader
def check_if_token_in_blacklist(jwt_header, jwt_payload):
    jti = jwt_payload['jti']
    token = TokenBlacklist.query.filter_by(jti=jti).first()
    return token is not None

# JWT error handlers
@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return {"message": "Token has expired", "error": "token_expired"}, 401

@jwt.invalid_token_loader
def invalid_token_callback(error):
    print("=" * 50)
    print("INVALID TOKEN ERROR:")
    print(f"Error: {error}")
    print("=" * 50)
    return {"message": "Invalid token", "error": "invalid_token", "details": str(error)}, 401

@jwt.unauthorized_loader
def missing_token_callback(error):
    print("=" * 50)
    print("MISSING TOKEN ERROR:")
    print(f"Error: {error}")
    print("=" * 50)
    return {"message": "Authorization token is missing", "error": "authorization_required"}, 401

@jwt.revoked_token_loader
def revoked_token_callback(jwt_header, jwt_payload):
    return {"message": "Token has been revoked", "error": "token_revoked"}, 401

# Register blueprints
api.register_blueprint(AuthBlueprint)
api.register_blueprint(UsersBlueprint)
api.register_blueprint(ProductsBlueprint)
api.register_blueprint(OrdersBlueprint)
api.register_blueprint(ReviewsBlueprint)
api.register_blueprint(BakeriesBlueprint)
api.register_blueprint(SurplusBagsBlueprint)
api.register_blueprint(RecommendationsBlueprint)
api.register_blueprint(AnalyticsBlueprint)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)
