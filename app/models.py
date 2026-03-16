import uuid
from sqlalchemy import Column, String, Date, DateTime
from sqlalchemy.sql import func
from .database import Base
from sqlalchemy import DateTime


class Patient(Base):
    __tablename__ = "patients"

    patient_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))

    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)

    date_of_birth = Column(String(50), nullable=False)
    sex = Column(String(20), nullable=False)

    phone_number = Column(String(50), nullable=False)

    email = Column(String(100))

    address_line_1 = Column(String(200), nullable=False)
    address_line_2 = Column(String(200))

    city = Column(String(100), nullable=False)
    state = Column(String(100), nullable=False)
    zip_code = Column(String(10), nullable=False)

    insurance_provider = Column(String(100))
    insurance_member_id = Column(String(100))

    preferred_language = Column(String(50), default="English")

    emergency_contact_name = Column(String(100))
    emergency_contact_phone = Column(String(50))

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    deleted_at = Column(DateTime, nullable=True)