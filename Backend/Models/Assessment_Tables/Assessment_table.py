from sqlalchemy import Column, String, Integer, DateTime, func, ForeignKey,Boolean
from Models.User_Tables.User_Profile import Base


class AssessmentTable(Base):
    __tablename__ = "course_assessment_table"
    __table_args__ = {"mysql_engine": "InnoDB"}  

    Assessment_ID = Column(String(50),primary_key=True,nullable=False)
    Module_ID = Column(String(50),ForeignKey("course_module_table.Module_ID",ondelete="CASCADE"),nullable=False,index=True)
    Title = Column(String(100),nullable=False)
    Description = Column(String(500), nullable=False)
    Total_Mark = Column(Integer,nullable=False)
    Passing_Mark = Column(Integer,nullable=False)
    Duration = Column(Integer,nullable=False)
    Attempt_Limit = Column(Integer,nullable=False)
    Status = Column(String(50),nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())