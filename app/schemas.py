from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date


class PatientBase(BaseModel):
    first_name: str
    last_name: str
    date_of_birth: str
    sex: str

    phone_number: str
    email: Optional[str] = None

    address_line_1: str
    address_line_2: Optional[str] = None

    city: str
    state: str
    zip_code: str

    insurance_provider: Optional[str] = None
    insurance_member_id: Optional[str] = None

    preferred_language: Optional[str] = "English"

    emergency_contact_name: Optional[str] = None
    emergency_contact_phone: Optional[str] = None


class PatientCreate(PatientBase):
    pass


class PatientUpdate(BaseModel):
    # Add "= None" to make these truly optional in the request body
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    date_of_birth: Optional[str] = None
    sex: Optional[str] = None

    phone_number: Optional[str] = None
    email: Optional[str] = None

    address_line_1: Optional[str] = None
    address_line_2: Optional[str] = None

    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None

    insurance_provider: Optional[str] = None
    insurance_member_id: Optional[str] = None

    preferred_language: Optional[str] = "English"

    emergency_contact_name: Optional[str] = None
    emergency_contact_phone: Optional[str] = None

class PatientResponse(PatientBase):
    patient_id: str

    class Config:
        from_attributes = True




class PhoneLookup(BaseModel):
    phone_number: str