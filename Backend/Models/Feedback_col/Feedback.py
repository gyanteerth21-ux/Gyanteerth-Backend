from sqlalchemy import Boolean, Column,String,BigInteger,DateTime,Date,func,ForeignKey,Integer,Boolean
from Models.User_Tables.User_Profile import Base

class FeedbackTable(Base):
    __tablename__ = "feedback_table"

    Feedback_ID = Column(String(50), primary_key=True)
    User_ID = Column(String(50),ForeignKey("user_profile.user_id"),nullable=False)
    Course_ID = Column(String(50),ForeignKey("course_table.course_id"),nullable=False)
    Course_rating = Column(String(50),nullable=False)
    Instructor_rating = Column(String(50),nullable=False)
    Review = Column(String(200),nullable=False)
    Disply_Status = Column(String(50),nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    created_at = Column(DateTime, default=func.now())