from sqlalchemy import Column, String, Integer, DateTime, func, ForeignKey,Boolean
from Models.User_Tables.User_Profile import Base


class CategoryCourseTable(Base):
    __tablename__ = "category_course_table"

    Category_ID = Column(String(50),primary_key=True,nullable=False,index=True)
    Category_Name = Column(String(100), nullable=False)
    slug = Column(String(100), unique=True, index=True, nullable=True) 
    Parent_ID = Column(String(50),ForeignKey("category_course_table.Category_ID"),nullable=True,index=True)     
    Course_Description = Column(String(500), nullable=False)
    Icon = Column(String(100),nullable=True)
    Thumbnail = Column(String(100),nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())