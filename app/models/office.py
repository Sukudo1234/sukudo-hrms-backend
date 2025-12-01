from sqlalchemy import Column, Integer, String, Boolean
from app.core.database import Base


class Office(Base):
    __tablename__ = "offices"

    id = Column(Integer, primary_key=True, index=True)
    office_name = Column(String, nullable=False)
    city = Column(String, nullable=False)
    country = Column(String, nullable=False)
    address = Column(String, nullable=True)
    remote = Column(Boolean, nullable=False, default=False)

