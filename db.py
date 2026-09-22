from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Ruta absoluta al archivo de la base de datos, dentro de la carpeta del proyecto
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "avance.db"

# SQLite necesita este formato de URL: sqlite:///ruta/al/archivo.db
DATABASE_URL = f"sqlite:///{DB_PATH}"

# Motor de conexión. check_same_thread=False es necesario para Streamlit.
engine = create_engine(DATABASE_URL, echo=False, connect_args={"check_same_thread": False})

# Fábrica de sesiones
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

# Clase base que heredarán los modelos (Grupo, Tema, Progreso)
Base = declarative_base()