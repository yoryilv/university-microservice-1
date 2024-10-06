from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Cambia los detalles de conexión por la IP elástica y credenciales correctas
DATABASE_URL = "mysql+mysqlclient://usuario:contraseña@IP_ELASTICA_AWS/nombre_bd"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
