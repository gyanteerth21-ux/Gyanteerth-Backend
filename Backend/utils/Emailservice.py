import asyncio
import logging
import os
import socket
import time
from email.message import EmailMessage
import aiosmtplib
from dotenv import load_dotenv, find_dotenv

logger = logging.getLogger("email_service")

# Module level state for rate limiting and validation
_email_send_lock = None
_last_send_time = 0.0
_config_validated = False

def validate_email_config(force: bool = False):
    global _config_validated
    if _config_validated and not force:
        return
    required_vars = ["SMTP_HOST", "SMTP_PORT", "SMTP_USERNAME", "SMTP_PASSWORD", "EMAIL_FROM"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    if missing_vars:
        err_msg = f"Email configuration validation failed: missing variables: {', '.join(missing_vars)}"
        logger.error(err_msg)
        raise ValueError(err_msg)
    _config_validated = True

# Load environment variables with fallback to local Backend/.env
dotenv_path = find_dotenv()
if not dotenv_path:
    fallback_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env")
    if os.path.exists(fallback_path):
        dotenv_path = fallback_path
load_dotenv(dotenv_path)

# Run validation on import (warning only, to avoid breaking startup if not configured yet)
try:
    validate_email_config()
except ValueError as e:
    logger.warning(f"Email service imported but not fully configured: {e}")

async def send_email(to_email: str, subject: str, body: str):
    global _last_send_time, _email_send_lock
    
    # Always enforce configuration validation before sending
    validate_email_config()
    
    # Initialize the lock inside the running event loop
    if _email_send_lock is None:
        _email_send_lock = asyncio.Lock()
        
    max_attempts = 3
    initial_delay = 2.0
    backoff_factor = 2.0

    for attempt in range(1, max_attempts + 1):
        # We acquire the lock for the rate-limiting and sending phase of this attempt
        async with _email_send_lock:
            # Enforce rate limiting of 1 email per 1.1 seconds
            now = time.time()
            elapsed = now - _last_send_time
            rate_limit_delay = 1.1
            if elapsed < rate_limit_delay:
                wait_time = rate_limit_delay - elapsed
                logger.info(f"Rate limiting: sleeping for {wait_time:.2f} seconds before sending to {to_email}")
                await asyncio.sleep(wait_time)
                
            logger.info(f"Attempting to send transactional email to {to_email} (attempt {attempt}/{max_attempts})")
            
            message = EmailMessage()
            email_from = os.getenv("EMAIL_FROM")
            
            message["From"] = email_from
            message["To"] = to_email
            message["Subject"] = subject

            message.set_content("Your email client does not support HTML.")
            message.add_alternative(body, subtype="html")

            smtp_host = os.getenv("SMTP_HOST")
            smtp_port = int(os.getenv("SMTP_PORT", "587"))
            smtp_username = os.getenv("SMTP_USERNAME")
            smtp_password = os.getenv("SMTP_PASSWORD")

            try:
                await aiosmtplib.send(
                    message,
                    hostname=smtp_host,
                    port=smtp_port,
                    start_tls=True,
                    username=smtp_username,
                    password=smtp_password
                )
                logger.info(f"Email successfully sent to {to_email}")
                _last_send_time = time.time()
                return
            except aiosmtplib.SMTPResponseException as e:
                _last_send_time = time.time()  # Update send time anyway to protect rate limit window
                # 5xx error codes are permanent failures
                if 500 <= e.code < 600:
                    logger.error(
                        f"Failed to send email to {to_email}: SMTPResponseException status_code={e.code}, message={e.message} (Permanent error, not retrying)"
                    )
                    raise
                else:
                    # 4xx or other temporary errors
                    if attempt == max_attempts:
                        logger.exception(
                            f"Failed to send email to {to_email}: SMTPResponseException status_code={e.code}, message={e.message} (Max attempts reached)"
                        )
                        raise
                    delay = initial_delay * (backoff_factor ** (attempt - 1))
                    logger.warning(
                        f"Temporary SMTP error {e.code} for {to_email}: {e.message}. Retrying in {delay}s..."
                    )
            except (aiosmtplib.SMTPException, OSError, asyncio.TimeoutError, socket.error) as e:
                _last_send_time = time.time()  # Update send time anyway to protect rate limit window
                if attempt == max_attempts:
                    logger.exception(
                        f"Failed to send email to {to_email}: {type(e).__name__}: {str(e)} (Max attempts reached)"
                    )
                    raise
                delay = initial_delay * (backoff_factor ** (attempt - 1))
                logger.warning(
                    f"Temporary network/SMTP error {type(e).__name__} for {to_email}: {str(e)}. Retrying in {delay}s..."
                )
        
        # We are now OUTSIDE the async with _email_send_lock block.
        # This allows other emails to acquire the lock and try to send while this email sleeps.
        await asyncio.sleep(delay)
