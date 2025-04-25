#This is for Data structure (Response/Request)
from pydantic import BaseModel

class HealthProgramCreate(BaseModel):
    name: str
    description: str

class ClientCreate(BaseModel):
    name: str
    email: str
    program_id: int
