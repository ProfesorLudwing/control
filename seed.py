"""
Script de inicialización: crea las tablas y carga los datos base.
Se corre UNA SOLA VEZ:  python seed.py

Si ya existen los datos, no los duplica (es idempotente).
"""

from db import Base, engine, SessionLocal
from models import Grupo, Tema, Progreso


# --- Datos base ------------------------------------------------------------

GRUPOS = ["3B", "3C", "3D", "3E"]

TEMAS = [
    (1,  "Web 1",  "Tierra Sistémica: Las Cuatro Esferas"),
    (2,  "Web 2",  "FluidoVital: Capas y Química del Aire y Agua"),
    (3,  "Web 3",  "Física de Fluidos: Presión, Densidad y Temp."),
    (4,  "Web 4",  "ClimaGlobal: Ciclo del Agua y Tiempo Atm."),
    (5,  "Web 5",  "Ecosistemas: Factores Bióticos y Abióticos"),
    (6,  "Web 6",  "Redes Tróficas y Flujo de Energía"),
    (7,  "Web 7",  "Ciclos Biogeoquímicos y Equilibrio"),
    (8,  "Web 8",  "CambioQuímico: Reacciones y Ecuaciones"),
    (9,  "Web 9",  "OxígenoTerrestre: Atmósfera Primitiva vs Actual"),
    (10, "Web 10", "QuímicaOxidante: Óxidos Básicos y Ácidos"),
    (11, "Web 11", "FotosíntesisGlobal: Captura de Carbono"),
    (12, "Web 12", "ClimaGlobal: Efecto Invernadero y Cambio Clim."),
    (13, "Web 13", "DeterioroLocal: Deforestación y Contaminación"),
    (14, "Web 14", "IngEco: Restauración y Tecnologías Verdes"),
]


# --- Lógica de inicialización ---------------------------------------------

def crear_tablas():
    """Crea avance.db y las tablas si no existen."""
    Base.metadata.create_all(bind=engine)
    print("OK: tablas creadas (o ya existían).")


def cargar_grupos(session):
    """Inserta los grupos si no están ya en la base."""
    nuevos = 0
    for nombre in GRUPOS:
        existe = session.query(Grupo).filter_by(nombre=nombre).first()
        if not existe:
            session.add(Grupo(nombre=nombre))
            nuevos += 1
    session.commit()
    print(f"OK: grupos cargados ({nuevos} nuevos de {len(GRUPOS)}).")


def cargar_temas(session):
    """Inserta los temas si no están ya en la base."""
    nuevos = 0
    for orden, web_nombre, titulo in TEMAS:
        existe = session.query(Tema).filter_by(orden=orden).first()
        if not existe:
            session.add(Tema(orden=orden, web_nombre=web_nombre, titulo=titulo))
            nuevos += 1
    session.commit()
    print(f"OK: temas cargados ({nuevos} nuevos de {len(TEMAS)}).")


def cargar_progreso_inicial(session):
    """Crea un registro 'pendiente' por cada combinación grupo × tema."""
    grupos = session.query(Grupo).all()
    temas = session.query(Tema).all()

    nuevos = 0
    for grupo in grupos:
        for tema in temas:
            existe = (
                session.query(Progreso)
                .filter_by(grupo_id=grupo.id, tema_id=tema.id)
                .first()
            )
            if not existe:
                session.add(Progreso(
                    grupo_id=grupo.id,
                    tema_id=tema.id,
                    estado="pendiente",
                ))
                nuevos += 1
    session.commit()
    print(f"OK: registros de progreso creados ({nuevos} nuevos).")


def main():
    print("Iniciando seed...")
    crear_tablas()

    session = SessionLocal()
    try:
        cargar_grupos(session)
        cargar_temas(session)
        cargar_progreso_inicial(session)
    finally:
        session.close()

    print("Seed completo.")


if __name__ == "__main__":
    main()