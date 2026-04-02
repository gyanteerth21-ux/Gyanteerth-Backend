from sqlalchemy import Column,String,BigInteger,DateTime,Date,func,ForeignKey
from .User_Profile import Base

class user_access_table(Base):
    __tablename__ = "user_access"

    access_id = Column(String(50), primary_key=True)
    user_id = Column(String(50), ForeignKey("user_profile.user_id"))
    provider_id = Column(String(150))
    provider_name = Column(String(150))
    role = Column(String(50))
    password_hash = Column(String(255))
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    created_at = Column(DateTime, default=func.now())