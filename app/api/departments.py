from typing import Optional, Union
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.core.database import get_session
from app.models.department import Department
from app.schemas.department import DepartmentCreate, DepartmentResponse, DepartmentListResponse

router = APIRouter(prefix="/departments", tags=["departments"])


@router.post("/createDepartment", response_model=DepartmentResponse, status_code=status.HTTP_201_CREATED)
async def create_department(
    department_data: DepartmentCreate,
    session: AsyncSession = Depends(get_session)
):
    """
    Create a new department.
    """
    # Check if department name already exists
    result = await session.execute(
        select(Department).where(Department.department_name == department_data.department_name)
    )
    existing_department = result.scalar_one_or_none()
    if existing_department:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Department '{department_data.department_name}' already exists"
        )
    
    # Create new department
    new_department = Department(
        department_name=department_data.department_name
    )
    
    session.add(new_department)
    await session.commit()
    await session.refresh(new_department)
    
    return DepartmentResponse.model_validate({
        "id": new_department.id,
        "department_name": new_department.department_name
    })


@router.get("", response_model=Union[DepartmentResponse, DepartmentListResponse])
async def get_departments(
    id: Optional[int] = Query(None, description="Department ID to get a specific department"),
    session: AsyncSession = Depends(get_session)
):
    """
    Get departments.
    - If 'id' is provided, returns the specific department with that ID.
    - If 'id' is not provided, returns all departments.
    """
    if id is not None:
        # Get specific department by ID
        result = await session.execute(
            select(Department).where(Department.id == id)
        )
        department = result.scalar_one_or_none()
        
        if not department:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Department with id {id} not found"
            )
        
        return DepartmentResponse.model_validate({
            "id": department.id,
            "department_name": department.department_name
        })
    else:
        # Get all departments
        # Get total count
        count_result = await session.execute(select(func.count(Department.id)))
        total = count_result.scalar_one()
        
        # Get all departments
        result = await session.execute(select(Department))
        departments = result.scalars().all()
        
        # Convert to response models
        department_responses = [
            DepartmentResponse.model_validate({
                "id": dept.id,
                "department_name": dept.department_name
            })
            for dept in departments
        ]
        
        return DepartmentListResponse(departments=department_responses, total=total)
