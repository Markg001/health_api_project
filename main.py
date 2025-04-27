# This is the entry point  for the app
#Creates the webAPI and adds routes like:m POST /program/, POST /clients/ 
#uses model +schemas to do this

from fastapi import FastAPI, Depends, HTTPException, Header, Security
from sqlalchemy.orm import Session
import models, schemas
from database import engine, SessionLocal, Base
from fastapi.security.api_key import APIKeyHeader
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

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

@app.get("/programs/")
def list_programs(db: Session = Depends(get_db)):
    programs = db.query(models.HealthProgram).all()
    return programs


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
    db_client = models.Client(**client.dict(exclude={"program_ids"}))
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client


@app.post("/clients/{client_id}/enroll/")
def enroll_client_in_program(
    client_id: int,
    enrollment: schemas.Enrollment,  # Expect an array of program IDs
    db: Session = Depends(get_db),
    _: str = Depends(verify_api_key)
):
    client = db.query(models.Client).filter(models.Client.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    # Enroll client in multiple programs
    programs = db.query(models.HealthProgram).filter(models.HealthProgram.id.in_(enrollment.program_ids)).all()
    if not programs:
        raise HTTPException(status_code=404, detail="Programs not found")

    client.programs.extend(programs)  # Add selected programs to the client's relationship
    db.commit()
    db.refresh(client)
    return client


@app.get("/clients/")
def get_clients(db: Session = Depends(get_db), _: str = Depends(verify_api_key)):
    clients = db.query(models.Client).all()
    return clients


@app.get("/clients/{client_id}")
def get_client_profile(client_id: int, db: Session = Depends(get_db), _: str = Depends(verify_api_key)):
    client = db.query(models.Client).filter(models.Client.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    return client  # This will return the client and the related programs via the relationship

# Allow your frontend (localhost or wherever you host)
origins = [
    "http://localhost:5500",  # If you're serving your HTML with Live Server extension
    "http://127.0.0.1:5500",  # Another possible localhost address
    "http://localhost",       # Optional
    "http://127.0.0.1"         # Optional
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,            # Frontend allowed
    allow_credentials=True,
    allow_methods=["*"],              # Allow all methods (GET, POST, OPTIONS etc.)
    allow_headers=["*"],              # Allow all headers (x-api-key etc.)
)

# Serve the 'Frontend' folder as static files
app.mount("/static", StaticFiles(directory="Frontend"), name="static")

# Serve index.html when visiting the root `/`
@app.get("/", response_class=FileResponse)
async def read_index():
    return "Frontend/index.html"