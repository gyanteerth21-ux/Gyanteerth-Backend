from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import exists, and_, func
from datetime import datetime
import uuid

# Models
from Models.Course_Tables.course_details import CourseTable
from Models.Course_Tables.Course_Module import CourseModuleTable
from Models.Course_Tables.Course_Prerec_Video import CourseVideoTable
from Models.Course_Tables.Live_Course import LiveCourseTable
from Models.Assessment_Tables.Assessment_table import AssessmentTable
from Models.Assessment_Tables.Question_table import QuestionTable
from Models.Assessment_Tables.Options_table import optionTable

# Progress Models
from Models.Progress.VideoProgressTable import VideoProgressTable
from Models.Progress.LiveAttendanceTable import LiveAttendanceTable
from Models.Progress.AssessmentAttemptTable import AssessmentAttemptTable
from Models.Progress.ModuleProgressTable import ModuleProgressTable
from Models.Progress.CourseProgressTable import CourseProgressTable
from Models.Progress.AssessmentResetRequestTable import AssessmentResetRequestTable

class ProgressService:
    async def mark_video_progress(self, user_id: str, course_id: str, module_id: str, video_id: str, db: Session):
        existing = db.query(VideoProgressTable).filter(
            VideoProgressTable.User_ID == user_id,
            VideoProgressTable.Video_ID == video_id
        ).first()

        if not existing:
            new_prog = VideoProgressTable(
                Video_Progress_ID=f"VID-PROG-{uuid.uuid4().hex[:8]}",
                User_ID=user_id,
                Video_ID=video_id,
                Module_ID=module_id,
                Completed_At=datetime.utcnow()
            )
            db.add(new_prog)
            db.commit()

            # Recalculate module progress
            self._calculate_module_progress(user_id, course_id, module_id, db)

        return {"message": "Video marked as completed successfully"}

    async def submit_assessment(self, user_id: str, course_id: str, module_id: str, assessment_id: str, answers: dict[str, str], db: Session):
        # 1. Fetch assessment details
        assessment = db.query(AssessmentTable).filter(AssessmentTable.Assessment_ID == assessment_id).first()
        if not assessment:
            raise HTTPException(status_code=404, detail="Assessment not found")

        # 2. Check existing attempt
        attempt = db.query(AssessmentAttemptTable).filter(
            AssessmentAttemptTable.User_ID == user_id,
            AssessmentAttemptTable.Assessment_ID == assessment_id
        ).first()

        attempt_no = 1
        if attempt:
            if attempt.Status == "Passed":
                return {
                    "message": "Assessment already passed",
                    "score": attempt.Score,
                    "attempt_no": attempt.Attempt_No,
                    "status": attempt.Status,
                    "passed": True
                }
            if attempt.Attempt_No >= assessment.Attempt_Limit:
                raise HTTPException(status_code=400, detail="Maximum distinct attempts reached. Contact Admin to reset.")
            attempt_no = attempt.Attempt_No + 1

        # 3. Calculate score
        score = 0
        answer_records = []
        for q_id, o_id in answers.items():
            if not str(q_id).startswith("QUES-"):
                continue
            if not o_id or not str(o_id).strip():
                continue
                
            correct_opt = db.query(optionTable).filter(
                optionTable.Question_ID == q_id,
                optionTable.Is_Correct == True
            ).first()
            
            is_correct = False
            if correct_opt and correct_opt.Option_ID == o_id:
                is_correct = True
                # Add marks for this question
                question = db.query(QuestionTable).filter(QuestionTable.Question_ID == q_id).first()
                if question:
                    score += question.Mark

            answer_records.append({
                "Question_ID": q_id,
                "Option_ID": o_id,
                "Is_Correct": is_correct
            })

        passed = score >= assessment.Passing_Mark
        new_status = "Passed" if passed else "Failed"

        # 4. Save attempt
        from Models.Progress.AssessmentAnswerTable import AssessmentAnswerTable
        should_save_answers = False
        target_attempt_id = None

        if attempt:
            target_attempt_id = attempt.Attempt_ID
            # We ONLY update if the new score is higher OR if they passed, keep best score
            if score > attempt.Score:
                attempt.Score = score
                should_save_answers = True
                
            attempt.Attempt_No = attempt_no
            if passed:
                attempt.Status = new_status
            attempt.Completed_At = datetime.utcnow()
        else:
            target_attempt_id = f"ATTEMPT-{uuid.uuid4().hex[:8]}"
            new_attempt = AssessmentAttemptTable(
                Attempt_ID=target_attempt_id,
                User_ID=user_id,
                Assessment_ID=assessment_id,
                Module_ID=module_id,
                Score=score,
                Attempt_No=attempt_no,
                Status=new_status,
                Completed_At=datetime.utcnow()
            )
            db.add(new_attempt)
            should_save_answers = True

        if should_save_answers:
            db.query(AssessmentAnswerTable).filter(AssessmentAnswerTable.Attempt_ID == target_attempt_id).delete()
            for ans in answer_records:
                new_ans = AssessmentAnswerTable(
                    Answer_ID=f"ANS-{uuid.uuid4().hex[:8]}",
                    Attempt_ID=target_attempt_id,
                    Question_ID=ans["Question_ID"],
                    Option_ID=ans["Option_ID"],
                    Is_Correct=ans["Is_Correct"],
                    created_at=datetime.utcnow()
                )
                db.add(new_ans)

        db.commit()

        if passed:
            self._calculate_module_progress(user_id, course_id, module_id, db)

        return {
            "message": "Assessment submitted successfully",
            "score": score,
            "attempt_no": attempt_no,
            "status": new_status,
            "passed": passed
        }

    def _calculate_module_progress(self, user_id: str, course_id: str | None, module_id: str, db: Session):
        """ Checks if all required items in a module are completed """

        if not course_id:
            mod = db.query(CourseModuleTable).filter(CourseModuleTable.Module_ID == module_id).first()
            if not mod:
                return False
            course_id = mod.Course_ID

        from Models.Course_Tables.course_details import CourseTable
        course = db.query(CourseTable).filter(CourseTable.course_id == course_id).first()
        course_type = course.course_Type.lower() if course and course.course_Type else ""

        # Check total videos vs completed videos (only for non-live courses)
        if course_type != "live":
            video_ids = db.query(CourseVideoTable.Video_ID).filter(CourseVideoTable.Module_ID == module_id).all()
            if video_ids:
                total_videos = len(video_ids)
                completed_videos = db.query(func.count(VideoProgressTable.Video_ID)).filter(
                    VideoProgressTable.User_ID == user_id,
                    VideoProgressTable.Module_ID == module_id
                ).scalar()
                if completed_videos < total_videos:
                    return False

        # Check live sessions (only for live courses)
        if course_type == "live":
            live_ids = db.query(LiveCourseTable.Live_ID).filter(LiveCourseTable.Module_ID == module_id).all()
            if live_ids:
                total_lives = len(live_ids)
                completed_lives = db.query(func.count(LiveAttendanceTable.Live_Class_ID)).filter(
                    LiveAttendanceTable.User_ID == user_id,
                    LiveAttendanceTable.Module_ID == module_id,
                    LiveAttendanceTable.Is_Present == True
                ).scalar()
                if completed_lives < total_lives:
                    return False

        # Check assessments (applicable to all courses)
        assessment_ids = db.query(AssessmentTable.Assessment_ID).filter(AssessmentTable.Module_ID == module_id).all()
        if assessment_ids:
            total_assessments = len(assessment_ids)
            completed_assessments = db.query(func.count(AssessmentAttemptTable.Assessment_ID)).filter(
                AssessmentAttemptTable.User_ID == user_id,
                AssessmentAttemptTable.Module_ID == module_id,
                AssessmentAttemptTable.Status == "Passed"
            ).scalar()
            if completed_assessments < total_assessments:
                return False

        # Everything is completed -> update module progress
        mod_prog = db.query(ModuleProgressTable).filter(
            ModuleProgressTable.User_ID == user_id,
            ModuleProgressTable.Module_ID == module_id
        ).first()

        if not mod_prog:
            mod_prog = ModuleProgressTable(
                Progress_ID=f"MOD-PROG-{uuid.uuid4().hex[:8]}",
                User_ID=user_id,
                Course_ID=course_id,
                Module_ID=module_id,
                Status="Completed",
                Completed_At=datetime.utcnow()
            )
            db.add(mod_prog)
        else:
            mod_prog.Status = "Completed"
            mod_prog.Completed_At = datetime.utcnow()

        db.commit()

        # Trigger course recalculation
        self._calculate_course_progress(user_id, course_id, db)
        return True

    def _calculate_course_progress(self, user_id: str, course_id: str, db: Session):
        from Models.Course_Tables.course_details import CourseTable
        course = db.query(CourseTable).filter(CourseTable.course_id == course_id).first()
        course_type = course.course_Type.lower() if course and course.course_Type else ""

        # Calculate total lessons (videos + live sessions + assessments)
        total_videos = 0
        total_lives = 0

        if course_type != "live":
            total_videos = db.query(func.count(CourseVideoTable.Video_ID)).join(
                CourseModuleTable, CourseModuleTable.Module_ID == CourseVideoTable.Module_ID
            ).filter(CourseModuleTable.Course_ID == course_id).scalar() or 0
        
        if course_type == "live":
            total_lives = db.query(func.count(LiveCourseTable.Live_ID)).join(
                CourseModuleTable, CourseModuleTable.Module_ID == LiveCourseTable.Module_ID
            ).filter(CourseModuleTable.Course_ID == course_id).scalar() or 0

        total_assessments = db.query(func.count(AssessmentTable.Assessment_ID)).join(
            CourseModuleTable, CourseModuleTable.Module_ID == AssessmentTable.Module_ID
        ).filter(CourseModuleTable.Course_ID == course_id).scalar() or 0

        total_items = total_videos + total_lives + total_assessments

        if total_items == 0:
            return

        # Calculate completed lessons
        completed_videos = 0
        completed_lives = 0

        if course_type != "live":
            completed_videos = db.query(func.count(VideoProgressTable.Video_ID)).join(
                CourseModuleTable, CourseModuleTable.Module_ID == VideoProgressTable.Module_ID
            ).filter(
                CourseModuleTable.Course_ID == course_id,
                VideoProgressTable.User_ID == user_id
            ).scalar() or 0

        if course_type == "live":
            completed_lives = db.query(func.count(LiveAttendanceTable.Live_Class_ID)).join(
                CourseModuleTable, CourseModuleTable.Module_ID == LiveAttendanceTable.Module_ID
            ).filter(
                CourseModuleTable.Course_ID == course_id,
                LiveAttendanceTable.User_ID == user_id,
                LiveAttendanceTable.Is_Present == True
            ).scalar() or 0

        completed_assessments = db.query(func.count(AssessmentAttemptTable.Assessment_ID)).join(
            CourseModuleTable, CourseModuleTable.Module_ID == AssessmentAttemptTable.Module_ID
        ).filter(
            CourseModuleTable.Course_ID == course_id,
            AssessmentAttemptTable.User_ID == user_id,
            AssessmentAttemptTable.Status == "Passed"
        ).scalar() or 0

        completed_items = completed_videos + completed_lives + completed_assessments
        
        percent = int((completed_items / total_items) * 100)

        # Still keep track of completed modules for other reporting purposes
        total_modules = db.query(func.count(CourseModuleTable.Module_ID)).filter(
            CourseModuleTable.Course_ID == course_id
        ).scalar() or 0

        completed_modules = db.query(func.count(ModuleProgressTable.Module_ID)).filter(
            ModuleProgressTable.User_ID == user_id,
            ModuleProgressTable.Course_ID == course_id,
            ModuleProgressTable.Status == "Completed"
        ).scalar() or 0

        course_prog = db.query(CourseProgressTable).filter(
            CourseProgressTable.User_ID == user_id,
            CourseProgressTable.Course_ID == course_id
        ).first()

        if not course_prog:
            course_prog = CourseProgressTable(
                Course_Progress_ID=f"CRS-PROG-{uuid.uuid4().hex[:8]}",
                User_ID=user_id,
                Course_ID=course_id,
                Completed_Module=completed_modules,
                Total_Modules=total_modules,
                Progress_Percentage=percent,
                Completed_At=datetime.utcnow() if percent == 100 else None
            )
            db.add(course_prog)
        else:
            course_prog.Completed_Module = completed_modules
            course_prog.Total_Modules = total_modules
            course_prog.Progress_Percentage = percent
            if percent == 100 and not course_prog.Completed_At:
                course_prog.Completed_At = datetime.utcnow()

        db.commit()

    async def get_course_progress(self, user_id: str, course_id: str, db: Session):
        # Auto-heal any corrupted progress by recalculating dynamically on fetch
        self._calculate_course_progress(user_id, course_id, db)

        course_prog = db.query(CourseProgressTable).filter(
            CourseProgressTable.User_ID == user_id,
            CourseProgressTable.Course_ID == course_id
        ).first()

        percent = course_prog.Progress_Percentage if course_prog else 0
        comp_mods = course_prog.Completed_Module if course_prog else 0
        tot_mods = course_prog.Total_Modules if course_prog else 0

        mod_progs = db.query(ModuleProgressTable).filter(
            ModuleProgressTable.User_ID == user_id,
            ModuleProgressTable.Course_ID == course_id
        ).all()

        mod_dict = {mp.Module_ID: mp.Status for mp in mod_progs}

        assess_progs = db.query(AssessmentAttemptTable).join(
            CourseModuleTable, CourseModuleTable.Module_ID == AssessmentAttemptTable.Module_ID
        ).filter(
            AssessmentAttemptTable.User_ID == user_id,
            CourseModuleTable.Course_ID == course_id
        ).all()

        a_list = [
            {
                "assessment_id": ap.Assessment_ID,
                "score": ap.Score,
                "attempt_no": ap.Attempt_No,
                "attempts_used": ap.Attempt_No,
                "status": ap.Status
            } for ap in assess_progs
        ]

        video_progs = []
        try:
            video_progs = db.query(VideoProgressTable).join(
                CourseModuleTable, CourseModuleTable.Module_ID == VideoProgressTable.Module_ID
            ).filter(
                VideoProgressTable.User_ID == user_id,
                CourseModuleTable.Course_ID == course_id
            ).all()
        except Exception as e:
            print(f"Error fetching video progress: {e}")

        live_progs = []
        try:
            live_progs = db.query(LiveAttendanceTable).join(
                CourseModuleTable, CourseModuleTable.Module_ID == LiveAttendanceTable.Module_ID
            ).filter(
                LiveAttendanceTable.User_ID == user_id,
                CourseModuleTable.Course_ID == course_id
            ).all()
        except Exception as e:
            print(f"Error fetching live progress: {e}")

        lessons_progress = [
            {"lesson_id": vp.Video_ID, "status": "Completed", "completed": True}
            for vp in video_progs
        ] + [
            {"lesson_id": lp.Live_Class_ID, "status": "Completed" if lp.Is_Present else "Pending", "completed": lp.Is_Present}
            for lp in live_progs
        ]

        return {
            "course_id": course_id,
            "total_modules": tot_mods,
            "completed_modules": comp_mods,
            "progress_percentage": percent,
            "modules_progress": mod_dict,
            "assessments_progress": a_list,
            "lessons_progress": lessons_progress
        }

    async def reset_assessment_attempts(self, user_id: str, assessment_id: str, db: Session):
        attempt = db.query(AssessmentAttemptTable).filter(
            AssessmentAttemptTable.User_ID == user_id,
            AssessmentAttemptTable.Assessment_ID == assessment_id
        ).first()

        if not attempt:
            raise HTTPException(status_code=404, detail="No attempt found to reset")

        db.delete(attempt)
        db.commit()
        return {"message": "Assessment attempts successfully reset for user"}

    async def request_assessment_reset(self, user_id: str, assessment_id: str, reason: str, db: Session):
        assessment = db.query(AssessmentTable).filter(AssessmentTable.Assessment_ID == assessment_id).first()
        if not assessment:
            raise HTTPException(status_code=404, detail="Assessment not found")

        # Check if already requested and pending
        existing_request = db.query(AssessmentResetRequestTable).filter(
            AssessmentResetRequestTable.User_ID == user_id,
            AssessmentResetRequestTable.Assessment_ID == assessment_id,
            AssessmentResetRequestTable.Status == "Pending"
        ).first()

        if existing_request:
            raise HTTPException(status_code=400, detail="You already have a pending request for this assessment")

        request_id = f"RST-REQ-{uuid.uuid4().hex[:8]}"
        new_request = AssessmentResetRequestTable(
            Request_ID=request_id,
            User_ID=user_id,
            Assessment_ID=assessment_id,
            Reason=reason,
            Status="Pending",
            Requested_At=datetime.utcnow()
        )
        db.add(new_request)
        db.commit()

        return {
            "message": "Reset request submitted successfully",
            "request_id": request_id
        }
