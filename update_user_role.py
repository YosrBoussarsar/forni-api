"""
Quick script to update user role to bakery_owner
"""
from app import app
from db import db
from models.user import UserModel

def update_user_role():
    with app.app_context():
        email = input("Enter user email: ")
        user = UserModel.query.filter_by(email=email).first()
        
        if not user:
            print(f"❌ No user found with email: {email}")
            return
        
        print(f"\nCurrent user info:")
        print(f"  Email: {user.email}")
        print(f"  Name: {user.first_name} {user.last_name}")
        print(f"  Current Role: {user.role}")
        
        print("\nAvailable roles:")
        print("  1. customer")
        print("  2. bakery_owner")
        print("  3. admin")
        
        choice = input("\nSelect new role (1-3): ")
        
        role_map = {
            "1": "customer",
            "2": "bakery_owner",
            "3": "admin"
        }
        
        new_role = role_map.get(choice)
        
        if not new_role:
            print("❌ Invalid choice")
            return
        
        user.role = new_role
        db.session.commit()
        
        print(f"\n✅ User role updated to: {new_role}")
        print(f"Please login again to see the changes.")

if __name__ == "__main__":
    update_user_role()
