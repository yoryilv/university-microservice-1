from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base  # Importar Base desde models

DATABASE_URL = "mysql://root:Aloramdon1!@localhost:3306/sistema_universidad"

# Crea el motor de conexión
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)  # Crear todas las tablas
