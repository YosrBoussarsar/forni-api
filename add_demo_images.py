from app import create_app, db
from models.bakery import BakeryModel
from models.product import ProductModel

app = create_app()

with app.app_context():
    # Update bakery images
    bakery_updates = [
        ("La Baguette Dorée", "https://images.unsplash.com/photo-1519864600265-abb23847ef2c"),
        ("Sweet Crumbs", "https://images.unsplash.com/photo-1504674900247-0877df9cc836"),
        ("Pain Artisan", "https://images.unsplash.com/photo-1464306076886-debede6bbf94"),
    ]
    for name, url in bakery_updates:
        bakery = BakeryModel.query.filter_by(name=name).first()
        if bakery:
            bakery.image_url = url
            print(f"Updated bakery: {name}")
    db.session.commit()

    # Update product images
    product_updates = [
        ("Croissant", "https://images.unsplash.com/photo-1502741338009-cac2772e18bc"),
        ("Pain au Chocolat", "https://images.unsplash.com/photo-1519864600265-abb23847ef2c"),
        ("Baguette", "https://images.unsplash.com/photo-1504674900247-0877df9cc836"),
        ("Éclair", "https://images.unsplash.com/photo-1464306076886-debede6bbf94"),
        ("Macaron Box (6)", "https://images.unsplash.com/photo-1505250463726-0d238b6b09b0"),
    ]
    for name, url in product_updates:
        product = ProductModel.query.filter_by(name=name).first()
        if product:
            product.image_url = url
            print(f"Updated product: {name}")
    db.session.commit()

    print("Demo images added!")
