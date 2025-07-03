from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
import json

# Configuración para usar PostgreSQL si está disponible, o JSON como fallback
# Usar variable de entorno DATABASE_URL para producción (Render)
DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://jhan:u3K3hYwGIEOdtNKeWnuIHVtJYNz5XE85@dpg-d1j2o5adbo4c73c270m0-a/ferreteria_6bx4")

# Render usa postgres:// pero SQLAlchemy requiere postgresql://
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# Intentar crear el motor de base de datos
try:
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base = declarative_base()
    print("Conexión a PostgreSQL establecida correctamente")
    USE_DB = True
except Exception as e:
    print(f"Error al conectar a PostgreSQL: {e}")
    print("Usando almacenamiento JSON como fallback")
    USE_DB = False

# Función para obtener una sesión de base de datos
def get_db():
    if USE_DB:
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()
    else:
        yield None

# Funciones para trabajar con JSON como fallback
def get_json_data(file_name):
    """Obtiene datos desde un archivo JSON"""
    file_path = os.path.join("data", file_name)
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_json_data(file_name, data):
    """Guarda datos en un archivo JSON"""
    os.makedirs("data", exist_ok=True)
    file_path = os.path.join("data", file_name)
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)