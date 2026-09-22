import streamlit as st
import os

# Configuración del Pizarrón Escolar
st.set_page_config(page_title="De la Roca a la Vida", page_icon="🌍", layout="wide")

st.title("🌍 De la Roca a la Vida: Litosfera, Pedosfera y Biosfera")
st.markdown("### CBTIS 303 | Ciencias Naturales, Experimentales y Tecnología III")
st.write("Explora las capas que conectan la geología con la vida. Cada subpestaña contiene su propia imagen e información específica.")

# --- RUTAS DE IMÁGENES ---
IMAGENES = {
    "Litosfera_Esquema": "litosfera_esquema.png",
    "Litosfera_Placas": "placas_tectonicas.jpg",
    "Litosfera_Tipos": "tipos_litosfera.png",
    "Pedosfera_Perfil": "pedosfera_perfil.png",
    "Pedosfera_Edafogenesis": "edafogenesis.jpg",
    "Biosfera_Esquema": "biosfera_esquema.png",
    "Biosfera_Fotosintesis": "fotosintesis.jpg",
    "Biosfera_Quimiosintesis": "quimiosintesis.png"
}

# --- BANCO DE PREGUNTAS ---
CUESTIONARIO = {
    "litosfera": [
        {
            "id": "lit1",
            "pregunta": "¿Qué capas componen la Litosfera?",
            "opciones": [
                "Corteza + manto superior rígido",
                "Corteza + manto completo",
                "Solo la corteza"
            ],
            "correcta": "Corteza + manto superior rígido",
            "pista": "Revisa la definición en la subpestaña 'Esquema General'."
        },
        {
            "id": "lit2",
            "pregunta": "¿Cuál es la diferencia principal entre la litosfera oceánica y la continental?",
            "opciones": [
                "La oceánica es más densa y delgada",
                "La continental es más caliente",
                "No hay diferencia"
            ],
            "correcta": "La oceánica es más densa y delgada",
            "pista": "Mira la subpestaña 'Tipos de Litosfera'."
        },
        {
            "id": "lit3",
            "pregunta": "¿Cuántas placas tectónicas principales fragmentan la Litosfera?",
            "opciones": [
                "Alrededor de 15",
                "Alrededor de 3",
                "Alrededor de 100"
            ],
            "correcta": "Alrededor de 15",
            "pista": "Revisa la subpestaña 'Placas Tectónicas'."
        },
        {
            "id": "lit4",
            "pregunta": "¿Cuál es el límite inferior de la Litosfera?",
            "opciones": [
                "La Astenosfera",
                "El Manto inferior",
                "El Núcleo externo"
            ],
            "correcta": "La Astenosfera",
            "pista": "Es donde la roca deja de ser rígida."
        }
    ],
    "pedosfera": [
        {
            "id": "ped1",
            "pregunta": "¿Qué es la Pedosfera?",
            "opciones": [
                "La capa de suelo fértil",
                "La capa de roca profunda",
                "La capa de agua subterránea"
            ],
            "correcta": "La capa de suelo fértil",
            "pista": "Es la 'piel' de la Tierra."
        },
        {
            "id": "ped2",
            "pregunta": "¿Cuál es el orden correcto de los horizontes del suelo, de arriba a abajo?",
            "opciones": [
                "O, A, B, C",
                "A, B, C, O",
                "B, A, O, C"
            ],
            "correcta": "O, A, B, C",
            "pista": "Revisa la subpestaña 'Perfil del Suelo'."
        },
        {
            "id": "ped3",
            "pregunta": "¿Qué procesos intervienen en la formación del suelo (Edafogénesis)?",
            "opciones": [
                "Meteorización y mezcla con materia orgánica",
                "Solo erosión eólica",
                "Solo actividad volcánica"
            ],
            "correcta": "Meteorización y mezcla con materia orgánica",
            "pista": "Revisa la subpestaña 'Edafogénesis'."
        },
        {
            "id": "ped4",
            "pregunta": "¿Por qué es importante la Pedosfera para la vida?",
            "opciones": [
                "Porque almacena nutrientes y agua",
                "Porque genera oxígeno",
                "Porque regula la temperatura global"
            ],
            "correcta": "Porque almacena nutrientes y agua",
            "pista": "Piensa en lo que las plantas necesitan para crecer."
        }
    ],
    "biosfera": [
        {
            "id": "bio1",
            "pregunta": "¿Qué es la Biosfera?",
            "opciones": [
                "El conjunto global de todos los ecosistemas y seres vivos",
                "Solo los animales terrestres",
                "Solo las plantas"
            ],
            "correcta": "El conjunto global de todos los ecosistemas y seres vivos",
            "pista": "Revisa la subpestaña 'Esquema General'."
        },
        {
            "id": "bio2",
            "pregunta": "¿Cuál es la principal fuente de energía que sostiene a la Biosfera?",
            "opciones": [
                "La fotosíntesis",
                "La quimiosíntesis",
                "La energía geotérmica"
            ],
            "correcta": "La fotosíntesis",
            "pista": "Representa el 99.9% de la energía de la Biosfera."
        },
        {
            "id": "bio3",
            "pregunta": "¿Qué proceso permite que exista vida en el fondo oceánico sin luz solar?",
            "opciones": [
                "Quimiosíntesis",
                "Fotosíntesis",
                "Respiración anaeróbica"
            ],
            "correcta": "Quimiosíntesis",
            "pista": "Recuerda la subpestaña 'Quimiosíntesis'."
        },
        {
            "id": "bio4",
            "pregunta": "¿Qué productos genera la fotosíntesis?",
            "opciones": [
                "Glucosa y oxígeno",
                "Solo dióxido de carbono",
                "Solo agua"
            ],
            "correcta": "Glucosa y oxígeno",
            "pista": "Revisa la ecuación en la subpestaña 'Fotosíntesis'."
        }
    ]
}

