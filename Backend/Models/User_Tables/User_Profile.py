from sqlalchemy import Column, String, BigInteger, DateTime, Date, func, ForeignKey, Boolean
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class user_profile_table(Base):
    __tablename__ = "user_profile"

    user_id = Column(String(50), primary_key=True, index=True)
    user_name = Column(String(150), nullable=True)
    user_pic = Column(String(255), nullable=True)
    user_email = Column(String(150), nullable=False, index=True)
    user_email_verified = Column(Boolean, default=False)
    user_number = Column(BigInteger, nullable=True)
    user_dob = Column(Date, nullable=True)
    user_gender = Column(String(10), nullable=True)
    user_city = Column(String(100), nullable=True)
    user_state = Column(String(100), nullable=True)
    Status = Column(String(30),nullable=True)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    created_at = Column(DateTime, default=func.now())