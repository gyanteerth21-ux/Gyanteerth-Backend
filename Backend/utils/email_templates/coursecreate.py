def course_created_template(course, trainer_name: str):
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

<!-- HEADER -->
<tr>
<td style="background:linear-gradient(90deg,#1db954,#00a86b);padding:30px;text-align:center;">
<img src="https://api.gyanteerthlearning.online/static/logo.png?v=2"
style="width:180px;margin-bottom:10px;" alt="Gyanteerth"/>
</td>
</tr>

<!-- TITLE -->
<tr>
<td align="center" style="padding:35px 40px 10px 40px;">
<h2 style="margin:0;color:#222;font-size:22px;">Course Created Successfully 🎉</h2>

<p style="color:#666;font-size:15px;margin-top:12px;line-height:1.6;">
Hi <b>{trainer_name}</b>, <br><br>

We would like to inform you that a new course has been created and assigned to you.
</p>
</td>
</tr>

<!-- COURSE DETAILS -->
<tr>
<td align="center" style="padding:20px 40px;">
<div style="
background:#f8f9fb;
border:1px solid #e6e6e6;
padding:22px;
border-radius:10px;
text-align:left;
font-size:14px;
color:#333;
">

<p style="margin:0 0 10px 0;"><b>Course Details</b></p>

<p style="margin:6px 0;"><strong>Course ID:</strong> {course.course_id}</p>
<p style="margin:6px 0;"><strong>Title:</strong> {course.course_title}</p>
<p style="margin:6px 0;"><strong>Type:</strong> {course.course_Type}</p>
<p style="margin:6px 0;"><strong>Duration:</strong> {course.duration}</p>
<p style="margin:6px 0;"><strong>Level:</strong> {course.level}</p>
<p style="margin:6px 0;"><strong>Language:</strong> {course.language}</p>

</div>
</td>
</tr>

<!-- STATUS -->
<tr>
<td align="center" style="padding:20px 40px;">
<div style="
background:#fff7e6;
border:1px solid #ffe0a3;
padding:14px;
border-radius:8px;
font-size:14px;
color:#7a5b00;
">
📌 <b>Current Status:</b> Draft
</div>
</td>
</tr>

<!-- MESSAGE -->
<tr>
<td align="center" style="padding:10px 40px 20px 40px;">
<p style="color:#444;font-size:14px;line-height:1.6;">
This course is currently in the <b>draft stage</b>.  
Further updates regarding scheduling and activation will be shared soon.
</p>
</td>
</tr>

<!-- BUTTON -->
<tr>
<td align="center" style="padding:25px 0;">
<a href="https://www.aruljayaraj.in/trainer-login"
style="
text-decoration:none;
color:#ffffff;
background-color:#1db954;
padding:14px 36px;
border-radius:8px;
font-size:16px;
font-weight:bold;
display:inline-block;
letter-spacing:0.5px;
">
Go to Dashboard
</a>
</td>
</tr>

<!-- FOOTER -->
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
Empowering Knowledge. Inspiring Growth.
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