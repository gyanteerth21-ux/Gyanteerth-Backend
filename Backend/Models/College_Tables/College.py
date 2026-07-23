from sqlalchemy import Column, String, DateTime, func
from Models.User_Tables.User_Profile import Base

class CollegeTable(Base):
    __tablename__ = "college_table"

    College_ID = Column(String(50), primary_key=True, index=True)
    College_Name = Column(String(200), nullable=False, unique=True, index=True)
    
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    created_at = Column(DateTime, default=func.now())
