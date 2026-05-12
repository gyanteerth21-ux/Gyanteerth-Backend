import aiosmtplib
import os
from email.message import EmailMessage
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

async def send_email(to_email: str, subject: str, body: str):
    message = EmailMessage()
    sender_email = os.getenv("EMAIL_USER")
    sender_password = os.getenv("EMAIL_PASSWORD")
    
    message["From"] = sender_email
    message["To"] = to_email
    message["Subject"] = subject

    message.set_content("Your email client does not support HTML.")
    message.add_alternative(body, subtype="html")

    await aiosmtplib.send(
        message,
        hostname="smtp.gmail.com",
        port=587,
        start_tls=True,
        username=sender_email,
        password=sender_password
    )
