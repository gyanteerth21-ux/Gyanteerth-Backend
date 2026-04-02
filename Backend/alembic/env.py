from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import ALL models (important for metadata)
import Models
from Models.User_Tables.User_Profile import Base
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
from Models.Progress.CourseProgressTable import CourseProgressTable
from Models.Progress.LiveAttendanceTable import LiveAttendanceTable
from Models.Progress.ModuleProgressTable import ModuleProgressTable
from Models.Progress.VideoProgressTable import VideoProgressTable

from Models.Payment.Payment import PaymentTable
from Models.Payment.order_item_table import OrderItemTable
from Models.Payment.Order_table import OrderTable

from Models.Feedback_col.Feedback import FeedbackTable
from Models.Feedback_col.Queries import QueriesTable

from Models.Certificate_Table.Certificate_table import CertificateTable


# Alembic Config
config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


# ✅ 🔥 IMPORTANT FIX: Ignore index changes
def include_object(object, name, type_, reflected, compare_to):
    if type_ == "index":
        return False   # 🚫 Ignore all index changes
    return True


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        include_object=include_object,  # ✅ add this
        compare_type=True,
        compare_server_default=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            include_object=include_object,  # ✅ add this
            compare_type=True,
            compare_server_default=True,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()