def welcome_email_template(name, email, password, role):
    role_display = "Trainer" if role.lower() == "trainer" else "Student"
    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Welcome to Gyanteerth</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #f4f4f4;
                margin: 0;
                padding: 0;
            }}
            .email-container {{
                max-width: 600px;
                margin: 0 auto;
                background-color: #ffffff;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            }}
            .header {{
                background: linear-gradient(90deg,#1db954,#00a86b) !important;
                background-color: #4CAF50;
                color: #ffffff;
                text-align: center;
                padding: 10px;
                border-radius: 8px 8px 0 0;
            }}
            .header h1 {{
                margin: 0;
                font-size: 24px;
            }}
            .content {{
                padding: 20px;
                color: #333333;
                line-height: 1.6;
            }}
            .content p {{
                margin: 10px 0;
            }}
            .credentials {{
                background-color: #f9f9f9;
                border-left: 4px solid #4CAF50;
                padding: 15px;
                margin: 20px 0;
                font-family: monospace;
                font-size: 16px;
            }}
            .button-container {{
                text-align: center;
                margin: 30px 0;
            }}
            .login-button {{
                background: linear-gradient(90deg,#1db954,#00a86b) !important;
                color: #ffffff !important;
                padding: 12px 30px;
                text-decoration: none;
                border-radius: 8px;
                font-weight: bold;
                display: inline-block;
                box-shadow: 0 4px 15px rgba(29, 185, 84, 0.25);
            }}
            .footer {{
                text-align: center;
                padding: 10px;
                font-size: 12px;
                color: #888888;
                border-top: 1px solid #eeeeee;
                margin-top: 20px;
            }}
        </style>
    </head>
    <body>
        <div class="email-container">
            <div class="header">
                <img src="https://api.gyanteerthlearning.online/static/logo.png?v=2" style="width:180px;" alt="Gyanteerth"/>
            </div>
            <div class="content">
                <p>Hello <strong>{name}</strong>,</p>
                <p>Your {role_display} account has been created successfully at Gyanteerth.</p>
                <p>Below are your login credentials. We recommend that you change your password after logging in for the first time.</p>
                <div class="credentials">
                    <strong>Email:</strong> {email} <br>
                    <strong>Password:</strong> {password}
                </div>
                <div class="button-container">
                    <a href="https://gyanteerthlearning.online/login" class="login-button">Login to Platform</a>
                </div>
                <p>If you have any questions or need assistance, please feel free to reach out to our support team.</p>
            </div>
            <div class="footer">
                <p>&copy; 2026 Gyanteerth. All rights reserved.</p>
            </div>
        </div>
    </body>
    </html>
    """