# --- FUNCIÓN PARA MOSTRAR IMÁGENES ---
def mostrar_imagen(nombre_archivo, texto_alternativo):
    if os.path.exists(nombre_archivo):
        st.image(nombre_archivo, caption=texto_alternativo, use_container_width=True)
    else:
        st.warning(f"⚠️ Guarda una imagen llamada '{nombre_archivo}' en tu carpeta para verla aquí.")

# --- PESTAÑAS PRINCIPALES ---
tab_litosfera, tab_pedosfera, tab_biosfera = st.tabs([
    "🪨 Litosfera",
    "🌱 Pedosfera",
    "🧬 Biosfera"
])

# ============================================================
# PESTAÑA 1: LITOSFERA
# ============================================================
with tab_litosfera:
    st.header("🪨 La Litosfera: La Capa Rígida")

    sub1, sub2, sub3 = st.tabs([
        "📏 Esquema General",
        "🗺️ Placas Tectónicas",
        "⚖️ Tipos de Litosfera"
    ])

    # --- Subpestaña 1: Esquema General ---
    with sub1:
        col1, col2 = st.columns([1.2, 1])
        with col1:
            mostrar_imagen(IMAGENES["Litosfera_Esquema"], "Esquema de la Litosfera sobre la Astenosfera.")
        with col2:
            st.success("### 📖 Definición de la Litosfera")
            st.markdown("""
            La **Litosfera** es la capa externa y rígida de la Tierra. 
            Incluye **toda la corteza** (continental y oceánica) **+ la parte superior del manto**.
            """)
            st.info("### 📊 Datos Clave")
            st.markdown("""
            - **Grosor:** 50-70 km (oceánica) a 100-200 km (continental).
            - **Límite inferior:** La **Astenosfera** (capa plástica sobre la que "flota").
            - **Comportamiento:** Es rígida y quebradiza; se fractura en lugar de fluir.
            - **Importancia:** Es el soporte físico de los continentes y el fondo oceánico.
            """)

    # --- Subpestaña 2: Placas Tectónicas ---
    with sub2:
        col1, col2 = st.columns([1.2, 1])
        with col1:
            mostrar_imagen(IMAGENES["Litosfera_Placas"], "Mapa de placas tectónicas y sus límites.")
        with col2:
            st.success("### 🗺️ Las Placas Tectónicas")
            st.markdown("""
            La Litosfera **no es continua**: está fragmentada en unas **15 placas rígidas** 
            que se mueven lentamente (unos pocos cm al año) sobre la Astenosfera.
            """)
            st.info("### 📊 Tipos de Límites entre Placas")
            st.markdown("""
            - **Convergente:** Las placas chocan → se forman montañas o volcanes (ej. Himalaya).
            - **Divergente:** Las placas se separan → nace nueva corteza oceánica (ej. Dorsal Meso-atlántica).
            - **Transformante:** Las placas se deslizan lateralmente → generan sismos (ej. Falla de San Andrés).
            """)
            st.warning("### 🌋 Fenómenos Asociados")
            st.markdown("""
            En los bordes de placas ocurren la mayoría de **terremotos, volcanes y tsunamis** del planeta.
            """)

    # --- Subpestaña 3: Tipos de Litosfera ---
    with sub3:
        col1, col2 = st.columns([1.2, 1])
        with col1:
            mostrar_imagen(IMAGENES["Litosfera_Tipos"], "Comparación entre litosfera oceánica y continental.")
        with col2:
            st.success("### ⚖️ Tipos de Litosfera")
            st.markdown("Existen dos tipos según su composición y grosor:")
            st.info("### 🌊 Litosfera Oceánica")
            st.markdown("""
            - **Composición:** Basalto (SIMA: Silicio + Magnesio).
            - **Grosor:** 50-70 km (delgada).
            - **Densidad:** Alta (se hunde bajo la continental).
            - **Edad:** Joven (se renueva constantemente).
            """)
            st.warning("### 🏔️ Litosfera Continental")
            st.markdown("""
            - **Composición:** Granito (SIAL: Silicio + Aluminio).
            - **Grosor:** 100-200 km (gruesa).
            - **Densidad:** Baja (flota sobre la oceánica).
            - **Edad:** Antigua (hasta miles de millones de años).
            """)

    st.write("---")
    with st.expander("📝 Pon a prueba tus conocimientos sobre la Litosfera"):
        for q in CUESTIONARIO["litosfera"]:
            ans = st.radio(q["pregunta"], q["opciones"], key=q["id"])
            if st.button("Validar Respuesta", key=f"btn_{q['id']}"):
                if ans == q["correcta"]:
                    st.success("🎉 ¡Excelente! Respuesta correcta.")
                else:
                    st.error(f"❌ Incorrecto. Pista: {q['pista']}")

