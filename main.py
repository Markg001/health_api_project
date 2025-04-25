# This is the entry point  for the app
#Creates the webAPI and adds routes like:m POST /program/, POST /clients/ 
#uses model +schemas to do this

from fastapi import FastAPI, Depends, HTTPException, Header, Security
from sqlalchemy.orm import Session
import models, schemas
from database import engine, SessionLocal, Base
from fastapi.security.api_key import APIKeyHeader

API_KEY = "supersecretkey"
API_KEY_NAME = "x-api-key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid or missing API Key")


app = FastAPI()

# Create the tables
Base.metadata.create_all(bind=engine)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/programs/")
def create_program(
    program: schemas.HealthProgramCreate,
    db: Session = Depends(get_db),
    _: str = Depends(verify_api_key)
):
    db_program = models.HealthProgram(**program.dict())
    db.add(db_program)
    db.commit()
    db.refresh(db_program)
    return db_program


@app.post("/clients/")
def register_client(
    client: schemas.ClientCreate,
    db: Session = Depends(get_db),
    _: str = Depends(verify_api_key)
):
    db_client = models.Client(**client.dict())
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client


@app.post("/clients/{client_id}/enroll/")
def enroll_client_in_program(
    client_id: int,
    program_id: int,
    db: Session = Depends(get_db),
    _: str = Depends(verify_api_key)
):
    client = db.query(models.Client).filter(models.Client.id == client_id).first()
    program = db.query(models.HealthProgram).filter(models.HealthProgram.id == program_id).first()

    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    if not program:
        raise HTTPException(status_code=404, detail="Program not found")

    client.program_id = program_id
    db.commit()
    db.refresh(client)
    return client

