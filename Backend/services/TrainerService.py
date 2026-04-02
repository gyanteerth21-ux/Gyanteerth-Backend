from fastapi import HTTPException
from sqlalchemy.orm import Session
from Models.Course_Tables.course_details import CourseTable
from Models.User_Tables.User_Access import user_access_table

class TrainerService:
    async def Trainer_have_course_ids(self,db:Session,token: str):
        try:
            trainer = db.query(user_access_table).filter(
                user_access_table.user_id == token.get("user_id"),
                user_access_table.role == "trainer"
            ).first()
    
            if not trainer:
                raise HTTPException(
                    status_code=404,
                    detail="User is not a trainer or does not exist"
                )
    
            courses = db.query(CourseTable.course_id).filter(
                CourseTable.instructor_id == token.get("user_id")
            ).all()
    
            course_ids = [c.course_id for c in courses]
    
            return {
                "status": True,
                "course_ids": course_ids
            }
    
        except HTTPException:
            raise
    
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to fetch course IDs: {str(e)}"
            )