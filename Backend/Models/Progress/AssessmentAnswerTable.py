from sqlalchemy import Column, String, Boolean, DateTime, func, ForeignKey
from Models.User_Tables.User_Profile import Base

class AssessmentAnswerTable(Base):
    __tablename__ = "assessment_answer_table"

    Answer_ID = Column(String(50), primary_key=True)
    Attempt_ID = Column(String(50), ForeignKey("assessment_attempt_table.Attempt_ID", ondelete="CASCADE"), nullable=False, index=True)
    Question_ID = Column(String(50), ForeignKey("course_question_table.Question_ID", ondelete="CASCADE"), nullable=False)
    Option_ID = Column(String(50), ForeignKey("question_option_table.Option_ID", ondelete="CASCADE"), nullable=False)
    Is_Correct = Column(Boolean, nullable=False)
    created_at = Column(DateTime, default=func.now())
