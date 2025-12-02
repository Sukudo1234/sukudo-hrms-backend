from pydantic import BaseModel, ConfigDict, Field


class DepartmentCreate(BaseModel):
    department_name: str = Field(..., min_length=1, max_length=255, description="Name of the department")


class DepartmentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    department_name: str


class DepartmentListResponse(BaseModel):
    departments: list[DepartmentResponse]
    total: int
