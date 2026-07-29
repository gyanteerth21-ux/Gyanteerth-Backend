from sqlalchemy.orm import Session
from sqlalchemy import and_

from Models.User_Tables.User_Profile import user_profile_table
from Models.User_Tables.User_Access import user_access_table
from Models.Progress.EnrollmentTable import EnrollmentTable
from Models.Progress.CourseProgressTable import CourseProgressTable
from Models.Course_Tables.course_details import CourseTable

def get_all_students_progress(db: Session, college_filter: str = None):
    """
    Fetches all users and their enrollments along with progress.
    Used by Admin service and TPO service.
    """
    query = db.query(user_profile_table).join(
        user_access_table,
        user_access_table.user_id == user_profile_table.user_id
    ).filter(user_access_table.role == "user")
    
    if college_filter:
        query = query.filter(user_profile_table.user_college == college_filter)
        
    users = query.all()

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
    
    return sorted(list(user_dict.values()), key=lambda x: x["avgProgress"], reverse=True)


def get_course_students_progress_data(db: Session, course_id: str):
    """
    Fetches all students enrolled in a specific course and their progress.
    Used by Trainer service.
    """
    students = db.query(
        user_profile_table.user_id,
        user_profile_table.user_name,
        user_profile_table.user_email,
        user_profile_table.user_college,
        user_profile_table.user_branch,
        user_profile_table.user_year,
        CourseProgressTable.Progress_Percentage,
        CourseProgressTable.Completed_Module,
        CourseProgressTable.Total_Modules
    ).join(
        EnrollmentTable,
        EnrollmentTable.User_ID == user_profile_table.user_id
    ).outerjoin(
        CourseProgressTable,
        and_(
            CourseProgressTable.User_ID == user_profile_table.user_id,
            CourseProgressTable.Course_ID == course_id
        )
    ).filter(
        EnrollmentTable.Course_ID == course_id
    ).all()

    data = [
        {
            "user_id": s.user_id,
            "user_name": s.user_name,
            "email": s.user_email,
            "user_college": s.user_college,
            "user_branch": s.user_branch,
            "user_year": s.user_year,
            "progress_percentage": s.Progress_Percentage or 0,
            "completed_modules": s.Completed_Module or 0,
            "total_modules": s.Total_Modules or 0
        }
        for s in students
    ]
    return data
