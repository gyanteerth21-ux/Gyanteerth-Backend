from fastapi import FastAPI, Request, HTTPException
from apscheduler.schedulers.background import BackgroundScheduler
from Database.DB import get_db
from sqlalchemy import text

from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from Models.Course_Tables.Live_Course import LiveCourseTable
from Models.Course_Tables.Recorded_live import CourseRecVideoTable
from Models.Course_Tables.Course_Module import CourseModuleTable


def get_upcoming_live_courses():
    db = get_db()
    now = datetime.utcnow()
    next_10_min = now + timedelta(minutes=10)

    # Step 1: Subquery → get module_ids present in video table
    video_module_subquery = db.query(CourseRecVideoTable.Module_ID).subquery()

    # Step 2: Main query
    live_courses = (
        db.query(LiveCourseTable)
        .join(CourseModuleTable, LiveCourseTable.Module_ID == CourseModuleTable.Module_ID)
        .filter(
            ~LiveCourseTable.Module_ID.in_(video_module_subquery),  # NOT IN video table
            LiveCourseTable.Start_time <= next_10_min,
            LiveCourseTable.Start_time >= now,
            CourseModuleTable.Position == 1
        )
        .all()
    )

    result = []

    for live in live_courses:
        course_id = live.Course_ID

        # Step 3: Get all live classes for that course
        all_live_for_course = (
            db.query(LiveCourseTable)
            .filter(LiveCourseTable.Course_ID == course_id)
            .all()
        )

        result.append({
            "trigger_live": live.Live_ID,
            "course_id": course_id,
            "module_id": live.Module_ID,
            "all_live_classes": all_live_for_course
        })

        print(f"Module ID: {live.Module_ID}, Course ID: {course_id}")

    return result