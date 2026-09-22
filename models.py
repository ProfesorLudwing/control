from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from db import Base


class Grupo(Base):
    __tablename__ = "grupos"

    id = Column(Integer, primary_key=True)
    nombre = Column(String(10), unique=True, nullable=False)   # "3B", "3C", "3D", "3E"

    # Relación: un grupo tiene muchos registros de progreso
    progresos = relationship("Progreso", back_populates="grupo", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Grupo {self.nombre}>"


class Tema(Base):
    __tablename__ = "temas"

    id = Column(Integer, primary_key=True)
    orden = Column(Integer, unique=True, nullable=False)       # 1, 2, 3, ... 14
    titulo = Column(String(200), nullable=False)               # "Tierra Sistémica: Las Cuatro Esferas"
    web_nombre = Column(String(100), nullable=False)           # "Web 1", "Web 2", ...

    # Relación: un tema aparece en muchos registros de progreso
    progresos = relationship("Progreso", back_populates="tema", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Tema {self.orden}: {self.titulo}>"


class Progreso(Base):
    __tablename__ = "progreso"

    id = Column(Integer, primary_key=True)
    grupo_id = Column(Integer, ForeignKey("grupos.id"), nullable=False)
    tema_id = Column(Integer, ForeignKey("temas.id"), nullable=False)

    # Estado del tema para ese grupo:
    #   "pendiente"        -> aún no lo ve
    #   "visto_presencial" -> lo vieron en clase (verde)
    #   "visto_auto"       -> lo vieron por su cuenta (azul cielo)
    estado = Column(String(20), nullable=False, default="pendiente")

    # Relaciones inversas
    grupo = relationship("Grupo", back_populates="progresos")
    tema = relationship("Tema", back_populates="progresos")

    # Un grupo no puede tener dos registros del mismo tema
    __table_args__ = (
        UniqueConstraint("grupo_id", "tema_id", name="uq_grupo_tema"),
    )

    def __repr__(self):
        return f"<Progreso grupo={self.grupo_id} tema={self.tema_id} estado={self.estado}>"