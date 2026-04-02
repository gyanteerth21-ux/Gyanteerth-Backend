from sqlalchemy import Column, String, Integer, DateTime, func, ForeignKey,Boolean
from Models.User_Tables.User_Profile import Base


class CourseDemoTable(Base):
    __tablename__ = "course_demo_table"
    __table_args__ = {"mysql_engine": "InnoDB"}  

    Demo_ID = Column(String(50), primary_key=True,nullable=False,index=True)
    Course_ID = Column(String(50),ForeignKey("course_table.course_id",ondelete="CASCADE"),nullable=False,index=True)
    Title = Column(String(100),nullable=False)
    Video_URL = Column(String(100),nullable=False)
    Duration = Column(String(50),nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())