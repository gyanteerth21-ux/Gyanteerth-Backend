from sqlalchemy import Column, String
import uuid
from Models.User_Tables.User_Profile import Base

class DegreeTable(Base):
    __tablename__ = 'degree_table'
    degree_id = Column(String, primary_key=True, default=lambda: f"DEGREE-{uuid.uuid4()}")
    degree_name = Column(String, unique=True, index=True, nullable=False)
