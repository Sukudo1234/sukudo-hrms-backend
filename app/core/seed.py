from sqlalchemy import select, func, text
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import AsyncSessionLocal
from app.models.department import Department
from app.models.role import Role


# Static departments to seed
STATIC_DEPARTMENTS = [
    "Project Management",
    "Tech/Automation",
    "It",
    "HR & Administration",
    "Finance anf accounts",
    "Marketing and outreach",
    "Translation",
    "SRT",
    "Dubing",
    "Post Production and audio Enginering",
    "Quality control",
    "Factory"
]

# Static roles to seed
STATIC_ROLES = [
    "Admin",
    "Sub-admin",
    "HR",
    "Employee",
    "IT"
]


async def seed_departments():
    """
    Seed static departments into the database.
    Only seeds if the table is empty (one-time initialization).
    After seeding, departments should be managed through the API.
    """
    async with AsyncSessionLocal() as session:
        try:
            # Check if departments already exist
            result = await session.execute(select(func.count(Department.id)))
            count = result.scalar_one()
            
            if count > 0:
                print(f"✓ Departments already exist ({count} department(s)), skipping seed")
                return
            
            # Reset the sequence to start from 1 (only when seeding)
            await session.execute(text("ALTER SEQUENCE departments_id_seq RESTART WITH 1"))
            await session.commit()
            print("✓ Reset sequence to start from 1")
            
            # Create new departments
            departments_to_create = [
                Department(department_name=dept_name)
                for dept_name in STATIC_DEPARTMENTS
            ]
            
            session.add_all(departments_to_create)
            await session.commit()
            print(f"✓ Seeded {len(departments_to_create)} department(s)")
                
        except Exception as e:
            await session.rollback()
            print(f"✗ Error seeding departments: {e}")
            raise


async def seed_roles():
    """
    Seed static roles into the database.
    Only seeds if the table is empty (one-time initialization).
    After seeding, roles should be managed through the API.
    """
    async with AsyncSessionLocal() as session:
        try:
            # Check if roles already exist
            result = await session.execute(select(func.count(Role.id)))
            count = result.scalar_one()
            
            if count > 0:
                print(f"✓ Roles already exist ({count} role(s)), skipping seed")
                return
            
            # Reset the sequence to start from 1 (only when seeding)
            await session.execute(text("ALTER SEQUENCE roles_id_seq RESTART WITH 1"))
            await session.commit()
            print("✓ Reset roles sequence to start from 1")
            
            # Create new roles
            roles_to_create = [
                Role(user_role=role_name)
                for role_name in STATIC_ROLES
            ]
            
            session.add_all(roles_to_create)
            await session.commit()
            print(f"✓ Seeded {len(roles_to_create)} role(s)")
                
        except Exception as e:
            await session.rollback()
            print(f"✗ Error seeding roles: {e}")
            raise

