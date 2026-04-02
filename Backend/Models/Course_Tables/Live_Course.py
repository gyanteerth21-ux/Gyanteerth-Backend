from sqlalchemy import Column, String, Integer, DateTime, func, ForeignKey,Boolean
from Models.User_Tables.User_Profile import Base


class LiveCourseTable(Base):
    __tablename__ = "live_course_table"
    __table_args__ = {"mysql_engine": "InnoDB"}  

    Live_ID = Column(String(50),primary_key=True,nullable=False,index=True)
    Module_ID = Column(String(50),ForeignKey("course_module_table.Module_ID",ondelete="CASCADE"),nullable=False,index=True)
    Course_ID = Column(String(50),ForeignKey("course_table.course_id",ondelete="CASCADE"),nullable=False,index=True)
    Meeting_URL = Column(String(100),nullable=False)
    Provider = Column(String(100), nullable=False)
    Start_time = Column(DateTime,nullable=False)
    End_time = Column(DateTime,nullable=False)
    Status = Column(String(50),nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())