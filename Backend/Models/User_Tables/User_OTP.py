from sqlalchemy import Boolean, Column,String,BigInteger,DateTime,Date,func,ForeignKey,Integer,Boolean
from .User_Profile import Base

class user_otp_table(Base):
    __tablename__ = "user_otp"

    otp_id = Column(String(50), primary_key=True)
    user_id = Column(String(50), ForeignKey("user_profile.user_id"),unique=True)
    otp = Column(Integer, nullable=False)
    expires_at = Column(DateTime, nullable=False,index=True)
    is_used = Column(Boolean, default=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    created_at = Column(DateTime, default=func.now())