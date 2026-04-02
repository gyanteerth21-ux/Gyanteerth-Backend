"""
init_db.py
-----------
Run this ONCE on a fresh database to create all tables.
Then alembic is stamped so future migrations track changes properly.

Usage:
    python init_db.py
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import dotenv
dotenv.load_dotenv()

from Database.DB import engine
from Models.User_Tables.User_Profile import Base

# Import ALL models so their tables are registered with Base.metadata
from Models.User_Tables.User_Profile import user_profile_table
from Models.User_Tables.User_Access import user_access_table
from Models.User_Tables.User_OTP import user_otp_table
from Models.User_Tables.User_Refresh_Token import user_refresh_token_table

from Models.Course_Tables.Course_Category import CategoryCourseTable
from Models.Course_Tables.Course_Demo import CourseDemoTable
from Models.Course_Tables.course_details import CourseTable
from Models.Course_Tables.Course_Module import CourseModuleTable
from Models.Course_Tables.Course_Note import CourseNotesTable
from Models.Course_Tables.Course_Prerec_Video import CourseVideoTable
from Models.Course_Tables.Live_Course import LiveCourseTable
from Models.Course_Tables.Recorded_live import CourseRecVideoTable

from Models.Assessment_Tables.Assessment_table import AssessmentTable
from Models.Assessment_Tables.Question_table import QuestionTable
from Models.Assessment_Tables.Options_table import optionTable

from Models.Progress.AssessmentAttemptTable import AssessmentAttemptTable
from Models.Progress.CourseProgressTable import CourseProgressTable
from Models.Progress.EnrollmentTable import EnrollmentTable
from Models.Progress.LiveAttendanceTable import LiveAttendanceTable
from Models.Progress.ModuleProgressTable import ModuleProgressTable
from Models.Progress.VideoProgressTable import VideoProgressTable

from Models.Payment.Payment import PaymentTable
from Models.Payment.order_item_table import OrderItemTable
from Models.Payment.Order_table import OrderTable

from Models.Feedback_col.Feedback import FeedbackTable
from Models.Feedback_col.Queries import QueriesTable

from Models.Certificate_Table.Certificate_table import CertificateTable

print("Creating all tables on Supabase PostgreSQL...")
Base.metadata.create_all(bind=engine)
print("All tables created successfully!")
