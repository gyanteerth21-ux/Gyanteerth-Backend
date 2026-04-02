from sqlalchemy import Boolean, Column,String,BigInteger,DateTime,Date,func,ForeignKey,Integer,Boolean
from Models.User_Tables.User_Profile import Base

class OrderTable(Base):
    __tablename__ = "order_table"

    Order_ID = Column(String(50), primary_key=True)
    User_ID = Column(String(50),ForeignKey("user_profile.user_id"),nullable=False)
    Total_Amount = Column(String(50),nullable=False)
    Status = Column(String(50),nullable=False)
    Payment_Method = Column(String(50),nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    created_at = Column(DateTime, default=func.now())