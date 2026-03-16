Voice AI Patient Registration Agent

This project implements a voice-based patient registration system that allows patients to register with a medical clinic through a phone call. A conversational AI assistant collects patient information and stores/updates it in a database via a FastAPI backend.

The system also includes an admin dashboard that allows administrators to view patient records stored in the database.

Live Demo :

The system can be tested directly without running the code locally. Call the number below to interact with the AI patient registration assistant.

Phone Number : +1 646 439 9385

The assistant will collect patient details conversationally and store/updates them in the database.

API Base URL : https://confiding-wobbily-tiffanie.ngrok-free.dev/

API Documentation :

You can view the API documentation and test the APIs/ verify from the database on swagger after calling the agent by visiting the below link:
https://confiding-wobbily-tiffanie.ngrok-free.dev/docs

(These hosted apis are connected to my own running mysql database)



SYSTEM DESIGN :

Caller
   ↓
Phone Call
   ↓
Vapi Voice Assistant
   ↓
Speech-to-Text
   ↓
LLM Conversation Logic
   ↓
API Tool Calls (Decides whether to register a new patient or update the record if already existing based on provided phone number)
   ↓
FastAPI Backend 
   ↓
MySQL Database
   ↓
Streamlit Admin Dashboard





REPOSITORY STRUCTURE:

voice-ai-patient-agent
│
├── app/
│   │
│   ├── main.py
│   │   Entry point of the FastAPI application.
│   │   Initializes logging and registers API routers.
│   │
│   ├── database.py
│   │   Handles database connection setup using SQLAlchemy.
│   │   Reads the database URL from environment variable.
│   │
│   ├── models.py
│   │   Defines SQLAlchemy ORM model representing database table.
│   │
│   ├── schemas.py
│   │   Defines Pydantic schemas used for request validation
│   │   and API data structures.
│   │
│   └── routers/
│       └── patients.py
│           Contains API endpoints for:
│           - Registering patients
│           - Checking if a patient exists
│           - Updating patient information
│
├── dashboard/
│   │
│   └── dashboard.py
│       Streamlit admin dashboard that displays
│       patient records stored in the database.
│
├── requirements.txt
│   Python dependencies required to run the project.
│
├── README.md
│   Project documentation and instructions.
│
└── METHODOLOGY.md
    Explanation of design decisions, architecture,
    and implementation approach.



BACKEND API ENDPOINTS:

1) Register Patient: POST /patients ---> (Registers a new patient)
2) Check Existing Patient : POST /patients/check-patient ----> (Checks whether a patient already exists using their phone number.)
3) Update Patient : PUT /patients/{patient_id} ----> (Updates an existing patient record.Partial updates are supported.)
4) Delete Patient : Delete /patients/{patient_id} ---> soft deletes a patient from database
5) List Patient : GET /Patients ---> Lists patients from database based on Last name, phone number, date of birth filtering

OBSERVABILITY:

The system logs the final payload received from the voice agent for observability and debugging.

Logs include: Patient registration payloads, Patient update payloads, and all listing payloads.

Logs are written to: agent_interactions.log

---------------------------------------------------
---------------------------------------------------

RUNNING THE PROJECT LOCALLY

The instructions below are only required if you want to run the project locally.

The live demo can be tested using the phone number provided earlier.

1. Install Dependencies : pip install -r requirements.txt
2. Configure Environment Variables 

Create a .env file in the project root.

Example:

DATABASE_URL=mysql+pymysql://username:password@localhost:3306/voice_ai_patients

The application reads the database connection string from this variable.

3. Database Setup

The project uses SQLAlchemy ORM with Base.metadata.create_all().

This means the required database table will be automatically created when the application starts, provided the database exists.

Ensure the database exists in MySQL:

CREATE DATABASE voice_ai_patients;

4. Run the Backend Server

Start the FastAPI backend:

uvicorn app.main:app --reload

The backend will run at:

http://localhost:8000

Swagger documentation will be available at:

http://localhost:8000/docs


5. Run the Admin Dashboard

Start the Streamlit dashboard:

streamlit run dashboard/dashboard.py

The dashboard will run at:

http://localhost:8501 Which will be connected yto your mysql database and showing patient records if they exist in the table.

ADMIN DASHBOARD DEMONSTRATION:

The project includes a Streamlit-based admin dashboard that allows administrators to view patient records stored in the database. The dashboard displays the same data that the voice agent inserts or updates through the backend APIs.

Due to the ngrok free-tier limitation, only one public URL can be exposed at a time. Since the backend API must remain publicly accessible for the voice agent and external testing, the dashboard is currently running locally on port 8501 and is not publicly hosted.

To demonstrate the dashboard functionality, a video recording is attached with this submission showing:

The voice agent registering a patient via phone call.

The backend inserting the data into the database.

The Streamlit dashboard updating in real time to reflect the new patient record.

Even without the dashboard video, reviewers can still verify the system functionality by using the hosted API documentation on swagger.

You can confirm patient records directly through the hosted URL as provided earlier.

https://confiding-wobbily-tiffanie.ngrok-free.dev/docs

From there you can:

Retrieve patient records

Verify newly inserted records

Verify updates made through the voice agent

This ensures that all backend functionality remains fully testable through the hosted API endpoints even without the locally hosted dashboard.

