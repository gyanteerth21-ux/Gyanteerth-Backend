from sqlalchemy import Boolean, Column,String,BigInteger,DateTime,Date,func,ForeignKey,Integer,Boolean, CheckConstraint
from Models.User_Tables.User_Profile import Base

class AssessmentAttemptTable(Base):
    __tablename__ = "assessment_attempt_table"

    Attempt_ID = Column(String(50), primary_key=True)
    User_ID = Column(String(50),ForeignKey("user_profile.user_id"),nullable=False)
    Assessment_ID = Column(String(50),ForeignKey("course_assessment_table.Assessment_ID"),nullable=False)
    Module_ID = Column(String(50),ForeignKey("course_module_table.Module_ID"),nullable=False)
    Score = Column(Integer,nullable=False)
    Attempt_No = Column(Integer,nullable=False)
    Status = Column(String(20),nullable=False)
    Completed_At = Column(DateTime)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    created_at = Column(DateTime, default=func.now())