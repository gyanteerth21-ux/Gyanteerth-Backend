from sqlalchemy.orm import Session
from fastapi import HTTPException
from Models.Course_Tables.course_details import CourseTable
from Models.Course_Tables.course_demo import CourseDemoTable
from Models.Course_Tables.course_notes import CourseNotesTable
from Models.Course_Tables.course_module import CourseModuleTable
from Models.Course_Tables.course_video import CourseVideoTable
from Models.Course_Tables.course_assignment import AssessmentTable
from Models.Course_Tables.assignment_questions import QuestionTable
from Models.Course_Tables.assignment_options import optionTable
from Models.Course_Tables.LiveCourse import LiveCourseTable
from Models.Course_Tables.course_rec_video import CourseRecVideoTable
from Models.User_Tables.User_Access import user_access_table

def get_active_course_ids(db: Session):
    try:
        active_courses = db.query(CourseTable.course_id).filter(
            CourseTable.is_active == True,
            CourseTable.draft == False
        ).all()
        return [c.course_id for c in active_courses]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch active courses: {str(e)}")

def get_trainer_course_ids(db: Session, trainer_id: str):
    try:
        trainer = db.query(user_access_table).filter(
            user_access_table.user_id == trainer_id,
            user_access_table.role == "trainer"
        ).first()

        if not trainer:
            raise HTTPException(
                status_code=404,
                detail="User is not a trainer or does not exist"
            )

        courses = db.query(CourseTable.course_id).filter(
            CourseTable.instructor_id == trainer_id,
            CourseTable.is_active == True,
            CourseTable.draft == False
        ).all()

        return [c.course_id for c in courses]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch trainer courses: {str(e)}"
        )

def get_full_course_details_data(course_id: str, db: Session):
    try:
        course = db.query(CourseTable).filter(CourseTable.course_id == course_id).first()

        if not course:
            raise HTTPException(status_code=404, detail="Course not found")

        demos = db.query(CourseDemoTable).filter(CourseDemoTable.Course_ID == course_id).all()
        demo_list = [{"demo_id": d.Demo_ID, "title": d.Title, "video_url": d.Video_URL, "duration": d.Duration} for d in demos]

        notes = db.query(CourseNotesTable).filter(CourseNotesTable.Course_ID == course_id).all()
        notes_list = [{"notes_id": n.Notes_ID, "title": n.Title, "file_url": n.File_URL, "file_type": n.File_Type} for n in notes]

        modules = db.query(CourseModuleTable).filter(CourseModuleTable.Course_ID == course_id).order_by(CourseModuleTable.Position).all()
        module_data = []

        for module in modules:
            module_dict = {
                "module_id": module.Module_ID,
                "title": module.Title,
                "description": module.Course_Description,
                "position": module.Position,
                "content": {}
            }

            course_type = course.course_Type.lower() if course.course_Type else ""
            if course_type != "live":
                videos = db.query(CourseVideoTable).filter(CourseVideoTable.Module_ID == module.Module_ID).all()
                module_dict["content"]["videos"] = [{"video_id": v.Video_ID, "video_url": v.Video_URL, "description": v.course_description} for v in videos]
            else:
                live_sessions = db.query(LiveCourseTable).filter(LiveCourseTable.Module_ID == module.Module_ID).all()
                live_list = []
                for live in live_sessions:
                    rec_videos = db.query(CourseRecVideoTable).filter(CourseRecVideoTable.Live_ID == live.Live_ID).all()
                    live_list.append({
                        "live_id": live.Live_ID,
                        "meeting_url": live.Meeting_URL,
                        "provider": live.Provider,
                        "start_time": live.Start_time,
                        "end_time": live.End_time,
                        "status": live.Status,
                        "recordings": [{"rec_video_id": r.Rec_Video_ID, "url": r.Rec_Video_URL, "duration": r.Duration} for r in rec_videos]
                    })
                module_dict["content"]["live_sessions"] = live_list

            assessments = db.query(AssessmentTable).filter(AssessmentTable.Module_ID == module.Module_ID).all()
            assessment_list = []
            for assess in assessments:
                questions = db.query(QuestionTable).filter(QuestionTable.Assessment_ID == assess.Assessment_ID).order_by(QuestionTable.Position).all()
                question_list = []
                for q in questions:
                    options = db.query(optionTable).filter(optionTable.Question_ID == q.Question_ID).order_by(optionTable.Position).all()
                    question_list.append({
                        "question_id": q.Question_ID,
                        "question_text": q.Question_Txt,
                        "mark": q.Mark,
                        "type": q.Question_Type,
                        "position": q.Position,
                        "options": [{"option_id": o.Option_ID, "text": o.Option_Txt, "is_correct": o.Is_Correct, "position": o.Position} for o in options]
                    })
                assessment_list.append({
                    "assessment_id": assess.Assessment_ID, "title": assess.Title,
                    "total_mark": assess.Total_Mark, "passing_mark": assess.Passing_Mark,
                    "duration": assess.Duration, "attempt_limit": assess.Attempt_Limit,
                    "questions": question_list
                })
            module_dict["content"]["assessments"] = assessment_list
            module_data.append(module_dict)

        return {
            "course_id": course.course_id, "title": course.course_title, "description": course.course_description,
            "type": course.course_Type, "level": course.level, "language": course.language,
            "trainer_id": course.instructor_id, "category_id": course.category_id,
            "duration_hours": course.duration, "key_skill": course.skill_set,
            "benefits": course.benefits, "required_knowlegde": course.required_knowledge,
            "thumbnail": course.thumbnail,
            "price": {"original": course.original_pay, "discount": course.discount_pay},
            "demo": demo_list, "notes": notes_list, "modules": module_data
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch course details: {str(e)}")
