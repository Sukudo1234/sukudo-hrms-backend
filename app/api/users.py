from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.core.database import get_session
from app.core.dependencies import get_current_user
from app.core.security import get_password_hash
from app.models.user import User, UserRole, UserStatus
from app.schemas.user import UserCreate, UserResponse, UserListResponse

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/createUser", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserCreate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """
    Create a new user. Requires JWT authentication.
    Only admin, sub_admin, and hr roles can create users.
    """
    # Check if current user has permission to create users
    if current_user.role not in [UserRole.ADMIN, UserRole.SUB_ADMIN, UserRole.HR]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to create users"
        )
    
    # Check if email already exists
    result = await session.execute(
        select(User).where(User.email == user_data.email)
    )
    existing_user = result.scalar_one_or_none()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Validate manager_id if provided
    if user_data.manager_id:
        manager_result = await session.execute(
            select(User).where(User.id == user_data.manager_id)
        )
        manager = manager_result.scalar_one_or_none()
        if not manager:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Manager not found"
            )
    
    # Validate department_id if provided
    if user_data.department_id:
        from app.models.department import Department
        dept_result = await session.execute(
            select(Department).where(Department.id == user_data.department_id)
        )
        department = dept_result.scalar_one_or_none()
        if not department:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Department not found"
            )
    
    # Create new user
    try:
        user_role = UserRole(user_data.role)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid role. Must be one of: {[r.value for r in UserRole]}"
        )
    
    try:
        user_status = UserStatus(user_data.status)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid status. Must be one of: {[s.value for s in UserStatus]}"
        )
    
    new_user = User(
        name=user_data.name,
        email=user_data.email,
        password_hash=get_password_hash(user_data.password),
        role=user_role,
        department_id=user_data.department_id,
        manager_id=user_data.manager_id,
        date_of_joining=user_data.date_of_joining,
        date_of_birth=user_data.date_of_birth,
        status=user_status
    )
    
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    
    # Convert SQLAlchemy model to Pydantic model using model_validate
    return UserResponse.model_validate({
        "id": new_user.id,
        "name": new_user.name,
        "email": new_user.email,
        "role": new_user.role.value,
        "department_id": new_user.department_id,
        "manager_id": new_user.manager_id,
        "date_of_joining": new_user.date_of_joining,
        "date_of_birth": new_user.date_of_birth,
        "status": new_user.status.value,
        "created_at": new_user.created_at,
        "updated_at": new_user.updated_at
    })


@router.get("/getUsers", response_model=UserListResponse)
async def get_users(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return"),
    role: Optional[str] = Query(None, description="Filter by role"),
    status_filter: Optional[str] = Query(None, alias="status", description="Filter by status"),
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """
    Get list of users with pagination. Requires JWT authentication.
    Only admin, sub_admin, and hr roles can view users.
    """
    # Check if current user has permission to view users
    if current_user.role not in [UserRole.ADMIN, UserRole.SUB_ADMIN, UserRole.HR]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to view users"
        )
    
    # Build base query for filtering
    base_query = select(User)
    
    # Apply filters
    if role:
        try:
            user_role = UserRole(role)
            base_query = base_query.where(User.role == user_role)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid role. Must be one of: {[r.value for r in UserRole]}"
            )
    
    if status_filter:
        try:
            user_status = UserStatus(status_filter)
            base_query = base_query.where(User.status == user_status)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid status. Must be one of: {[s.value for s in UserStatus]}"
            )
    
    # Get total count with same filters
    count_query = select(func.count(User.id))
    if role:
        try:
            user_role = UserRole(role)
            count_query = count_query.where(User.role == user_role)
        except ValueError:
            pass
    if status_filter:
        try:
            user_status = UserStatus(status_filter)
            count_query = count_query.where(User.status == user_status)
        except ValueError:
            pass
    
    total_result = await session.execute(count_query)
    total = total_result.scalar_one()
    
    # Apply pagination to main query
    query = base_query.offset(skip).limit(limit)
    
    # Execute query
    result = await session.execute(query)
    users = result.scalars().all()
    
    # Convert to response models
    user_responses = [
        UserResponse.model_validate({
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role.value,
            "department_id": user.department_id,
            "manager_id": user.manager_id,
            "date_of_joining": user.date_of_joining,
            "date_of_birth": user.date_of_birth,
            "status": user.status.value,
            "created_at": user.created_at,
            "updated_at": user.updated_at
        })
        for user in users
    ]
    
    return UserListResponse(users=user_responses, total=total)

