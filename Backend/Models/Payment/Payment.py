from sqlalchemy import Boolean, Column,String,BigInteger,DateTime,Date,func,ForeignKey,Integer,Boolean
from Models.User_Tables.User_Profile import Base

class PaymentTable(Base):
    __tablename__ = "payment_table"

    Payment_ID = Column(String(50), primary_key=True)
    order_ID = Column(String(50),ForeignKey("order_table.Order_ID"),nullable=False)
    User_ID = Column(String(50),ForeignKey("user_profile.user_id"),nullable=False)
    Payment_Gateway = Column(String(50),nullable=False)
    Transaction_Id = Column(String(100),nullable=False)
    Amount = Column(String(50),nullable=False)
    Status = Column(String(50),nullable=False)
    Payment_Time = Column(DateTime,nullable = False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    created_at = Column(DateTime, default=func.now())