# ============================================================
# PESTAÑA 2: PEDOSFERA
# ============================================================
with tab_pedosfera:
    st.header("🌱 La Pedosfera: La Piel Viva")

    sub1, sub2 = st.tabs([
        "📏 Perfil del Suelo",
        "🔄 Edafogénesis"
    ])

    # --- Subpestaña 1: Perfil del Suelo ---
    with sub1:
        col1, col2 = st.columns([1.2, 1])
        with col1:
            mostrar_imagen(IMAGENES["Pedosfera_Perfil"], "Perfil del suelo con horizontes O, A, B y C.")
        with col2:
            st.success("### 📖 ¿Qué es la Pedosfera?")
            st.markdown("""
            Es la **capa más superficial de la Litosfera**, transformada por la acción 
            de la vida y el clima. Es el **suelo fértil** donde crecen las plantas.
            """)
            st.info("### 📊 Horizontes del Suelo (de arriba a abajo)")
            st.markdown("""
            - **Horizonte O:** Hojarasca y materia orgánica fresca.
            - **Horizonte A:** Mezcla de humus y minerales (el más fértil).
            - **Horizonte B:** Acumulación de arcilla y óxidos.
            - **Horizonte C:** Roca madre fragmentada.
            """)
            st.warning("### 📏 Grosor")
            st.markdown("Apenas **0.5 a 2 metros**. ¡Es una película finísima comparada con los 6,371 km del radio terrestre!")

    # --- Subpestaña 2: Edafogénesis ---
    with sub2:
        col1, col2 = st.columns([1.2, 1])
        with col1:
            mostrar_imagen(IMAGENES["Pedosfera_Edafogenesis"], "Proceso de formación del suelo (edafogénesis).")
        with col2:
            st.success("### 🔄 La Edafogénesis")
            st.markdown("""
            Es el **proceso de formación del suelo** a partir de la roca madre, 
            gracias a la acción del clima, el agua y los seres vivos.
            """)
            st.info("### 📊 Pasos del Proceso")
            st.markdown("""
            1. **Meteorización:** La roca madre se rompe (física, química y biológica).
            2. **Biodeterioro:** Líquenes y raíces aceleran la fragmentación.
            3. **Mezcla con humus:** La materia orgánica muerta se descompone.
            4. **Formación de horizontes:** Se estratifican las capas O, A, B, C.
            """)
            st.warning("### 🌱 Importancia")
            st.markdown("Sin edafogénesis no habría suelos fértiles, y sin suelos no habría agricultura ni ecosistemas terrestres.")

    st.write("---")
    with st.expander("📝 Pon a prueba tus conocimientos sobre la Pedosfera"):
        for q in CUESTIONARIO["pedosfera"]:
            ans = st.radio(q["pregunta"], q["opciones"], key=q["id"])
            if st.button("Validar Respuesta", key=f"btn_{q['id']}"):
                if ans == q["correcta"]:
                    st.success("🎉 ¡Excelente! Respuesta correcta.")
                else:
                    st.error(f"❌ Incorrecto. Pista: {q['pista']}")

