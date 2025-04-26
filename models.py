#This is the SQLAlchemy models
# Tells the app: "A client has a name,email and belongs to a program"

from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from database import Base

# Middle table (association table)
client_program_association = Table(
    'client_program_association',
    Base.metadata,
    Column('client_id', ForeignKey('clients.id'), primary_key=True),
    Column('program_id', ForeignKey('health_programs.id'), primary_key=True)
)

class HealthProgram(Base):
    __tablename__ = "health_programs"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    description = Column(String)

    clients = relationship(
        "Client",
        secondary=client_program_association,
        back_populates="programs"
    )

class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True)

    programs = relationship(
        "HealthProgram",
        secondary=client_program_association,
        back_populates="clients"
    )
