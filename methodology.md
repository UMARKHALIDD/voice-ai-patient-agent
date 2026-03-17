METHODOLOGY AND SYSTEM DESIGN

This document explains the architecture, implementation approach, and design decisions used to build the Voice AI Patient Registration System.

The goal of this system is to allow patients to register with a clinic through a phone call, where an AI voice assistant collects the required information conversationally and stores it in a database via API calls.

SYSTEM OVERVIEW

The system consists of five main components:

Phone Call Interface

Voice AI Assistant

Backend API

Database

Admin Dashboard 



SYSTEM FLOW:

Caller
   ↓
Phone Call
   ↓
Twilio / Vapi Phone Number
   ↓
Voice AI Assistant
   ↓
Speech-to-Text
   ↓
LLM Conversation Logic
   ↓
Tool Calls (API Requests)
   ↓
FastAPI Backend
   ↓
MySQL Database
   ↓
Streamlit Admin Dashboard




VOICE INFRASTRUCTURE

The voice interface is implemented using Vapi, which provides:

Speech-to-Text (STT)

Text-to-Speech (TTS)

Conversation orchestration

Tool calling support

A phone number was provisioned and connected to the Vapi assistant. When a user calls this number:

The call is received by the Vapi assistant

User speech is converted to text

The LLM processes the request

When necessary, the assistant triggers backend API tools

The backend processes the request and returns a response

AI ASSISTANT DESIGN

The assistant is configured using a system prompt that defines its behavior. The assistant performs the following tasks:

Collect patient information conversationally, Validate user input, Check if the patient already exists, Register a new patient or update an existing one, Confirm details before database insertion

The assistant collects information in a structured conversation flow rather than asking for all information at once.

SYSTEM PROMPT BEHAVIOUR

The assistant follows these key rules:

1. Collect Basic Information First

The assistant begins by collecting:

first_name

last_name

phone_number

This information is collected first because the phone number is used to determine whether the patient already exists.

2. Check Existing Patient

After collecting the phone number, the assistant calls the tool:

check_patient

The backend checks whether a patient already exists using the phone number.

Possible responses:

exists = true
exists = false

3. Existing Patient Handling

If the patient already exists, the assistant asks:

"It looks like we already have a record for [First Name] [Last Name]. Would you like to update your information instead?"

Two possible flows occur:

If user says YES

The assistant collects updated fields and calls:

update_patient

The patient record is updated using the returned patient_id.

If user says NO

The assistant politely ends the call.

4. New Patient Registration

If the patient does not exist, the assistant continues collecting the required fields:

date_of_birth, sex, address_line_1 ,city, state, zip_code

OPTIONAL INFORMATION COLLECTION

After collecting required fields, the assistant offers to collect optional information.

Optional fields include:

email, address_line_2, insurance_provider, insurance_member_id, preferred_language, emergency_contact_name, emergency_contact_phone

The assistant asks:

"Would you like to provide this optional information, or proceed with registration?"

If the user declines, registration continues without optional fields.

INPUT VALIDATION

The assistant performs conversational validation before calling backend APIs.

PHONE NUMBER VALIDATION

The assistant ensures the phone number contains 10–11 digits.

If the user provides an invalid phone number:

Example:

"123"

The assistant asks the user again for a valid phone number.

DATE OF BIRTH VALIDATION

The assistant ensures:

Date of birth is not in the future

If a future date is detected, the assistant requests a valid date.

TOOL ARCHITECTURE:

The system uses three backend tools exposed as API endpoints.

1) Check Patient Tool

Purpose:

Determine whether a patient already exists.

Endpoint:

POST /patients/check-patient

Input:

phone_number

Response:

{
  "data": {
     "exists": true,
     "first_name": "...",
     "last_name": "...",
     "patient_id": "..."
  },
  "error": null
}

This response determines the next conversation path.

2) Register Patient Tool

Purpose:

Create a new patient record.

Endpoint:

POST /patients

The assistant calls this tool after:

collecting required fields, collecting optional fields (if provided), confirming all information with the user.

3) Update Patient Tool

Purpose:

Update an existing patient record.

Endpoint:

PUT /patients/{patient_id}

This tool is used only if the patient already exists and the user agrees to update their information.

UPDATE LOGIC

The update API supports partial updates.

The backend uses:

exclude_unset=True

This ensures that only fields provided by the assistant are updated.

Example:

If the user only updates the ZIP code:

{
  "zip_code": "90591"
}

Only the ZIP code will be modified.

This prevents accidental overwriting of existing fields.

DATABASE DESIGN

The system uses MySQL with SQLAlchemy ORM.

The database stores patient information including:

personal details

contact information

insurance information

emergency contacts

The system also implements soft deletion using:

deleted_at

Soft-deleted records are ignored in:

check_patient queries

update operations

Observability

To ensure transparency and debugging capability, the system logs:

API requests from the voice agent and final payloads received from the assistant

Logs are written to:

agent_interactions.log

This allows easy inspection of agent behavior during calls.

Admin Dashboard

A Streamlit dashboard is included for administrators.

The dashboard allows administrators to:

view patient records, monitor new registrations, verify updates.

Due to ngrok free-tier limitations, the dashboard runs locally.

A demo video is included to demonstrate:

DEMO VIDEO LINK : https://drive.google.com/drive/folders/10maSoIZlRiAmBa5FfTopx0X7zP6Hl00Z?usp=sharing

voice registration

real-time database updates

dashboard updates




Summary

The system successfully demonstrates:

End-to-end voice-based patient registration

Conversational AI workflow

Tool-based API integration

Database-backed patient records

Real-time admin monitoring

The architecture is designed to be modular, extensible, and production-ready, allowing additional clinic workflows to be added easily in the future.