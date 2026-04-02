from sqlalchemy import Boolean, Column,String,BigInteger,DateTime,Date,func,ForeignKey,Integer,Boolean
from Models.User_Tables.User_Profile import Base

class VideoProgressTable(Base):
    __tablename__ = "video_progress_table"

    Video_Progress_ID = Column(String(50), primary_key=True)
    User_ID = Column(String(50),ForeignKey("user_profile.user_id"),nullable=False)
    Video_ID = Column(String(50),nullable=False)
    Module_ID = Column(String(50),ForeignKey("course_module_table.Module_ID"),nullable=False)
    Completed_At = Column(DateTime)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    created_at = Column(DateTime, default=func.now())