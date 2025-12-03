from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, ConfigDict


class UserCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    email: EmailStr
    password: str = Field(..., min_length=6)
    role: str = Field(..., pattern="^(employee|hr|sub_admin|admin)$")
    department_id: Optional[int] = None
    office_id: Optional[int] = None
    manager_id: Optional[int] = None
    date_of_joining: Optional[date] = None
    date_of_birth: Optional[date] = None
    status: str = Field(default="active", pattern="^(active|inactive)$")


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    name: str
    email: str
    role: str
    department_id: Optional[int]
    office_id: Optional[int]
    manager_id: Optional[int]
    date_of_joining: Optional[date]
    date_of_birth: Optional[date]
    status: str
    created_at: datetime
    updated_at: datetime


class UserListResponse(BaseModel):
    users: list[UserResponse]
    total: int

