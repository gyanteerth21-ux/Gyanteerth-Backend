from sqlalchemy import Boolean, Column,String,BigInteger,DateTime,Date,func,ForeignKey,Integer,Boolean
from Models.User_Tables.User_Profile import Base

class ModuleProgressTable(Base):
    __tablename__ = "module_progress_table"

    Progress_ID = Column(String(50), primary_key=True)
    User_ID = Column(String(50),ForeignKey("user_profile.user_id"),nullable=False)
    Course_ID = Column(String(50),ForeignKey("course_table.course_id"),nullable=False)
    Module_ID = Column(String(50),ForeignKey("course_module_table.Module_ID"),nullable=False)
    Status = Column(String(20),nullable=False)
    Completed_At = Column(DateTime)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    created_at = Column(DateTime, default=func.now())