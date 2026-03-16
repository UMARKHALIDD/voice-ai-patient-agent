import logging
import sys
import time
from fastapi import FastAPI, Request
from .database import Base, engine
from .routers import patients

# 1. Setup Logging - This handles BOTH terminal and file
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("agent_interactions.log"), # The persistent file 
        logging.StreamHandler(sys.stdout)             # current terminal printing
    ]
)
logger = logging.getLogger("patient-api")

app = FastAPI(title="Voice AI Patient Registration API")

@app.middleware("http")
async def log_requests(request: Request, call_next):
    # Consume body safely
    body_bytes = await request.body()
    
    # This keeps the body available for my actual API routes
    async def receive():
        return {"type": "http.request", "body": body_bytes}
    request._receive = receive

    # Capture the info for the terminal and the file
    method = request.method
    url = request.url
    body_str = body_bytes.decode("utf-8")

   
    logger.info("\n===== VAPI INTERACTION =====")
    logger.info(f"METHOD/URL: {method} {url}")
    if body_str:
        logger.info(f"PAYLOAD: {body_str}")
    logger.info("============================\n")

    response = await call_next(request)
    return response

# Database and Routers
Base.metadata.create_all(bind=engine)
app.include_router(patients.router)

@app.get("/")
def root():
    return {"message": "Voice AI Patient Registration API is running"}


# from fastapi import FastAPI, Request
# from .database import Base, engine
# from .routers import patients

# app = FastAPI(title="Voice AI Patient Registration API")
# @app.middleware("http")
# async def log_requests(request: Request, call_next):
#     body = await request.body()
#     print("\n===== RAW REQUEST =====")
#     print("URL:", request.url)
#     print("METHOD:", request.method)
#     print("BODY:", body.decode("utf-8"))
#     print("=======================\n")

#     response = await call_next(request)
#     return response

# Base.metadata.create_all(bind=engine)

# app.include_router(patients.router)



# @app.get("/")
# def root():
#     return {"message": "Voice AI Patient Registration API is running"}