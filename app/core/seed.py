from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import AsyncSessionLocal
from app.models.department import Department


# Static departments to seed
STATIC_DEPARTMENTS = [
    "HR",
    "Engineering",
    "Quality Assurance",
    "Marketing"
]


async def seed_departments():
    """
    Seed static departments into the database.
    Only creates departments that don't already exist.
    """
    async with AsyncSessionLocal() as session:
        try:
            # Get existing departments
            result = await session.execute(select(Department))
            existing_departments = {dept.department_name for dept in result.scalars().all()}
            
            # Create departments that don't exist
            departments_to_create = [
                Department(department_name=dept_name)
                for dept_name in STATIC_DEPARTMENTS
                if dept_name not in existing_departments
            ]
            
            if departments_to_create:
                session.add_all(departments_to_create)
                await session.commit()
                print(f"✓ Seeded {len(departments_to_create)} department(s)")
            else:
                print("✓ All departments already exist")
                
        except Exception as e:
            await session.rollback()
            print(f"✗ Error seeding departments: {e}")
            raise

