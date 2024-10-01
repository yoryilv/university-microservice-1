from sqlalchemy import Column, String, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

# Define la clase base
Base = declarative_base()

class Carrera(Base):
    __tablename__ = 'Carreras'
    id_carrera = Column(String(12), primary_key=True)
    nombre_carrera = Column(String(100), nullable=False)

class Estudiante(Base):
    __tablename__ = 'Estudiantes'
    id_estudiante = Column(String(12), primary_key=True)
    nombre = Column(String(100), nullable=False)
    fecha_nacimiento = Column(Date, nullable=False)
    email = Column(String(100), nullable=False)
    id_carrera = Column(String(12), ForeignKey('Carreras.id_carrera'))

    carrera = relationship("Carrera", backref="estudiantes")
