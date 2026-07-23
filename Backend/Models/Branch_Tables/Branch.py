from sqlalchemy import Column, String
import uuid
from Models.User_Tables.User_Profile import Base

class BranchTable(Base):
    __tablename__ = 'branch_table'
    branch_id = Column(String, primary_key=True, default=lambda: f"BRANCH-{uuid.uuid4()}")
    branch_name = Column(String, unique=True, index=True, nullable=False)