# ============================================================
# PESTAÑA 3: BIOSFERA
# ============================================================
with tab_biosfera:
    st.header("🧬 La Biosfera: La Vida que Conecta")

    sub1, sub2, sub3 = st.tabs([
        "🌍 Esquema General",
        "🌿 Fotosíntesis",
        "⚗️ Quimiosíntesis"
    ])

    # --- Subpestaña 1: Esquema General ---
    with sub1:
        col1, col2 = st.columns([1.2, 1])
        with col1:
            mostrar_imagen(IMAGENES["Biosfera_Esquema"], "La Biosfera como una película delgada de vida.")
        with col2:
            st.success("### 📖 Definición de la Biosfera")
            st.markdown("""
            La **Biosfera** es el conjunto global de todos los ecosistemas y seres vivos. 
            Es una capa delgada (~20 km) que impregna la Litosfera, Hidrosfera y Atmósfera.
            """)
            st.info("### 📊 Datos Clave")
            st.markdown("""
            - **Grosor:** Desde el fondo oceánico (-11 km) hasta la atmósfera baja (+12 km).
            - **Función:** Transforma la Litosfera mediante **biodeterioro** y **edafogénesis**.
            - **Motores energéticos:**
                - **Fotosíntesis** (99.9%).
                - **Quimiosíntesis** (0.1%).
            """)
            st.warning("### 🔗 Relación con las Otras Capas")
            st.markdown("""
            - Con la **Litosfera:** Obtiene nutrientes minerales y la transforma.
            - Con la **Hidrosfera:** Regula el ciclo del agua.
            - Con la **Atmósfera:** Intercambia CO₂ y O₂.
            """)

    # --- Subpestaña 2: Fotosíntesis ---
    with sub2:
        col1, col2 = st.columns([1.2, 1])
        with col1:
            mostrar_imagen(IMAGENES["Biosfera_Fotosintesis"], "Esquema del proceso de fotosíntesis.")
        with col2:
            st.success("### 🌿 La Fotosíntesis")
            st.markdown("""
            Proceso por el cual **plantas, algas y cianobacterias** capturan la energía 
            solar y la convierten en energía química (glucosa).
            """)
            st.info("### 📊 Ecuación General")
            st.markdown("""
            **6 CO₂ + 6 H₂O + Luz solar → C₆H₁₂O₆ + 6 O₂**
            
            - **Reactivos:** Dióxido de carbono (CO₂) + Agua (H₂O).
            - **Productos:** Glucosa (C₆H₁₂O₆) + Oxígeno (O₂).
            """)
            st.warning("### 🌍 Importancia Global")
            st.markdown("""
            - **Libera el oxígeno** que respiramos.
            - **Captura el CO₂** atmosférico (regula el clima).
            - **Es la base de la cadena trófica** en casi todos los ecosistemas.
            - Representa el **99.9%** de la energía que sostiene a la Biosfera.
            """)

    # --- Subpestaña 3: Quimiosíntesis ---
    with sub3:
        col1, col2 = st.columns([1.2, 1])
        with col1:
            mostrar_imagen(IMAGENES["Biosfera_Quimiosintesis"], "Comparación entre fotosíntesis y quimiosíntesis.")
        with col2:
            st.success("### ⚗️ La Quimiosíntesis")
            st.markdown("""
            Proceso por el cual **bacterias y arqueas** obtienen energía oxidando 
            compuestos inorgánicos que vienen directamente de la Litosfera.
            """)
            st.info("### 📊 ¿Dónde Ocurre?")
            st.markdown("""
            - **Fondo oceánico:** Fuentes hidrotermales (fumarolas negras).
            - **Subsuelo terrestre:** Hasta 10 km de profundidad en rocas.
            - **Suelo:** Nitrificación (bacterias *Nitrosomonas* y *Nitrobacter*).
            """)
            st.warning("### ⚡ ¿Qué Produce?")
            st.markdown("""
            - **Materia orgánica nueva** sin necesidad de luz solar.
            - **Compuestos oxidados** (sulfatos, nitratos, óxidos de hierro).
            - **Nuevos minerales** (precipitación de óxidos).
            - **Ecosistemas completos** (gusanos tubícolas gigantes, almejas).
            """)
            st.error("### 🔬 Dato Clave")
            st.markdown("""
            En el suelo, la quimiosíntesis (nitrificación) produce los **nitratos** 
            que las plantas absorben. ¡Sin ella, la agricultura no existiría!
            """)

    st.write("---")
    with st.expander("📝 Pon a prueba tus conocimientos sobre la Biosfera"):
        for q in CUESTIONARIO["biosfera"]:
            ans = st.radio(q["pregunta"], q["opciones"], key=q["id"])
            if st.button("Validar Respuesta", key=f"btn_{q['id']}"):
                if ans == q["correcta"]:
                    st.success("🎉 ¡Excelente! Respuesta correcta.")
                else:
                    st.error(f"❌ Incorrecto. Pista: {q['pista']}")