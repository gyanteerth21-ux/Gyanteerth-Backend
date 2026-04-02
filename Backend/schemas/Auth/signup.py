from pydantic import BaseModel, EmailStr, field_validator
from utils.validator import validate_user_id, validate_password, validate_otp


class passwordrequest(BaseModel):
    user_id: str
    password: str
    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "USER-1234-abcd",
                "password": "P@ssw0rd"
            }
        }

    _validate_user_id = field_validator("user_id")(validate_user_id)
    _validate_password = field_validator("password")(validate_password)

class refresh_token_request(BaseModel):
    refresh_token: str
    class Config:
        json_schema_extra = {
            "example": {
                "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9....."
            }
        }

class refresh_token_response(BaseModel):
    access_token: str
    class Config:
        json_schema_extra = {
            "example":{
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9....."
            }
        }
    

class update_password_request(BaseModel):
    new_password: str
    token:str

    _validate_password = field_validator("new_password")(validate_password)


class loginrequest(BaseModel):
    Email: EmailStr
    password: str
    class config:
        json_schema_extra = {
            "example": {
                "Email": "user@gmail.com",
                "password": "User@1234"
            }
        }
    _validate_password = field_validator("password")(validate_password)

class SignupEmailRequest(BaseModel):
    email: EmailStr
    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@gmail.com"
            }
        }

class OTPVerificationRequest(BaseModel):
    user_id: str
    otp: str
    class Config:
        json_schema_extra = {
            "example":{
              "user_id": "USER-1234-abcd",
              "otp": "123456"
            }
        }

    _validate_user_id = field_validator("user_id")(validate_user_id)
    _validate_otp = field_validator("otp")(validate_otp)


class SignupResponse(BaseModel):
    exists: bool
    message: str
    user_id: str | None = None

    class Config:
        json_schema_extra = {
            "example": {
                "exists": False,
                "message": "OTP sent to your email",
                "user_id": "USER-1234-abcd"
            }
        }

class verify_otpResponse(BaseModel):
    success: bool
    message: str

    class Config:
        json_schema_extra = {
            "example":{
              "success": True,
              "message": "Email verified successfully"
            }
        }

class uncomplete_passResponse(BaseModel):
    success: bool
    message: str

    class Config:
        json_schema_extra = {
            "example":{
              "success": True,
              "message": "User profile deleted successfully"
            }
        }

class set_passwordResponse(BaseModel):
    success: bool
    message: str

    class Config:
        json_schema_extra = {
            "example":{
              "success": True,
              "message": "Password set successfully"
            }
        }

class loginresponse(BaseModel):
    success:bool
    message:str
    role:str
    access_token:str
    refresh_token:str

    class Config:
        json_schema_extra = {
            "example":{
                "success":True,
                "message":"Login successful",
                "role": "user",
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.....",
                "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9....."
            }
        }
    
class forget_pass_response(BaseModel):
    success:bool
    message:str
    class Config:
        json_schema_extra = {
            "example":{
                "success":True,
                "message": "Password reset token sent to your email"
            }
        }

class update_pass_response(BaseModel):
    success:bool
    message:str
    class Config:
        json_schema_extra = {
            "example":{
            "success": True,
            "message": "Password updated successfully"
        }
        }