from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from models import Estudiante, Carrera, Base
from config import SessionLocal, engine
from typing import List
from pydantic import BaseModel
from datetime import datetime

app = FastAPI()

class EstudianteModel(BaseModel):
    id_estudiante: str
    nombre: str
    fecha_nacimiento: str
    email: str
    id_carrera: str

class CarreraModel(BaseModel):
    id_carrera: str
    nombre_carrera: str

@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)

def get_db():
    db_session = SessionLocal()
    try:
        yield db_session
    finally:
        db_session.close()

@app.get("/estudiantes", response_model=List[EstudianteModel])
def get_estudiantes(db: Session = Depends(get_db)):
    estudiantes = db.query(Estudiante).all()
    return [
        EstudianteModel(
            id_estudiante=e.id_estudiante,
            nombre=e.nombre,
            fecha_nacimiento=e.fecha_nacimiento.strftime('%Y-%m-%d'),  # Convertir a string
            email=e.email,
            id_carrera=e.id_carrera
        ) for e in estudiantes
    ]

@app.post("/estudiantes", response_model=str)
def add_estudiante(estudiante: EstudianteModel, db: Session = Depends(get_db)):
    # Convertir la cadena de fecha a datetime
    fecha_nacimiento = datetime.strptime(estudiante.fecha_nacimiento, '%Y-%m-%d').date()
    
    # Verificar si la carrera existe
    carrera_existente = db.query(Carrera).filter(Carrera.id_carrera == estudiante.id_carrera).first()
    if not carrera_existente:
        raise HTTPException(status_code=404, detail="Carrera no encontrada")
    
    nuevo_estudiante = Estudiante(
        id_estudiante=estudiante.id_estudiante,
        nombre=estudiante.nombre,
        fecha_nacimiento=fecha_nacimiento,  # Almacenar como datetime
        email=estudiante.email,
        id_carrera=estudiante.id_carrera
    )
    
    db.add(nuevo_estudiante)
    db.commit()
    return "Estudiante creado con éxito!"

@app.get("/estudiantes/{id_estudiante}", response_model=EstudianteModel)
def get_estudiante(id_estudiante: str, db: Session = Depends(get_db)):
    estudiante = db.query(Estudiante).filter(Estudiante.id_estudiante == id_estudiante).first()
    if not estudiante:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    return EstudianteModel(
        id_estudiante=estudiante.id_estudiante,
        nombre=estudiante.nombre,
        fecha_nacimiento=estudiante.fecha_nacimiento.strftime('%Y-%m-%d'),  # Convertir a string
        email=estudiante.email,
        id_carrera=estudiante.id_carrera
    )

@app.put("/estudiantes/{id_estudiante}", response_model=EstudianteModel)
def update_estudiante(id_estudiante: str, estudiante: EstudianteModel, db: Session = Depends(get_db)):
    estudiante_db = db.query(Estudiante).filter(Estudiante.id_estudiante == id_estudiante).first()
    if not estudiante_db:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    
    # Actualizar solo los campos proporcionados
    estudiante_db.nombre = estudiante.nombre
    estudiante_db.fecha_nacimiento = datetime.strptime(estudiante.fecha_nacimiento, '%Y-%m-%d').date()
    estudiante_db.email = estudiante.email
    estudiante_db.id_carrera = estudiante.id_carrera
    
    db.commit()
    db.refresh(estudiante_db)
    return EstudianteModel(
        id_estudiante=estudiante_db.id_estudiante,
        nombre=estudiante_db.nombre,
        fecha_nacimiento=estudiante_db.fecha_nacimiento.strftime('%Y-%m-%d'),
        email=estudiante_db.email,
        id_carrera=estudiante_db.id_carrera
    )

@app.delete("/estudiantes/{id_estudiante}")
def delete_estudiante(id_estudiante: str, db: Session = Depends(get_db)):
    estudiante = db.query(Estudiante).filter(Estudiante.id_estudiante == id_estudiante).first()
    if not estudiante:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    
    db.delete(estudiante)
    db.commit()
    return {"message": "Estudiante eliminado"}

# Endpoints para Carreras
@app.get("/carreras", response_model=List[CarreraModel])
def get_carreras(db: Session = Depends(get_db)):
    carreras = db.query(Carrera).all()
    return [CarreraModel(**c.__dict__) for c in carreras]

@app.post("/carreras", response_model=CarreraModel)
def create_carrera(carrera: CarreraModel, db: Session = Depends(get_db)):
    new_carrera = Carrera(**carrera.dict())
    db.add(new_carrera)
    db.commit()
    db.refresh(new_carrera)
    return CarreraModel(**new_carrera.__dict__)

@app.get("/carreras/{id_carrera}", response_model=CarreraModel)
def get_carrera(id_carrera: str, db: Session = Depends(get_db)):
    carrera = db.query(Carrera).filter(Carrera.id_carrera == id_carrera).first()
    if not carrera:
        raise HTTPException(status_code=404, detail="Carrera no encontrada")
    return CarreraModel(**carrera.__dict__)

@app.put("/carreras/{id_carrera}", response_model=CarreraModel)
def update_carrera(id_carrera: str, carrera: CarreraModel, db: Session = Depends(get_db)):
    carrera_db = db.query(Carrera).filter(Carrera.id_carrera == id_carrera).first()
    if not carrera_db:
        raise HTTPException(status_code=404, detail="Carrera no encontrada")
    
    carrera_db.nombre_carrera = carrera.nombre_carrera
    db.commit()
    db.refresh(carrera_db)
    return CarreraModel(**carrera_db.__dict__)

@app.delete("/carreras/{id_carrera}")
def delete_carrera(id_carrera: str, db: Session = Depends(get_db)):
    carrera = db.query(Carrera).filter(Carrera.id_carrera == id_carrera).first()
    if not carrera:
        raise HTTPException(status_code=404, detail="Carrera no encontrada")
    
    db.delete(carrera)
    db.commit()
    return {"message": "Carrera eliminada"}
