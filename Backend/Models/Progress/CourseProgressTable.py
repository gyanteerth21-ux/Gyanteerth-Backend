from sqlalchemy import Boolean, Column,String,BigInteger,DateTime,Date,func,ForeignKey,Integer,Boolean
from Models.User_Tables.User_Profile import Base

class CourseProgressTable(Base):
    __tablename__ = "course_progress_table"

    Course_Progress_ID = Column(String(50), primary_key=True)
    User_ID = Column(String(50),ForeignKey("user_profile.user_id"),nullable=False)
    Course_ID = Column(String(50),ForeignKey("course_table.course_id"),nullable=False)
    Completed_Module = Column(Integer,nullable=False)
    Total_Modules = Column(Integer,nullable=False)
    Progress_Percentage = Column(Integer,nullable=False)
    Completed_At = Column(DateTime)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    created_at = Column(DateTime, default=func.now())
    