import re
import uuid


def validate_user_id(value: str):
    if not re.match(r"^USER-[0-9a-fA-F\-]{36}$", value):
        raise ValueError("Invalid user_id format")

    try:
        uuid.UUID(value.replace("USER-", ""))
    except ValueError:
        raise ValueError("Invalid UUID in user_id")

    return value


def validate_password(value: str):

    if len(value) < 8:
        raise ValueError("Password must be at least 8 characters long")

    pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&]).{8,}$'

    if not re.match(pattern, value):
        raise ValueError(
            "Password must contain uppercase, lowercase, number, and special character"
        )

    return value


def validate_otp(value: str):

    if not re.match(r"^\d{6}$", value):
        raise ValueError("OTP must be a 6 digit number")

    return value