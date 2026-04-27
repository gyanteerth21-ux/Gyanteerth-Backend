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
                CourseTable.instructor_id == token.get("user_id"),
                CourseTable.is_active == True,
                CourseTable.draft == False
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

    async def get_course_students_progress(self, course_id: str, db: Session, token: dict):
        try:
            user_id = token.get("user_id")
            role = token.get("role")

            # Admin or the assigned trainer can access
            is_admin = role == "admin"
            
            course = db.query(CourseTable).filter(CourseTable.course_id == course_id).first()
            if not course:
                raise HTTPException(status_code=404, detail="Course not found")

            if not is_admin and course.instructor_id != user_id:
                raise HTTPException(status_code=403, detail="Not authorized to view progress for this course")

            # Fetch students enrolled in this course
            from Models.Progress.EnrollmentTable import EnrollmentTable
            from Models.User_Tables.User_Profile import user_profile_table
            from Models.Progress.CourseProgressTable import CourseProgressTable
            from sqlalchemy import and_

            students = db.query(
                user_profile_table.user_id,
                user_profile_table.user_name,
                user_profile_table.user_email,
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
                    "progress_percentage": s.Progress_Percentage or 0,
                    "completed_modules": s.Completed_Module or 0,
                    "total_modules": s.Total_Modules or 0
                }
                for s in students
            ]

            return {
                "status": True,
                "course_id": course_id,
                "data": data
            }

        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to fetch students progress: {str(e)}")

    async def get_assessment_results(self, token: dict, from_date: str, to_date: str, course_id: str, db: Session):
        from Models.Progress.AssessmentAttemptTable import AssessmentAttemptTable
        from Models.User_Tables.User_Profile import user_profile_table
        from Models.Course_Tables.course_details import CourseTable
        from Models.Course_Tables.Course_Module import CourseModuleTable
        from Models.Assessment_Tables.Assessment_table import AssessmentTable
        from datetime import datetime

        user_id = token.get("user_id")
        role = token.get("role")
        is_admin = role == "admin"

        query = db.query(
            AssessmentAttemptTable.Attempt_ID,
            AssessmentAttemptTable.Score,
            AssessmentAttemptTable.Attempt_No,
            AssessmentAttemptTable.Status,
            AssessmentAttemptTable.created_at.label("Start_Time"),
            AssessmentAttemptTable.Completed_At.label("End_Time"),
            user_profile_table.user_name,
            user_profile_table.user_email,
            CourseTable.course_title,
            AssessmentTable.Title.label("Assessment_Title")
        ).join(
            user_profile_table, user_profile_table.user_id == AssessmentAttemptTable.User_ID
        ).join(
            AssessmentTable, AssessmentTable.Assessment_ID == AssessmentAttemptTable.Assessment_ID
        ).join(
            CourseModuleTable, CourseModuleTable.Module_ID == AssessmentAttemptTable.Module_ID
        ).join(
            CourseTable, CourseTable.course_id == CourseModuleTable.Course_ID
        )

        if not is_admin:
            query = query.filter(CourseTable.instructor_id == user_id)
            
        if course_id:
            query = query.filter(CourseTable.course_id == course_id)

        if from_date:
            try:
                fd = datetime.strptime(from_date, "%Y-%m-%d")
                query = query.filter(AssessmentAttemptTable.created_at >= fd)
            except Exception:
                pass
                
        if to_date:
            try:
                td = datetime.strptime(to_date, "%Y-%m-%d")
                td = td.replace(hour=23, minute=59, second=59)
                query = query.filter(AssessmentAttemptTable.created_at <= td)
            except Exception:
                pass

        results = query.order_by(AssessmentAttemptTable.created_at.desc()).all()
        
        data = []
        for r in results:
            data.append({
                "attempt_id": r.Attempt_ID,
                "student_name": r.user_name,
                "student_email": r.user_email,
                "course_name": r.course_title,
                "assessment_title": r.Assessment_Title,
                "score": r.Score,
                "attempt_no": r.Attempt_No,
                "status": r.Status,
                "start_time": r.Start_Time,
                "end_time": r.End_Time
            })

        return {"status": True, "data": data}

    async def export_assessment_results(self, token: dict, from_date: str, to_date: str, course_id: str, db: Session):
        import pandas as pd
        import io
        from fastapi.responses import StreamingResponse

        results = await self.get_assessment_results(token, from_date, to_date, course_id, db)
        data = results.get("data", [])

        if not data:
            df = pd.DataFrame()
            buffer = io.BytesIO()
            with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, sheet_name="Results")
            buffer.seek(0)
            headers = {'Content-Disposition': 'attachment; filename="assessment_results.xlsx"'}
            return StreamingResponse(buffer, headers=headers, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

        attempt_ids = [r["attempt_id"] for r in data]
        
        from Models.Progress.AssessmentAnswerTable import AssessmentAnswerTable
        from Models.Assessment_Tables.Question_table import QuestionTable
        from Models.Assessment_Tables.Options_table import optionTable
        
        answers = db.query(
            AssessmentAnswerTable.Attempt_ID,
            QuestionTable.Question_Txt,
            optionTable.Option_Txt
        ).join(
            QuestionTable, QuestionTable.Question_ID == AssessmentAnswerTable.Question_ID
        ).join(
            optionTable, optionTable.Option_ID == AssessmentAnswerTable.Option_ID
        ).filter(
            AssessmentAnswerTable.Attempt_ID.in_(attempt_ids)
        ).all()

        attempt_answers = {}
        for ans in answers:
            att_id = ans.Attempt_ID
            q_txt = f"Q: {ans.Question_Txt}"
            opt_txt = ans.Option_Txt
            if att_id not in attempt_answers:
                attempt_answers[att_id] = {}
            attempt_answers[att_id][q_txt] = opt_txt

        expanded_data = []
        for row in data:
            att_id = row["attempt_id"]
            new_row = {
                "Attempt ID": att_id,
                "Student Name": row["student_name"],
                "Student Email": row["student_email"],
                "Course Name": row["course_name"],
                "Assessment Title": row["assessment_title"],
                "Score": row["score"],
                "Attempt No": row["attempt_no"],
                "Status": row["status"],
                "Start Time": row["start_time"],
                "End Time": row["end_time"]
            }
            if att_id in attempt_answers:
                new_row.update(attempt_answers[att_id])
            
            expanded_data.append(new_row)

        df = pd.DataFrame(expanded_data)
        
        for col in ["Start Time", "End Time"]:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col]).dt.tz_localize(None)

        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name="Results")
        buffer.seek(0)

        headers = {
            'Content-Disposition': 'attachment; filename="assessment_results.xlsx"'
        }
        return StreamingResponse(buffer, headers=headers, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")