from sqlalchemy import Boolean, Column,String,BigInteger,DateTime,Date,func,ForeignKey,Integer,Boolean
from Models.User_Tables.User_Profile import Base

class CertificateTable(Base):
    __tablename__ = "certificate_table"

    Certificate_ID = Column(String(50), primary_key=True)
    User_ID = Column(String(50),ForeignKey("user_profile.user_id"),nullable=False)
    Course_ID = Column(String(50),ForeignKey("course_table.course_id"),nullable=False)
    certificate_number = Column(Integer,nullable=False)
    Verification_code = Column(Integer,nullable=False)
    Certificate_url = Column(String(100),nullable=False)
    Issued_at = Column(DateTime,nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    created_at = Column(DateTime, default=func.now())