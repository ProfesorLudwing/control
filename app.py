"""
App de control de avance — CNEyT III
Corre con:  streamlit run app.py
"""

import streamlit as st

from db import SessionLocal
from models import Grupo, Tema, Progreso

from exportar_html import generar_html

# ============================================================
# Configuración de la página
# ============================================================
st.set_page_config(
    page_title="Control de Avance CNEyT III",
    page_icon="📚",
    layout="wide",
)

# --- Botón de exportar HTML (vista móvil) ---
with st.expander("📥 Exportar vista para celular", expanded=False):
    st.caption(
        "Genera un archivo HTML de solo lectura con el avance de los 4 grupos. "
        "Ábrelo en el navegador del celular."
    )
    if st.button("Generar HTML", key="btn_generar_html"):
        st.session_state["html_listo"] = True

    if st.session_state.get("html_listo"):
        html_str = generar_html()
        st.download_button(
            label="⬇️ Descargar avance_vista.html",
            data=html_str,
            file_name="avance_vista.html",
            mime="text/html",
            key="btn_descargar_html",
        )
# ============================================================
# Helpers de base de datos
# ============================================================

def get_grupos():
    s = SessionLocal()
    try:
        return s.query(Grupo).order_by(Grupo.nombre).all()
    finally:
        s.close()


def get_temas_con_progreso(grupo_id):
    s = SessionLocal()
    try:
        filas = (
            s.query(Tema, Progreso)
            .join(Progreso, Progreso.tema_id == Tema.id)
            .filter(Progreso.grupo_id == grupo_id)
            .order_by(Tema.orden)
            .all()
        )
        return [
            {
                "tema_id": t.id,
                "orden": t.orden,
                "web": t.web_nombre,
                "titulo": t.titulo,
                "estado": p.estado,
                "resumen_clase": p.resumen_clase,
                "tarea_asignada": p.tarea_asignada,
            }
            for t, p in filas
        ]
    finally:
        s.close()


def actualizar_estado(grupo_id, tema_id, nuevo_estado):
    s = SessionLocal()
    try:
        p = s.query(Progreso).filter_by(grupo_id=grupo_id, tema_id=tema_id).first()
        if p:
            p.estado = nuevo_estado
            s.commit()
    finally:
        s.close()


def toggle_subactividad(grupo_id, tema_id, campo):
    """Alterna True/False en resumen_clase o tarea_asignada."""
    s = SessionLocal()
    try:
        p = s.query(Progreso).filter_by(grupo_id=grupo_id, tema_id=tema_id).first()
        if p:
            setattr(p, campo, not getattr(p, campo))
            s.commit()
    finally:
        s.close()


# ============================================================
# Encabezado
# ============================================================
st.title("📚 Control de Avance — CNEyT III")
st.caption("Nuestro hogar: El sistema terrestre · CBTIS 303")


# ============================================================
# Selector de grupo
# ============================================================
grupos = get_grupos()

if not grupos:
    st.error("No hay grupos en la base de datos. Corre `python seed.py` primero.")
    st.stop()

nombres_grupos = [g.nombre for g in grupos]
grupo_seleccionado = st.selectbox("Selecciona el grupo", nombres_grupos)
grupo = next(g for g in grupos if g.nombre == grupo_seleccionado)


# ============================================================
# Cargar temas del grupo
# ============================================================
temas = get_temas_con_progreso(grupo.id)

vistos = sum(1 for t in temas if t["estado"] != "pendiente")
total = len(temas)
siguiente = next((t for t in temas if t["estado"] == "pendiente"), None)


# ============================================================
# Panel de resumen
# ============================================================
col_izq, col_der = st.columns([2, 1])

with col_izq:
    st.subheader(f"{grupo.nombre} — {vistos} de {total} temas vistos")

with col_der:
    if siguiente:
        st.info(
            f"**Siguiente:** Tema {siguiente['orden']}  \n"
            f"{siguiente['web']} — {siguiente['titulo']}"
        )
    else:
        st.success("🎉 Todos los temas vistos")

st.divider()


# ============================================================
# Lista de temas
# ============================================================
for t in temas:
    estado = t["estado"]
    es_siguiente = siguiente and t["tema_id"] == siguiente["tema_id"]

    if estado == "visto_presencial":
        bg, color_texto, etiqueta = "#28a745", "white", "VISTO EN CLASE"
    elif estado == "visto_auto":
        bg, color_texto, etiqueta = "#87CEEB", "black", "AUTOEVALUADO"
    elif es_siguiente:
        bg, color_texto, etiqueta = "#FFA500", "white", "SIGUIENTE"
    else:
        bg, color_texto, etiqueta = "#E0E0E0", "#555", "PENDIENTE"

    # --- Fila 1: título + botones principales ---
    c_titulo, c_clase, c_auto, c_reset = st.columns([6, 1, 1, 1])

    with c_titulo:
        st.markdown(
            f"""
            <div style="
                background-color:{bg};
                color:{color_texto};
                padding:10px 14px;
                border-radius:6px;
                font-weight:500;
                line-height:1.3em;
            ">
                <b>{t['web']}</b> — {t['titulo']}
                <span style="float:right; font-size:0.75em; opacity:0.85;">
                    {etiqueta}
                </span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c_clase:
        if st.button("🟩 Clase", key=f"clase_{t['tema_id']}", use_container_width=True):
            actualizar_estado(grupo.id, t["tema_id"], "visto_presencial")
            st.rerun()

    with c_auto:
        if st.button("🟦 Auto", key=f"auto_{t['tema_id']}", use_container_width=True):
            actualizar_estado(grupo.id, t["tema_id"], "visto_auto")
            st.rerun()

    with c_reset:
        if st.button(
            "↺",
            key=f"reset_{t['tema_id']}",
            use_container_width=True,
            disabled=(estado == "pendiente"),
            help="Regresar a pendiente (conserva subactividades)",
        ):
            actualizar_estado(grupo.id, t["tema_id"], "pendiente")
            st.rerun()

    # --- Fila 2: subactividades (solo si el tema está visto) ---
    if estado != "pendiente":
        c1, c2, c3, c4 = st.columns([6, 1, 1, 1])

        # Columna 1 vacía (indentación)
        # Columna 4 vacía (espacio)

        if estado == "visto_presencial":
            with c2:
                texto = "✅ Resumen" if t["resumen_clase"] else "☐ Resumen"
                if st.button(
                    texto,
                    key=f"res_{t['tema_id']}",
                    use_container_width=True,
                    help="Resumen construido en el pizarrón entre todos",
                ):
                    toggle_subactividad(grupo.id, t["tema_id"], "resumen_clase")
                    st.rerun()

        with c3:
            texto = "✅ Tarea" if t["tarea_asignada"] else "☐ Tarea"
            if st.button(
                texto,
                key=f"tar_{t['tema_id']}",
                use_container_width=True,
                help="Ya se encargó la tarea para que aborden el tema en casa",
            ):
                toggle_subactividad(grupo.id, t["tema_id"], "tarea_asignada")
                st.rerun()

    # Separación entre temas
    st.markdown("<div style='margin-bottom:6px'></div>", unsafe_allow_html=True)