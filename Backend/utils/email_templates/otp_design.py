def otp_email_template(otp: str):
    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
</head>

<body style="margin:0;padding:0;background:#f4f6f8;font-family:Arial,Helvetica,sans-serif;">

<table width="100%" cellpadding="0" cellspacing="0" style="padding:40px 0;">
<tr>
<td align="center">

<table width="520" cellpadding="0" cellspacing="0"
style="background:#ffffff;border-radius:14px;overflow:hidden;border:1px solid #e6e6e6;box-shadow:0 6px 20px rgba(0,0,0,0.06);">

<tr>
<td style="background:linear-gradient(90deg,#1db954,#00a86b);padding:30px;text-align:center;">
<img src="https://res.cloudinary.com/dosahgtni/image/upload/v1773465717/Gyanteerth-removebg-preview_t5ap3i.png"
style="width:180px;margin-bottom:10px;" alt="Gyanteerth"/>
</td>
</tr>

<tr>
<td align="center" style="padding:35px 40px 10px 40px;">
<h2 style="margin:0;color:#222;font-size:24px;">Verify your email</h2>

<p style="color:#666;font-size:15px;margin-top:12px;line-height:1.6;">
Welcome to <b>Gyanteerth</b>.  
Enter the verification code below to activate your account.
</p>
</td>
</tr>

<tr>
<td align="center" style="padding:30px 0;">
<div style="
background:#f8f9fb;
border:2px dashed #1db954;
padding:24px 40px;
border-radius:12px;
font-size:38px;
font-weight:bold;
letter-spacing:10px;
color:#222;
display:inline-block;
box-shadow:0 3px 8px rgba(0,0,0,0.05);
">

{otp}

</div>
</td>
</tr>

<tr>
<td align="center">
<p style="color:#444;font-size:14px;">
⏱ This code will expire in 
<b style="color:#1db954;">5 minutes</b>.
</p>
</td>
</tr>

<tr>
<td align="center" style="padding:20px 40px;">
<div style="
background:#fff7e6;
border:1px solid #ffe0a3;
padding:14px;
border-radius:8px;
font-size:13px;
color:#7a5b00;
">
🔒 For security reasons, never share this code with anyone.
</div>
</td>
</tr>

<tr>
<td align="center" style="padding:20px 40px;">
<hr style="border:none;border-top:1px solid #eee;">
</td>
</tr>

<tr>
<td align="center" style="padding:0 40px 30px 40px;">
<p style="font-size:13px;color:#777;margin-bottom:6px;">
Gyanteerth Learning Platform
</p>

<p style="font-size:12px;color:#aaa;margin:0;">
Committed towards excellence
</p>

<p style="font-size:11px;color:#bbb;margin-top:12px;">
© 2026 Gyanteerth. All rights reserved.
</p>
</td>
</tr>

</table>

</td>
</tr>
</table>

</body>
</html>
"""

def forget_password_email_template(token: str):
    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
</head>

<body style="margin:0;padding:0;background:#f4f6f8;font-family:Arial,Helvetica,sans-serif;">

<table width="100%" cellpadding="0" cellspacing="0" style="padding:40px 0;">
<tr>
<td align="center">

<table width="520" cellpadding="0" cellspacing="0"
style="background:#ffffff;border-radius:14px;overflow:hidden;border:1px solid #e6e6e6;box-shadow:0 6px 20px rgba(0,0,0,0.06);">

<tr>
<td style="background:linear-gradient(90deg,#1db954,#00a86b);padding:30px;text-align:center;">
<img src="https://res.cloudinary.com/dosahgtni/image/upload/v1773465717/Gyanteerth-removebg-preview_t5ap3i.png"
style="width:180px;margin-bottom:10px;" alt="Gyanteerth"/>
</td>
</tr>

<tr>
<td align="center" style="padding:35px 40px 10px 40px;">
<h2 style="margin:0;color:#222;font-size:24px;">Reset  your password</h2>

<p style="color:#666;font-size:15px;margin-top:12px;line-height:1.6;">
Welcome to <b>Gyanteerth</b>.  
Click the link below to update  your account password.
</p>
</td>
</tr>

<tr>
<td align="center" style="padding:30px 0;">
<button><a href="https://www.aruljayaraj.in/reset-password?token={token}" 
style="
text-decoration:none;
color:#ffffff;
background-color:#1db954;
padding:14px 34px;
border-radius:8px;
font-size:16px;
font-weight:bold;
font-family:Arial, Helvetica, sans-serif;
display:inline-block;
letter-spacing:0.5px;
">
Reset Password
</a></button>
</td>
</tr>

<tr>
<td align="center">
<p style="color:#444;font-size:14px;">
⏱ This link will expire in 
<b style="color:#1db954;">5 minutes</b>.
</p>
</td>
</tr>

<tr>
<td align="center" style="padding:20px 40px;">
</td>
</tr>

<tr>
<td align="center" style="padding:20px 40px;">
<hr style="border:none;border-top:1px solid #eee;">
</td>
</tr>

<tr>
<td align="center" style="padding:0 40px 30px 40px;">
<p style="font-size:13px;color:#777;margin-bottom:6px;">
Gyanteerth Learning Platform
</p>

<p style="font-size:12px;color:#aaa;margin:0;">
Committed towards excellence
</p>

<p style="font-size:11px;color:#bbb;margin-top:12px;">
© 2026 Gyanteerth. All rights reserved.
</p>
</td>
</tr>

</table>

</td>
</tr>
</table>

</body>
</html>
"""