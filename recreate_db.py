"""
Recreate database with new schema
"""
import os
from app import create_app
from db import db
from werkzeug.security import generate_password_hash
from models.user import UserModel

# Remove old database
db_path = "instance/data.db"
if os.path.exists(db_path):
    os.remove(db_path)
    print(f"Removed old database: {db_path}")

# Create new database
app = create_app()

with app.app_context():
    db.create_all()
    print("Database tables created with new schema!")
    
    # Create default admin user
    admin = UserModel(
        email="admin@forni.tn",
        password_hash=generate_password_hash("Admin123!"),
        role="admin",
        first_name="Admin",
        last_name="User",
    )
    db.session.add(admin)
    db.session.commit()
    print("Default admin user created (email: admin@forni.tn, password: Admin123!)")
    
print("\nDatabase recreated successfully!")
print("You can now run: python seed.py (if you have seed data)")
