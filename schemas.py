#This is for Data structure (Response/Request)
#Tells FastAPI : "When someone send as data, this is what it should look like"
from pydantic import BaseModel
from typing import List, Optional

class HealthProgramCreate(BaseModel):
    name: str
    description: str

class ClientCreate(BaseModel):
    name: str
    email: str
    program_ids: Optional[List[int]] = []  # Allow multiple programs

class Enrollment(BaseModel):
    program_ids: List[int]  # List of program IDs to enroll the client in
