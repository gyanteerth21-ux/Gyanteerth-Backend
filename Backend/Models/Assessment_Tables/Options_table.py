from sqlalchemy import Column, String, Integer, DateTime, func, ForeignKey,Boolean
from Models.User_Tables.User_Profile import Base


class optionTable(Base):
    __tablename__ = "question_option_table"
    __table_args__ = {"mysql_engine": "InnoDB"}  

    Option_ID = Column(String(50),primary_key=True,nullable=False,index=True)
    Question_ID = Column(String(50),ForeignKey("course_question_table.Question_ID",ondelete="CASCADE"),nullable=False,index=True)
    Option_Txt = Column(String(500), nullable=False)
    Is_Correct = Column(Boolean,nullable=False)
    Position = Column(Integer,nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())