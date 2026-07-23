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

        users = db.query(user_profile_table).join(
            user_access_table,
            user_access_table.user_id == user_profile_table.user_id
        ).filter(
            user_access_table.role == "user",
            user_profile_table.user_college == tpo_college
        ).all()

        user_dict = {
            u.user_id: {
                "user_id": u.user_id,
                "name": u.user_name,
                "email": u.user_email,
                "college": getattr(u, "user_college", None),
                "branch": getattr(u, "user_branch", None),
                "year": getattr(u, "user_year", None),
                "enrollments": [],
                "avgProgress": 0,
                "_total_progress": 0
            }
            for u in users
        }

        enrollments = db.query(
            EnrollmentTable.User_ID,
            EnrollmentTable.Course_ID,
            CourseTable.course_title,
            CourseProgressTable.Progress_Percentage
        ).join(
            CourseTable, CourseTable.course_id == EnrollmentTable.Course_ID
        ).outerjoin(
            CourseProgressTable,
            (CourseProgressTable.User_ID == EnrollmentTable.User_ID) & 
            (CourseProgressTable.Course_ID == EnrollmentTable.Course_ID)
        ).all()

        for e in enrollments:
            uid = e.User_ID
            if uid in user_dict:
                prog = e.Progress_Percentage or 0
                user_dict[uid]["enrollments"].append({
                    "course_id": e.Course_ID,
                    "course_title": e.course_title,
                    "progress": prog
                })
                user_dict[uid]["_total_progress"] += prog

        for u in user_dict.values():
            count = len(u["enrollments"])
            if count > 0:
                u["avgProgress"] = round(u["_total_progress"] / count)
            del u["_total_progress"]
        
        sorted_students = sorted(list(user_dict.values()), key=lambda x: x["avgProgress"], reverse=True)

        return {
            "status": True,
            "data": sorted_students
        }
