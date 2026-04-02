import aiosmtplib
from email.message import EmailMessage

async def send_email(to_email: str, subject: str, body: str):
    message = EmailMessage()
    message["From"] = "aruljayarajj826@gmail.com"
    message["To"] = to_email
    message["Subject"] = subject

    message.set_content("Your email client does not support HTML.")

    message.add_alternative(body, subtype="html")

    await aiosmtplib.send(
        message,
        hostname="smtp.gmail.com",
        port=587,
        start_tls=True,
        username="aruljayarajj826@gmail.com",
        password="ysbqpkpkfmkypfub" 
    )
