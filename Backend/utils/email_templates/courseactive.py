def course_active_template(course_id,course_title,content_type,course_duration,course_level,course_language, course_structure):
    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Course Activated</title>
</head>

<body style="margin:0; padding:0; background-color:#f4f6f8; font-family:Arial, sans-serif;">

  <table width="100%" cellpadding="0" cellspacing="0" style="padding:20px; background-color:#f4f6f8;">
    <tr>
      <td align="center">

        <table width="600" cellpadding="0" cellspacing="0" style="background:#ffffff; border-radius:8px; overflow:hidden;">

          <!-- Header -->
          <tr>
            <td style="background:#4CAF50; color:#ffffff; padding:18px; text-align:center; font-size:22px; font-weight:bold;">
              🎉 Course Activated – Now Live
            </td>
          </tr>

          <!-- Body -->
          <tr>
            <td style="padding:25px; color:#333333; font-size:14px; line-height:1.6;">

              <p>Hi Trainer,</p>

              <p>
                We are pleased to inform you that your course has been successfully 
                <strong style="color:#4CAF50;">activated</strong> and is now live on the platform.
              </p>

              <!-- Course Details Box -->
              <table width="100%" cellpadding="10" cellspacing="0" style="margin:20px 0; border-collapse:collapse; border:1px solid #e0e0e0;">
                
                <tr style="background:#f1f1f1;">
                  <td colspan="2" style="font-weight:bold; text-align:center;">
                    Course Details
                  </td>
                </tr>

                <tr>
                  <td style="border:1px solid #e0e0e0;"><strong>Course ID</strong></td>
                  <td style="border:1px solid #e0e0e0;">{course_id}</td>
                </tr>

                <tr>
                  <td style="border:1px solid #e0e0e0;"><strong>Title</strong></td>
                  <td style="border:1px solid #e0e0e0;">{course_title}</td>
                </tr>

                <tr>
                  <td style="border:1px solid #e0e0e0;"><strong>Type</strong></td>
                  <td style="border:1px solid #e0e0e0;">{content_type}</td>
                </tr>

                <tr>
                  <td style="border:1px solid #e0e0e0;"><strong>Duration</strong></td>
                  <td style="border:1px solid #e0e0e0;">{course_duration}</td>
                </tr>

                <tr>
                  <td style="border:1px solid #e0e0e0;"><strong>Level</strong></td>
                  <td style="border:1px solid #e0e0e0;">{course_level}</td>
                </tr>

                <tr>
                  <td style="border:1px solid #e0e0e0;"><strong>Language</strong></td>
                  <td style="border:1px solid #e0e0e0;">{course_language}</td>
                </tr>

                <tr>
                  <td style="border:1px solid #e0e0e0;"><strong>Status</strong></td>
                  <td style="border:1px solid #e0e0e0; color:green; font-weight:bold;">
                    Active
                  </td>
                </tr>

              </table>
              <br/>

              <!-- Course Structure Box -->
              <h3 style="color:#4CAF50; font-size:16px;">Course Structure</h3>
              <table width="100%" cellpadding="10" cellspacing="0" style="margin-bottom:20px; border-collapse:collapse; border:1px solid #e0e0e0;">
                <tr style="background:#f1f1f1;">
                  <th style="border:1px solid #e0e0e0; text-align:left;">Module</th>
                  <th style="border:1px solid #e0e0e0; text-align:center;">Content Summary</th>
                </tr>
                {"".join([
                    f'''<tr>
                          <td style="border:1px solid #e0e0e0; font-weight:bold;">{mod.get("title", "")}</td>
                          <td style="border:1px solid #e0e0e0; text-align:center; font-size:13px; color:#555;">
                            Videos: {len(mod.get("content", {}).get("videos", []))} <br/>
                            Live Sessions: {len(mod.get("content", {}).get("live_sessions", []))} <br/>
                            Assessments: {len(mod.get("content", {}).get("assessments", []))}
                          </td>
                        </tr>'''
                    for mod in course_structure.get("modules", [])
                ]) if course_structure and course_structure.get("modules") else '<tr><td colspan="2" style="border:1px solid #e0e0e0; text-align:center;">No structure available</td></tr>'}
              </table>

              <p>
                Your course is now available to learners. You can monitor enrollments,
                track learner progress, and manage course content from your dashboard.
              </p>

              <p>
                If you need any updates or assistance, feel free to reach out to us anytime.
              </p>

              <!-- CTA Button -->
              <div style="text-align:center; margin:30px 0;">
                <a href="#" style="
                  background:#4CAF50;
                  color:#ffffff;
                  padding:12px 20px;
                  text-decoration:none;
                  border-radius:5px;
                  font-weight:bold;
                  display:inline-block;
                ">
                  View Course
                </a>
              </div>

              <p>
                Best regards,<br>
                <strong>Admin Team</strong>
              </p>

            </td>
          </tr>

          <!-- Footer -->
          <tr>
            <td style="background:#f1f1f1; text-align:center; padding:12px; font-size:12px; color:#777;">
              © 2026 Your Platform. All rights reserved.
            </td>
          </tr>

        </table>

      </td>
    </tr>
  </table>

</body>
</html>
"""