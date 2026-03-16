from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime
from fastapi import Request
from ..database import get_db
from .. import models, schemas
import json
from app.schemas import PatientBase, PatientCreate, PhoneLookup
import logging
logger = logging.getLogger("patient-api")

router = APIRouter(prefix="/patients", tags=["patients"])


@router.post("/")
async def create_patient(request: Request, patient: schemas.PatientCreate, db: Session = Depends(get_db)):

    logger.info(f"SAVING NEW PATIENT TO DB: {patient.model_dump()}")

    new_patient = models.Patient(**patient.model_dump())

    db.add(new_patient)
    db.commit()
    db.refresh(new_patient)
    logger.info(f"DATABASE SUCCESS: Created ID {new_patient.patient_id}")

    return new_patient



@router.get("/")
def list_patients(
    last_name: Optional[str] = None,
    phone_number: Optional[str] = None,
    date_of_birth: Optional[str] = None,
    db: Session = Depends(get_db)
):

    query = db.query(models.Patient).filter(models.Patient.deleted_at == None)

    if last_name:
        query = query.filter(models.Patient.last_name == last_name)

    if phone_number:
        query = query.filter(models.Patient.phone_number == phone_number)

    if date_of_birth:
        query = query.filter(models.Patient.date_of_birth == date_of_birth)

    patients = query.all()

    return {
        "data": patients,
        "error": None
    }


@router.get("/{patient_id}")
def get_patient(patient_id: str, db: Session = Depends(get_db)):

    patient = db.query(models.Patient).filter(
        models.Patient.patient_id == patient_id,
        models.Patient.deleted_at == None
    ).first()

    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    return {
        "data": patient,
        "error": None
    }


import logging
import json

# Ensuring this name matches the logger configured in my main.py
logger = logging.getLogger("patient-api")

@router.put("/{patient_id}", status_code=200)
def update_patient(
    patient_id: str,
    patient_update: schemas.PatientUpdate,
    db: Session = Depends(get_db)
):
    # --- LOG THE PAYLOAD ---
    # Captures the raw data received from Vapi/User
    logger.info(f"INCOMING PUT PAYLOAD FOR {patient_id}: {patient_update.model_dump_json()}")
    # -----------------------

    patient = db.query(models.Patient).filter(
        models.Patient.patient_id == patient_id,
        models.Patient.deleted_at.is_(None)
    ).first()

    if not patient:
        logger.warning(f"Update failed: Patient {patient_id} not found.")
        raise HTTPException(status_code=404, detail="Patient not found")

    update_data = patient_update.model_dump(exclude_unset=True)

    # prevent overwriting with empty strings
    update_data = {k: v for k, v in update_data.items() if v not in ["", None]}

    if not update_data:
        logger.warning(f"Update aborted: No valid fields provided for {patient_id}")
        raise HTTPException(
            status_code=400,
            detail="No valid fields provided for update"
        )

    for key, value in update_data.items():
        setattr(patient, key, value)

    db.commit()
    db.refresh(patient)

    logger.info(f"SUCCESS: Patient {patient_id} updated in database.")

    return {
        "data": patient,
        "error": None
    }


@router.delete("/{patient_id}")
def delete_patient(patient_id: str, db: Session = Depends(get_db)):

    patient = db.query(models.Patient).filter(
        models.Patient.patient_id == patient_id,
        models.Patient.deleted_at == None
    ).first()

    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    patient.deleted_at = datetime.utcnow()

    db.commit()

    return {
        "data": "Patient deleted successfully",
        "error": None
    }


@router.post("/check-patient")
def check_patient(payload: PhoneLookup, db: Session = Depends(get_db)):

    patient = db.query(models.Patient).filter(
    models.Patient.phone_number == payload.phone_number,
    models.Patient.deleted_at == None
    ).first()

    if patient:
        return {
            "data": {
                "exists": True,
                "first_name": patient.first_name,
                "last_name": patient.last_name,
                "patient_id": patient.patient_id
            },
            "error": None
        }

    return {
        "data": {
            "exists": False
        },
        "error": None
    }