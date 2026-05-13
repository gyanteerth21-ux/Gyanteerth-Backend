from os import path

from fastapi import FastAPI,HTTPException,Request,APIRouter,Depends,Path
from fastapi.responses import JSONResponse
from schemas.Auth.signup import passwordrequest,SignupEmailRequest,OTPVerificationRequest,loginrequest,refresh_token_request,update_password_request
from schemas.Auth.signup import SignupResponse,verify_otpResponse,uncomplete_passResponse,set_passwordResponse,refresh_token_response,loginresponse,forget_pass_response,update_pass_response
from schemas.Auth.signup import StudentRegisterRequest, StudentRegisterResponse, StudentVerifyAndSetPasswordRequest, StudentVerifyResponse
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


# ── Student Self-Registration ──────────────────────────────────────────────────

@router_auth.post(
    "/register",
    response_model=StudentRegisterResponse,
    summary="Student Registration – Step 1",
    description=(
        "Register a new student account. "
        "Provide your name and email. A 6-digit OTP will be sent to the email for verification. "
        "The OTP expires in 5 minutes. Use the returned `user_id` in the verify step."
    )
)
async def register_student(
    data: StudentRegisterRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    return await AuthService().register_student_service(data, background_tasks, db)


@router_auth.post(
    "/verify_registration",
    response_model=StudentVerifyResponse,
    summary="Student Registration – Step 2 (Verify Email & Set Password)",
    description=(
        "Complete registration by verifying the OTP sent to your email and setting your password. "
        "Password must be at least 8 characters and contain uppercase, lowercase, a digit, and a special character. "
        "Both `password` and `confirm_password` must match."
    )
)
async def verify_registration(
    data: StudentVerifyAndSetPasswordRequest,
    db: Session = Depends(get_db)
):
    return await AuthService().verify_email_and_set_password_service(data, db)
