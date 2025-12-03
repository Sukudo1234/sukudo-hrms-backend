from datetime import datetime
from enum import Enum as PyEnum
from sqlalchemy import Column, Integer, String, Date, DateTime, Boolean, ForeignKey, Enum
from sqlalchemy.orm import relationship
from app.core.database import Base


class UserRole(PyEnum):
    EMPLOYEE = "employee"
    HR = "hr"
    SUB_ADMIN = "sub_admin"
    ADMIN = "admin"


class UserStatus(PyEnum):
    ACTIVE = "active"
    INACTIVE = "inactive"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    password_hash = Column(String, nullable=False)
    role = Column(Enum(UserRole), nullable=False, default=UserRole.EMPLOYEE)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=True)
    office_id = Column(Integer, ForeignKey("offices.id"), nullable=True)
    manager_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    date_of_joining = Column(Date, nullable=True)
    date_of_birth = Column(Date, nullable=True)
    status = Column(Enum(UserStatus), nullable=False, default=UserStatus.ACTIVE)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    department = relationship("Department", back_populates="users")
    office = relationship("Office", backref="users")
    manager = relationship("User", remote_side=[id], backref="subordinates")

