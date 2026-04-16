from Models.Course_Tables.course_details import CourseTable
from Models.Progress.EnrollmentTable import EnrollmentTable
from Models.User_Tables.User_Profile import user_profile_table
from fastapi import FastAPI, UploadFile, File, HTTPException
import cloudinary
import cloudinary.uploader
from utils.Emailservice import send_email
from Database.DB import get_db
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os
import time
import uuid


load_dotenv()
cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET")
)

class UserService:
    def delete_cloudinary(public_id):
        cloudinary.uploader.destroy(public_id)
    async def get_user_profile(self, token: dict, db: Session):
        user_id = token.get("user_id")
        user = db.query(user_profile_table).filter(
            user_profile_table.user_id == user_id
        ).first()
    
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        return {
            "user_id": user.user_id,
            "email": user.user_email,
            "user_name": user.user_name,
            "user_pic": user.user_pic,
            "user_number": user.user_number,
            "user_dob": user.user_dob,
            "user_gender": user.user_gender,
            "user_city": user.user_city,
            "user_state": user.user_state,
            "email_verified": user.user_email_verified
        }
    
    async def update_user_profile(self, Data, user_gender,background_tasks, user_pic: UploadFile | None, token: dict, db: Session):
        user_id = token.get("user_id")
        cloud_start = 0
        cloud_end = 0
        cloud_dstart = 0
        cloud_dend = 0
        user = db.query(user_profile_table).filter(
            user_profile_table.user_id == user_id
        ).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        try:
            if user_pic:
                if user.user_pic and "res.cloudinary.com" in user.user_pic:
                    file_name = user.user_pic.split("/")[-1]
                    public_id = file_name.split(".")[0]
                    cloud_dstart = time.time()
                    background_tasks.add_task(self.delete_cloudinary, public_id)
                    cloud_dend = time.time()
                cloud_start = time.time()
                upload_result = cloudinary.uploader.upload(user_pic.file)
                cloud_end = time.time()
                user.user_pic = upload_result.get("secure_url")
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Image upload failed: {str(e)}"
            )
        user.user_name = Data.user_name
        user.user_number = Data.user_number
        user.user_dob = Data.user_dob
        user.user_gender = user_gender
        user.user_city = Data.user_city
        user.user_state = Data.user_state
        user.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(user)
        return {
            "message": "User profile updated successfully",
            "user_id": user.user_id,
            "email": user.user_email,
            "user_name": user.user_name,
            "user_pic": user.user_pic,
            "user_number": str(user.user_number) if user.user_number else None,
            "user_dob": user.user_dob,
            "user_gender": user.user_gender,
            "user_city": user.user_city,
            "user_state": user.user_state,
            "cloud_upload_time": cloud_end - cloud_start,
            "cloud_delete_time":cloud_dend - cloud_dstart
        }
    
    async def enroll_course(self, course_id: str, db: Session,token: dict):

        course = db.query(CourseTable).filter(
            CourseTable.course_id == course_id,
            CourseTable.is_active == True
        ).first()

        if not course:
            raise HTTPException(status_code=404, detail="Course not found or inactive")
    
        existing = db.query(EnrollmentTable).filter(
            EnrollmentTable.User_ID == token.get('user_id'),
            EnrollmentTable.Course_ID == course_id
        ).first()
    
        if existing:
            raise HTTPException(status_code=400, detail="Already enrolled in this course")
    
        enrollment = EnrollmentTable(
            Enrollment_ID=f"ENROLL-{uuid.uuid4().hex[:8]}",
            User_ID=token.get('user_id'),
            Course_ID=course_id,
            Status="ACTIVE",
            Enrolled_AT=datetime.utcnow()
        )
    
        db.add(enrollment)
        db.commit()
        db.refresh(enrollment)
    
        return {
            "enrollment_id": enrollment.Enrollment_ID,
            "message": "Successfully enrolled"
        }
    
    async def enrolled_course(self,db:Session,token:dict):
        try:
            user_id = token.get("user_id")
            enrollments = db.query(EnrollmentTable).filter(
                EnrollmentTable.User_ID == user_id,
            ).all()
    
            course_ids = [enrollment.Course_ID for enrollment in enrollments]
    
            courses = db.query(CourseTable).filter(
                CourseTable.course_id.in_(course_ids)
            ).all()
    
            return [
                {
                    "course_id": course.course_id,
                    "course_name": course.course_title,
                    "course_description": course.course_description,
                    "course_pic": course.thumbnail
                }
                for course in courses
            ]
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    async def mark_live_attendance(self, live_class_id: str, module_id: str, attended_live: bool, watched_recording: bool, token: dict, db: Session):
        from Models.Progress.LiveAttendanceTable import LiveAttendanceTable
        user_id = token.get("user_id")

        if not attended_live and not watched_recording:
            raise HTTPException(status_code=400, detail="Must mark either live attendance or recording view as true")

        attendance = db.query(LiveAttendanceTable).filter(
            LiveAttendanceTable.User_ID == user_id,
            LiveAttendanceTable.Live_Class_ID == live_class_id
        ).first()

        if attendance:
            # Update existing attendance
            if attended_live:
                attendance.Attended_Live = True
            if watched_recording:
                attendance.Watched_Recording = True
            attendance.Is_Present = True
            attendance.updated_at = datetime.utcnow()
            message = "Attendance updated successfully"
        else:
            # Create new attendance record
            attendance = LiveAttendanceTable(
                Live_Attendance_ID=f"LIVE-ATT-{uuid.uuid4().hex[:8]}",
                User_ID=user_id,
                Live_Class_ID=live_class_id,
                Module_ID=module_id,
                Attended_Live=attended_live,
                Watched_Recording=watched_recording,
                Is_Present=True,
                Completed_At=datetime.utcnow()
            )
            db.add(attendance)
            message = "Attendance marked successfully"

        db.commit()

        from services.ProgressService import ProgressService
        ProgressService()._calculate_module_progress(user_id, None, module_id, db)

        return {
            "message": message,
            "is_present": attendance.Is_Present
        }

    async def submit_course_feedback(self, user_id: str, course_id: str, feedback_data, db: Session):
        # 1. Check if course is completed
        from Models.Progress.CourseProgressTable import CourseProgressTable
        from Models.Feedback_col.Feedback import FeedbackTable
        import uuid

        progress = db.query(CourseProgressTable).filter(
            CourseProgressTable.User_ID == user_id,
            CourseProgressTable.Course_ID == course_id
        ).first()

        if not progress or progress.Progress_Percentage < 100:
             raise HTTPException(status_code=400, detail="You must complete 100% of the course before providing feedback.")

        # 2. Check if feedback already exists
        existing = db.query(FeedbackTable).filter(
            FeedbackTable.User_ID == user_id,
            FeedbackTable.Course_ID == course_id
        ).first()

        if existing:
            raise HTTPException(status_code=400, detail="You have already provided feedback for this course.")

        # 3. Save feedback
        new_feedback = FeedbackTable(
            Feedback_ID = f"FEEDBACK-{uuid.uuid4().hex[:8]}",
            User_ID = user_id,
            Course_ID = course_id,
            Course_rating = feedback_data.Course_rating,
            Instructor_rating = feedback_data.Instructor_rating,
            Review = feedback_data.Review,
            Disply_Status = "Pending"
        )
        
        db.add(new_feedback)
        db.commit()

        return {
            "status": True,
            "message": "Feedback submitted successfully. It will be visible once approved by Admin.",
            "feedback_id": new_feedback.Feedback_ID
        }

    async def get_public_feedbacks(self, db: Session):
        from Models.Feedback_col.Feedback import FeedbackTable
        from Models.User_Tables.User_Profile import user_profile_table
        from Models.Course_Tables.course_details import CourseTable

        feedbacks = db.query(
            user_profile_table.user_name,
            user_profile_table.user_pic,
            CourseTable.course_title,
            FeedbackTable.Course_rating,
            FeedbackTable.Review,
            FeedbackTable.created_at
        ).join(
            user_profile_table, user_profile_table.user_id == FeedbackTable.User_ID
        ).join(
            CourseTable, CourseTable.course_id == FeedbackTable.Course_ID
        ).filter(
            FeedbackTable.Disply_Status == "Approved"
        ).order_by(FeedbackTable.created_at.desc()).all()

        data = [
            {
                "user_name": f.user_name,
                "user_pic": f.user_pic,
                "course_title": f.course_title,
                "course_rating": f.Course_rating,
                "review": f.Review,
                "created_at": f.created_at
            }
            for f in feedbacks
        ]

        return {
            "status": True,
            "data": data
        }

    async def get_certificate_details(self, user_id: str, course_id: str, db: Session):
        from Models.Progress.CourseProgressTable import CourseProgressTable
        from Models.Certificate_Table.Certificate_table import CertificateTable
        import random

        # 1. Check if course progress is 100%
        progress = db.query(CourseProgressTable).filter(
            CourseProgressTable.User_ID == user_id,
            CourseProgressTable.Course_ID == course_id
        ).first()

        if not progress or progress.Progress_Percentage < 100:
            raise HTTPException(status_code=400, detail="You must complete 100% of the course to get the certificate.")

        # 2. Fetch User and Course details
        user = db.query(user_profile_table).filter(user_profile_table.user_id == user_id).first()
        course = db.query(CourseTable).filter(CourseTable.course_id == course_id).first()

        if not user or not course:
            raise HTTPException(status_code=404, detail="User or Course not found.")

        # 3. Check for existing certificate
        certificate = db.query(CertificateTable).filter(
            CertificateTable.User_ID == user_id,
            CertificateTable.Course_ID == course_id
        ).first()

        if not certificate:
            certificate = CertificateTable(
                Certificate_ID=str(uuid.uuid4()),
                User_ID=user_id,
                Course_ID=course_id,
                certificate_number=random.randint(100000, 999999), 
                Verification_code=random.randint(1000, 9999),
                Certificate_url="",
                Issued_at=datetime.utcnow()
            )
            db.add(certificate)
            db.commit()
            db.refresh(certificate)

        return {
            "uuid": certificate.Certificate_ID,
            "course_name": course.course_title,
            "course_duration": course.duration,
            "user_name": user.user_name,
            "issued_date": certificate.Issued_at
        }
