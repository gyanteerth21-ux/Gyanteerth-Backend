import uuid
import random
from datetime import datetime, timedelta
from aiohttp import request
from sqlalchemy.orm import Session
from fastapi import HTTPException,Request,Depends,status
from fastapi.security import HTTPBearer,HTTPAuthorizationCredentials
from Models.User_Tables.User_Profile import user_profile_table
from Models.User_Tables.User_Refresh_Token import user_refresh_token_table
from Models.User_Tables.User_OTP import user_otp_table
from Models.User_Tables.User_Access import user_access_table
from utils.Emailservice import send_email
from sqlalchemy.exc import IntegrityError
from Database.DB import get_db
from utils.email_templates.otp_design import otp_email_template,forget_password_email_template
from utils.security import hash_password, verify_password
from utils.security import create_access_token, decode_token
from utils.security import create_refresh_token,create_forget_token
from google.oauth2 import id_token
from google.auth.transport import requests
from fastapi import Request
from dotenv import load_dotenv, find_dotenv
import os
load_dotenv(find_dotenv())

REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", 7))
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")


class user_Authorization(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(user_Authorization, self).__init__(auto_error=auto_error)
    async def __call__(self, request: Request ):
        credentials: HTTPAuthorizationCredentials = await super(user_Authorization, self).__call__(request)
        if not credentials:
            raise HTTPException(status_code=401, detail="Invalid authorization code")
        try:
            token = decode_token(credentials.credentials)
            if not token:
                raise HTTPException(status_code=401, detail="Invalid token")

            if token.get("role").lower() != "user":
                raise HTTPException(status_code=403, detail="Permission denied")
            return token
        
        except HTTPException:
            raise   
        except Exception as e:
            print("Token decode error:", e)
            raise HTTPException(status_code=401, detail=str(e))

class admin_Authorization(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(admin_Authorization, self).__init__(auto_error=auto_error)
    async def __call__(self, request: Request ):
        credentials: HTTPAuthorizationCredentials = await super(admin_Authorization, self).__call__(request)
        if not credentials:
            raise HTTPException(status_code=401, detail="Invalid authorization code")
        try:
            token = decode_token(credentials.credentials)
            if not token:
                raise HTTPException(status_code=401, detail="Invalid token")

            if token.get("role").lower() != "admin":
                raise HTTPException(status_code=403, detail="Permission denied")
            return token
        
        except HTTPException:
            raise   
        except Exception as e:
            print("Token decode error:", e)
            raise HTTPException(status_code=401, detail=str(e))

class trainer_Authorization(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(trainer_Authorization, self).__init__(auto_error=auto_error)
    async def __call__(self, request: Request ):
        credentials: HTTPAuthorizationCredentials = await super(trainer_Authorization, self).__call__(request)
        if not credentials:
            raise HTTPException(status_code=401, detail="Invalid authorization code")
        try:
            token = decode_token(credentials.credentials)
            if not token:
                raise HTTPException(status_code=401, detail="Invalid token")

            if token.get("role").lower() not in ["trainer", "admin"]:
                raise HTTPException(status_code=403, detail="Permission denied")
            return token
        
        except HTTPException:
            raise   
        except Exception as e:
            print("Token decode error:", e)
            raise HTTPException(status_code=401, detail=str(e))

class full_Authorization(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(full_Authorization, self).__init__(auto_error=auto_error)
    async def __call__(self, request: Request ):
        credentials: HTTPAuthorizationCredentials = await super(full_Authorization, self).__call__(request)
        if not credentials:
            raise HTTPException(status_code=401, detail="Invalid authorization code")
        try:
            token = decode_token(credentials.credentials)
            if not token:
                raise HTTPException(status_code=401, detail="Invalid token")

            if token.get("role").lower() not in ["user", "trainer", "admin"]:
                raise HTTPException(status_code=403, detail="Permission denied")
            return token
        
        except HTTPException:
            raise   
        except Exception as e:
            print("Token decode error:", e)
            raise HTTPException(status_code=401, detail=str(e))

class AuthService:

    async def refresh_token_check_service(self, data, db: Session):
        try:
            token_data = decode_token(data.refresh_token)
    
            if not token_data or token_data.get("type") != "refresh":
                raise HTTPException(status_code=401, detail="Invalid refresh token")
    
            user_id = token_data.get("user_id")
    
            token_record = db.query(user_refresh_token_table).filter(
                user_refresh_token_table.user_id == user_id,
                user_refresh_token_table.refresh_token == data.refresh_token,
                user_refresh_token_table.is_revoked == False,
                user_refresh_token_table.expires_at > datetime.utcnow()
            ).first()
    
            if not token_record:
                raise HTTPException(
                    status_code=401,
                    detail="Refresh token is invalid, revoked, or expired"
                )
    
            access_token = create_access_token(user_id, "user")
    
            return {
                "success": True,
                "access_token": access_token
            }

        except HTTPException as http_err:
        
            raise http_err
    
        except Exception as e:
            
            print(f"Error in refresh_token_check_service: {str(e)}")
    
            raise HTTPException(
                status_code=500,
                detail="Internal server error while refreshing token"
            )
    
    
    async def login_service(self, data,  request:Request, db: Session):

        result = (
            db.query(user_profile_table, user_access_table)
            .join(
                user_access_table,
                user_access_table.user_id == user_profile_table.user_id
            )
            .filter(
                user_profile_table.user_email == data.Email,
                user_profile_table.user_email_verified == True
            )
            .first()
        )
        
        if not result:
            raise HTTPException(status_code=400, detail="Invalid email or password")
        
        user, access_record = result
        
        print(f"DEBUG: PASSWORD LENGTH: {len(data.password)}")
        
        if not verify_password(data.password, access_record.password_hash):
            raise HTTPException(status_code=400, detail="Invalid email or password")
        user_agent = request.headers.get("user-agent", "Unknown")
        device_name = "Unknown"
    
        if "Windows" in user_agent:
            device_name = "Windows PC"
        elif "Android" in user_agent:
            device_name = "Android Phone"
        elif "iPhone" in user_agent:
            device_name = "iPhone"
        elif "Mac" in user_agent:
            device_name = "Mac"
    
        client_ip = request.headers.get("x-forwarded-for", "Unknown")
        if client_ip == "Unknown" and request.client:
            client_ip = request.client.host
            
        if client_ip:
            client_ip = client_ip.split(",")[0].strip()[:50]
        else:
            client_ip = "Unknown"

        re_refresh_token = create_refresh_token(user.user_id)
        
        # Check if refresh token record exists, if not create one
        token_record = db.query(user_refresh_token_table).filter(
            user_refresh_token_table.user_id == user.user_id
        ).first()

        if token_record:
            token_record.refresh_token = re_refresh_token
            token_record.ip_address = client_ip
            token_record.user_agent = user_agent
            token_record.device_name = device_name
            token_record.expires_at = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
            token_record.is_revoked = False
        else:
            new_token_record = user_refresh_token_table(
                refresh_token_id=f"RefreshToken-{uuid.uuid4()}",
                user_id=user.user_id,
                refresh_token=re_refresh_token,
                ip_address=client_ip,
                user_agent=user_agent,
                device_name=device_name,
                expires_at=datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS),
                is_revoked=False
            )
            db.add(new_token_record)

        db.commit()
        return {
            "success": True,
            "message": "Login successful",
            "role": access_record.role,
            "access_token": create_access_token(user.user_id, access_record.role),
            "refresh_token": re_refresh_token
        }
    
    async def forget_password_token_email(self, data, db: Session):
        result = (
            db.query(user_profile_table, user_access_table)
            .join(
                user_access_table,
                user_access_table.user_id == user_profile_table.user_id
            )
            .filter(
                user_profile_table.user_email == data.email,
                user_profile_table.user_email_verified == True
            )
            .first()
        )

        if not result:
            raise HTTPException(status_code=400, detail="Invalid email or password")
        
        user, access_record = result

        if not user or access_record.role == "Admin":
            raise HTTPException(status_code=400, detail="User or trainer with this email does not exist")

        forget_token = create_forget_token(user.user_id, "user")
        subject = "Gyanteerth Password Reset Code"
        body = forget_password_email_template(forget_token)
        # Sending email directly (await) instead of background task
        # so it works reliably on free-tier deployments
        await send_email(data.email, subject, body)
        return {
            "success": True,
            "message": "Password reset token sent to your email"
        }
    
    async def update_password_service(self, data, db: Session):

        token_data = decode_token(data.token)

        if not token_data or token_data.get("type") != "forget":
            raise HTTPException(status_code=401, detail="Invalid forget token")

        user_id = token_data.get("user_id")

        result = (
            db.query(user_profile_table, user_access_table)
            .join(
                user_access_table,
                user_access_table.user_id == user_profile_table.user_id
            )
            .filter(
                user_profile_table.user_id == user_id,
                user_profile_table.user_email_verified == True
            )
            .first()
        )
        if not result:
            raise HTTPException(status_code=400, detail="User not found or email not verified")
        
        user, access_record = result

        if not user:
            raise HTTPException(status_code=400, detail="User not found")

        if not access_record:
            raise HTTPException(status_code=400, detail="User does not have an email access account")

        access_record.password_hash = hash_password(data.new_password)
        db.commit()

        return {
            "success": True,
            "message": "Password updated successfully"
        }

    # ── Student Self-Registration ──────────────────────────────────────────────

    async def register_student_service(self, data, background_tasks, db: Session):
        """
        Step 1 – Register a new student.
        Creates an unverified user profile and sends a 6-digit OTP to the email.
        """
        try:
            # Check if a verified account already exists for this email
            existing = db.query(user_profile_table).filter(
                user_profile_table.user_email == data.email,
                user_profile_table.user_email_verified == True
            ).first()

            if existing:
                raise HTTPException(
                    status_code=400,
                    detail="An account with this email already exists. Please log in."
                )

            # If an unverified profile exists, reuse it (allow re-sending OTP)
            unverified = db.query(user_profile_table).filter(
                user_profile_table.user_email == data.email,
                user_profile_table.user_email_verified == False
            ).first()

            if unverified:
                user_id = unverified.user_id
                # Update name in case it changed
                unverified.user_name = data.name
            else:
                user_id = f"USER-{uuid.uuid4()}"
                new_user = user_profile_table(
                    user_id=user_id,
                    user_name=data.name,
                    user_email=data.email,
                    user_email_verified=False,
                    Status="Pending"
                )
                db.add(new_user)
                db.flush()

            # Generate a 6-digit OTP
            otp_value = random.randint(100000, 999999)
            expires_at = datetime.utcnow() + timedelta(minutes=5)

            # Upsert OTP record (one OTP row per user)
            existing_otp = db.query(user_otp_table).filter(
                user_otp_table.user_id == user_id
            ).first()

            if existing_otp:
                existing_otp.otp = otp_value
                existing_otp.expires_at = expires_at
                existing_otp.is_used = False
            else:
                new_otp = user_otp_table(
                    otp_id=f"OTP-{uuid.uuid4()}",
                    user_id=user_id,
                    otp=otp_value,
                    expires_at=expires_at,
                    is_used=False
                )
                db.add(new_otp)

            db.commit()

            # Send OTP email in background
            subject = "Verify your Gyanteerth account"
            body = otp_email_template(str(otp_value))
            background_tasks.add_task(send_email, data.email, subject, body)

            return {
                "success": True,
                "message": "OTP sent to your email. Please verify to complete registration.",
                "user_id": user_id
            }

        except HTTPException:
            raise
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Registration failed: {str(e)}")

    async def verify_email_and_set_password_service(self, data, db: Session):
        """
        Step 2 – Verify OTP and set password to complete registration.
        Marks the user as verified and creates the access (credentials) record.
        """
        try:
            # Validate passwords match
            if data.password != data.confirm_password:
                raise HTTPException(status_code=400, detail="Passwords do not match.")

            # Load the pending user
            user = db.query(user_profile_table).filter(
                user_profile_table.user_id == data.user_id,
                user_profile_table.user_email_verified == False
            ).first()

            if not user:
                raise HTTPException(
                    status_code=404,
                    detail="User not found or email is already verified."
                )

            # Validate OTP
            otp_record = db.query(user_otp_table).filter(
                user_otp_table.user_id == data.user_id,
                user_otp_table.is_used == False,
                user_otp_table.expires_at > datetime.utcnow()
            ).first()

            if not otp_record:
                raise HTTPException(status_code=400, detail="OTP is invalid or has expired.")

            if str(otp_record.otp) != data.otp:
                raise HTTPException(status_code=400, detail="Incorrect OTP.")

            # Mark OTP as used
            otp_record.is_used = True

            # Mark email as verified & activate user
            user.user_email_verified = True
            user.Status = "Active"

            # Create access (credentials) record only if not already existing
            existing_access = db.query(user_access_table).filter(
                user_access_table.user_id == data.user_id
            ).first()

            if not existing_access:
                access = user_access_table(
                    access_id=f"Access-{uuid.uuid4()}",
                    user_id=data.user_id,
                    provider_id=f"Email-{uuid.uuid4()}",
                    provider_name="Email",
                    role="user",
                    password_hash=hash_password(data.password)
                )
                db.add(access)
            else:
                existing_access.password_hash = hash_password(data.password)

            db.commit()

            return {
                "success": True,
                "message": "Email verified and account created successfully. You can now log in."
            }

        except HTTPException:
            raise
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Verification failed: {str(e)}")
