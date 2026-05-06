import uuid
import sys
import os

# Add the Backend folder to path
sys.path.append(os.getcwd())

from Database.DB import SessionLocal
from Models.User_Tables.User_Profile import user_profile_table
from Models.User_Tables.User_Access import user_access_table
from utils.security import hash_password

def create_admin():
    db = SessionLocal()
    try:
        email = "parthasarathyg693@gmail.com"
        password = "Partha#123"
        
        # Check if user already exists
        existing_user = db.query(user_profile_table).filter(user_profile_table.user_email == email).first()
        if existing_user:
            print(f"User with email {email} already exists.")
            return

        user_id = str(uuid.uuid4())
        
        # 1. Create Profile
        new_profile = user_profile_table(
            user_id=user_id,
            user_name="Admin",
            user_email=email,
            user_email_verified=True,
            Status="active"
        )
        db.add(new_profile)
        
        # 2. Create Access (Password and Role)
        new_access = user_access_table(
            access_id=str(uuid.uuid4()),
            user_id=user_id,
            provider_id=email,
            provider_name="credentials",
            role="admin",
            password_hash=hash_password(password)
        )
        db.add(new_access)
        
        db.commit()
        print(f"✅ Admin user {email} created successfully!")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error creating admin: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    create_admin()
