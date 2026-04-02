from sqlalchemy import Column, String, Integer, DateTime, func, ForeignKey,Boolean
from Models.User_Tables.User_Profile import Base


class CourseVideoTable(Base):
    __tablename__ = "course_video_table"
    __table_args__ = {"mysql_engine": "InnoDB"}  

    Video_ID = Column(String(50),primary_key=True,nullable=False,index=True)
    Module_ID = Column(String(50),ForeignKey("course_module_table.Module_ID",ondelete="CASCADE"),nullable=False,index=True)
    Course_ID = Column(String(50),ForeignKey("course_table.course_id",ondelete="CASCADE"),nullable=False,index=True)
    Video_URL = Column(String(100),nullable=False)
    course_description = Column(String(500), nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())