from sqlalchemy import Column, String, Integer, DateTime, func, ForeignKey,Boolean
from Models.User_Tables.User_Profile import Base


class CourseTable(Base):
    __tablename__ = "course_table"
    __table_args__ = {"mysql_engine": "InnoDB"}  

    course_id = Column(String(50), primary_key=True, index=True)
    instructor_id = Column(String(50),ForeignKey("user_profile.user_id"),nullable=False,index=True)
    category_id = Column(String(50),ForeignKey("category_course_table.Category_ID"),nullable=False,index=True)
    course_Type = Column(String(20),nullable=False)
    course_title = Column(String(100), nullable=False)
    course_description = Column(String(500), nullable=False)
    slug = Column(String(100), unique=True, index=True, nullable=True)
    skill_set = Column(String(200), nullable=False)
    required_knowledge = Column(String(200), nullable=False)
    benefits = Column(String(200), nullable=False)
    thumbnail = Column(String(255), nullable=False)
    duration = Column(String(50), nullable=False)
    level = Column(String(30), nullable=False)
    language = Column(String(50), nullable=False)
    original_pay = Column(Integer, nullable=False)
    discount_pay = Column(Integer, nullable=False)
    is_active = Column(Boolean, default=False)
    students_count = Column(Integer, default=0)
    draft   = Column(Boolean,nullable=False,default=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())