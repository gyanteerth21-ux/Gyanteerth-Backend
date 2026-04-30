from sqlalchemy import Column, String, DateTime, ForeignKey, func
from Models.User_Tables.User_Profile import Base

class AssessmentResetRequestTable(Base):
    __tablename__ = "assessment_reset_request_table"

    Request_ID = Column(String(50), primary_key=True)
    User_ID = Column(String(50), ForeignKey("user_profile.user_id"), nullable=False)
    Assessment_ID = Column(String(50), ForeignKey("course_assessment_table.Assessment_ID"), nullable=False)
    Reason = Column(String(500), nullable=True)
    Status = Column(String(20), default="Pending", nullable=False)
    Requested_At = Column(DateTime, default=func.now(), nullable=False)
    Resolved_At = Column(DateTime, nullable=True)
