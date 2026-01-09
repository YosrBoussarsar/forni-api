"""
Simple database migration - adds phone and opening_hours to bakeries table
"""
import sqlite3
import os

db_path = "instance/forni.db"

if not os.path.exists(db_path):
    print(f"Database not found at {db_path}")
    exit(1)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

try:
    # Check if column exists
    cursor.execute("PRAGMA table_info(bakeries)")
    columns = [col[1] for col in cursor.fetchall()]
    
    # Add phone column if it doesn't exist
    if 'phone' not in columns:
        cursor.execute("ALTER TABLE bakeries ADD COLUMN phone VARCHAR(50)")
        print("Added 'phone' column to bakeries table")
    else:
        print("'phone' column already exists")
    
    # Add opening_hours column if it doesn't exist
    if 'opening_hours' not in columns:
        cursor.execute("ALTER TABLE bakeries ADD COLUMN opening_hours VARCHAR(100)")
        print("Added 'opening_hours' column to bakeries table")
    else:
        print("'opening_hours' column already exists")
    
    conn.commit()
    print("\nDatabase migration completed successfully!")
    
except Exception as e:
    print(f"Error during migration: {e}")
    conn.rollback()
finally:
    conn.close()
