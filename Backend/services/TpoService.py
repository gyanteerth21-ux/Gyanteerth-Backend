from sqlalchemy.orm import Session
from fastapi import HTTPException
from Models.User_Tables.User_Profile import user_profile_table
from Models.User_Tables.User_Access import user_access_table
from Models.Progress.EnrollmentTable import EnrollmentTable
from Models.Progress.CourseProgressTable import CourseProgressTable
from Models.Course_Tables.course_details import CourseTable

class TpoService:
    async def get_tpo_students(self, tpo_id: str, db: Session):
        tpo = db.query(user_profile_table).filter(user_profile_table.user_id == tpo_id).first()
        if not tpo or not tpo.user_college:
            raise HTTPException(status_code=400, detail="TPO profile or college not found")
        
        tpo_college = tpo.user_college

        from utils.student_utils import get_all_students_progress
        sorted_students = get_all_students_progress(db, tpo_college)

        return {
            "status": True,
            "data": sorted_students
        }
