from resources.auth import blp as AuthBlueprint
from resources.users import blp as UsersBlueprint
from resources.bakeries import blp as BakeriesBlueprint
from resources.products import blp as ProductsBlueprint
from resources.surplus_bags import blp as SurplusBagsBlueprint
from resources.orders import blp as OrdersBlueprint
from resources.reviews import blp as ReviewsBlueprint
from resources.analytics import blp as AnalyticsBlueprint
from resources.recommendations import blp as RecommendationsBlueprint

def register_blueprints(app):
    app.register_blueprint(AuthBlueprint, url_prefix="/api/v1/auth")
    app.register_blueprint(UsersBlueprint, url_prefix="/api/v1/users")
    app.register_blueprint(BakeriesBlueprint, url_prefix="/api/v1/bakeries")
    app.register_blueprint(ProductsBlueprint, url_prefix="/api/v1/products")
    app.register_blueprint(SurplusBagsBlueprint, url_prefix="/api/v1/surplus-bags")
    app.register_blueprint(OrdersBlueprint, url_prefix="/api/v1/orders")
    app.register_blueprint(ReviewsBlueprint, url_prefix="/api/v1/reviews")
    app.register_blueprint(AnalyticsBlueprint, url_prefix="/api/v1/analytics")
    app.register_blueprint(RecommendationsBlueprint, url_prefix="/api/v1/recommendations")
