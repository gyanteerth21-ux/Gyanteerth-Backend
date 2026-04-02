from os import path

from fastapi import FastAPI,HTTPException,Request,APIRouter,Depends,Path
from fastapi.responses import JSONResponse
from schemas.Auth.signup import passwordrequest,SignupEmailRequest,OTPVerificationRequest,loginrequest,refresh_token_request,update_password_request
from schemas.Auth.signup import SignupResponse,verify_otpResponse,uncomplete_passResponse,set_passwordResponse,refresh_token_response,loginresponse,forget_pass_response,update_pass_response
from services.AuthService import AuthService, user_Authorization,admin_Authorization,trainer_Authorization 
from Database.DB import get_db
from sqlalchemy.orm import Session
from fastapi import Request
from fastapi import BackgroundTasks
from sqlalchemy.orm import Session
from typing import Annotated

router_auth = APIRouter()

@router_auth.get("/security_check/")
async def read(token: object = Depends(user_Authorization())):
    return token

@router_auth.get("/security_check_admin/")
async def read(token: object = Depends(admin_Authorization())):
    return token

@router_auth.get("/security_check_trainer/")
async def read(token: object = Depends(trainer_Authorization())):
    return token

@router_auth.post("/signup_credentials",response_model=SignupResponse,summary="Check email and send OTP",
    description="Checks whether the email exists and sends an OTP for verification.")
async def signup_credentials(data: SignupEmailRequest, db: Session = Depends(get_db)):
    return await AuthService().check_email(data, db)

@router_auth.post("/verify_otp",response_model=verify_otpResponse,summary="Verify OTP",
    description="Verifies the OTP for the given user.")
async def verify_otp(data: OTPVerificationRequest, db: Session = Depends(get_db)):
    return await AuthService().verify_otp_service(data, db)

@router_auth.delete("/delete_user_profile_after_verified_add_complete_pass",response_model=uncomplete_passResponse,summary="Delete User Profile After Verified not add complete pass",
    description="Deletes the user profile after successful OTP verification without setting the password.")
async def delete_user_profile_after_verified_add_complete_pass(user_id: Annotated[str,Path(example="user-abcd-efgh")], db: Session = Depends(get_db)):
    return await AuthService().delete_user_profile_service(user_id, db)

@router_auth.post("/set_password",response_model=set_passwordResponse,summary="Set Password",
    description="Sets the password for the user after successful OTP verification.")
async def set_password(data: passwordrequest, request: Request, db: Session = Depends(get_db)):
    return await AuthService().set_password_service(data, request, db)

@router_auth.post("/new_access_token",response_model = refresh_token_response,summary="Generate New Access Token",
    description="Generates a new access token using the refresh token.")
async def new_access_token(data:refresh_token_request, db: Session = Depends(get_db)):
    return await AuthService().refresh_token_check_service(data, db)

@router_auth.post("/login",response_model=loginresponse,summary="Login",
    description="password must be 8 characters long, contain at least one uppercase letter, one lowercase letter, one digit, and one special character.")
async def login(data: loginrequest,request:Request, db: Session = Depends(get_db)):
    return await AuthService().login_service(data,request, db)

@router_auth.post("/forget_password",response_model=forget_pass_response,summary="Forget Password",
    description="Sends a password reset link to the user's email.")
async def forget_password(data: SignupEmailRequest, db: Session = Depends(get_db)):
    return await AuthService().forget_password_token_email(data, db)

@router_auth.put("/update_password",response_model=update_pass_response,summary="Update Password",
    description="Updates the user's password.")
async def update_password(data: update_password_request, db: Session = Depends(get_db)):
    return await AuthService().update_password_service(data, db)

@router_auth.post("/google-signup",summary="Google Signup",
    description="Signs up a new user via Google.")
async def google_signup(data: dict,db:Session = Depends(get_db)):
    return await AuthService().google_signup_service(data, db)