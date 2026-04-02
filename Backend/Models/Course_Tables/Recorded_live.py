from sqlalchemy import Column, String, Integer, DateTime, func, ForeignKey,Boolean
from Models.User_Tables.User_Profile import Base


class CourseRecVideoTable(Base):
    __tablename__ = "course_rec_video_table"
    __table_args__ = {"mysql_engine": "InnoDB"}  

    Rec_Video_ID = Column(String(50),primary_key=True,nullable=False,index=True)
    Live_ID = Column(String(50),ForeignKey("live_course_table.Live_ID",ondelete="CASCADE"),nullable=False,index=True)
    Course_ID = Column(String(50),ForeignKey("course_table.course_id",ondelete="CASCADE"),nullable=False,index=True)
    Rec_Video_URL = Column(String(100),nullable=False)
    Duration = Column(String(50),nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())