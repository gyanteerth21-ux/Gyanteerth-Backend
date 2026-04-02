from sqlalchemy import Boolean, Column,String,BigInteger,DateTime,Date,func,ForeignKey,Integer,Boolean
from Models.User_Tables.User_Profile import Base

class OrderItemTable(Base):
    __tablename__ = "order_item_table"

    order_item_ID = Column(String(50), primary_key=True)
    order_ID = Column(String(50),ForeignKey("order_table.Order_ID"),nullable=False)
    Course_ID = Column(String(50),ForeignKey("course_table.course_id"),nullable=False)
    Price = Column(Integer,nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    created_at = Column(DateTime, default=func.now())