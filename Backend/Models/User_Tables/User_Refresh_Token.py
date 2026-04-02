from sqlalchemy import Boolean, Column,String,BigInteger,DateTime,Date,func,ForeignKey,Boolean
from .User_Profile import Base

class user_refresh_token_table(Base):
    __tablename__ = "user_refresh_tokens"

    refresh_token_id = Column(String(50), primary_key=True)
    user_id = Column(String(50), ForeignKey("user_profile.user_id"))
    refresh_token = Column(String(255))
    device_name = Column(String(255))
    ip_address = Column(String(50))
    user_agent = Column(String(255))
    expires_at = Column(DateTime, nullable=False)
    is_revoked = Column(Boolean, default=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    created_at = Column(DateTime, default=func.now())