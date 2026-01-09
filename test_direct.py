"""Direct test without HTTP - to verify code changes"""
from app import create_app, db
from models.user import UserModel
from models.bakery import BakeryModel
from werkzeug.security import generate_password_hash
from flask_jwt_extended import create_access_token

app = create_app()

with app.app_context():
    # Create test user if doesn't exist
    user = UserModel.query.filter_by(email="test@owner.com").first()
    if not user:
        user = UserModel(
            email="test@owner.com",
            password_hash=generate_password_hash("Test123!"),
            first_name="Test",
            last_name="Owner",
            phone="12345678",
            role="bakery_owner"
        )
        db.session.add(user)
        db.session.commit()
        print(f"Created user with ID: {user.id}")
    else:
        print(f"Using existing user with ID: {user.id}")
    
    # Create token with STRING identity (the fix)
    print(f"\nCreating token with identity=str({user.id}) = '{str(user.id)}'")
    token = create_access_token(identity=str(user.id))
    print(f"Token created successfully")
    print(f"Token (first 50 chars): {token[:50]}...")
    
    # Now test creating a bakery
    print(f"\nAttempting to create bakery...")
    bakery = BakeryModel(
        name="Direct Test Bakery",
        description="Testing direct creation",
        address="123 Test St",
        city="Tunis",
        owner_id=user.id
    )
    db.session.add(bakery)
    db.session.commit()
    print(f"✅ Bakery created successfully with ID: {bakery.id}")
    
    # Clean up
    db.session.delete(bakery)
    db.session.commit()
    print(f"✅ Test bakery deleted")
