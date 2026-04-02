from sqlalchemy import Column, String, Integer, DateTime, func, ForeignKey,Boolean
from Models.User_Tables.User_Profile import Base


class QuestionTable(Base):
    __tablename__ = "course_question_table"
    __table_args__ = {"mysql_engine": "InnoDB"}  

    Question_ID = Column(String(50),primary_key=True,nullable=False)
    Assessment_ID = Column(String(50),ForeignKey("course_assessment_table.Assessment_ID",ondelete="CASCADE"),nullable=False,index=True)
    Question_Txt = Column(String(500), nullable=False)
    Mark = Column(Integer,nullable=False)
    Question_Type = Column(String(100),nullable=False)
    Explanation = Column(String(500),nullable=False)
    Position = Column(Integer,nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())