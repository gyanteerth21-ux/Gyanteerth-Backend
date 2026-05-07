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
        user = db.query(user_profile_table).filter(user_profile_table.user_email == email).first()
        
        if not user:
            user_id = str(uuid.uuid4())
            # 1. Create Profile
            user = user_profile_table(
                user_id=user_id,
                user_name="Admin",
                user_email=email,
                user_email_verified=True,
                Status="active"
            )
            db.add(user)
            print(f"Created new profile for {email}")
        else:
            user_id = user.user_id
            print(f"Using existing profile for {email}")
        
        # 2. Check if Access already exists
        access = db.query(user_access_table).filter(user_access_table.user_id == user_id).first()
        
        if access:
            access.role = "admin"
            access.password_hash = hash_password(password)
            access.provider_name = "credentials"
            print(f"Updated existing access record to admin.")
        else:
            # Create new access record
            new_access = user_access_table(
                access_id=str(uuid.uuid4()),
                user_id=user_id,
                provider_id=email,
                provider_name="credentials",
                role="admin",
                password_hash=hash_password(password)
            )
            db.add(new_access)
            print(f"Created new access record as admin.")
        
        db.commit()
        print(f"✅ Admin user {email} is now ready!")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error creating admin: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    create_admin()
