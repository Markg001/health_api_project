#This is the SQLAlchemy models

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class HealthProgram(Base):
    __tablename__ = "health_programs"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    description = Column(String)

    clients = relationship("Client", back_populates="program")

class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True)
    program_id = Column(Integer, ForeignKey("health_programs.id"))

    program = relationship("HealthProgram", back_populates="clients")
