"""
Genera un archivo HTML de solo lectura con todo el avance.
Abrirlo en cualquier navegador (PC o celular).
Corre con:  python exportar_html.py
"""

from datetime import datetime
from html import escape

from db import SessionLocal
from models import Grupo, Tema, Progreso


ARCHIVO_SALIDA = "avance_vista.html"

ETIQUETAS_ESTADO = {
    "visto_presencial": ("Visto en clase", "verde"),
    "visto_auto":       ("Autoevaluado",   "azul"),
    "pendiente":        ("Pendiente",      "gris"),
}


def recolectar_datos():
    s = SessionLocal()
    try:
        grupos = s.query(Grupo).order_by(Grupo.nombre).all()
        resultado = []
        for grupo in grupos:
            filas = (
                s.query(Tema, Progreso)
                .join(Progreso, Progreso.tema_id == Tema.id)
                .filter(Progreso.grupo_id == grupo.id)
                .order_by(Tema.orden)
                .all()
            )
            temas = [
                {
                    "web": t.web_nombre,
                    "titulo": t.titulo,
                    "estado": p.estado,
                    "resumen": p.resumen_clase,
                    "tarea": p.tarea_asignada,
                }
                for t, p in filas
            ]
            vistos = sum(1 for t in temas if t["estado"] != "pendiente")
            resultado.append({
                "nombre": grupo.nombre,
                "vistos": vistos,
                "total": len(temas),
                "temas": temas,
            })
        return resultado
    finally:
        s.close()


def construir_html(grupos):
    fecha = datetime.now().strftime("%d/%m/%Y %H:%M")

    css = """
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        background: #f4f5f7;
        color: #222;
        line-height: 1.4;
        padding: 12px;
        max-width: 720px;
        margin: 0 auto;
    }
    header {
        background: white;
        padding: 16px;
        border-radius: 8px;
        margin-bottom: 16px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.06);
    }
    header h1 { font-size: 1.2em; margin-bottom: 4px; }
    header p { font-size: 0.85em; color: #666; }

    .grupo {
        background: white;
        border-radius: 8px;
        margin-bottom: 16px;
        overflow: hidden;
        box-shadow: 0 1px 3px rgba(0,0,0,0.06);
    }
    .grupo-header {
        padding: 12px 16px;
        background: #2c3e50;
        color: white;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .grupo-header h2 { font-size: 1.1em; }
    .grupo-header .contador { font-size: 0.9em; opacity: 0.9; }

    .tema {
        padding: 10px 16px;
        border-bottom: 1px solid #eee;
        display: flex;
        flex-direction: column;
        gap: 4px;
    }
    .tema:last-child { border-bottom: none; }

    .tema-linea1 {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        gap: 8px;
    }
    .tema-titulo {
        font-size: 0.95em;
        flex: 1;
    }
    .tema-titulo .web { font-weight: 600; color: #555; }
    .badge {
        font-size: 0.7em;
        padding: 3px 8px;
        border-radius: 10px;
        white-space: nowrap;
        font-weight: 600;
        text-transform: uppercase;
    }
    .badge-verde { background: #28a745; color: white; }
    .badge-azul  { background: #87CEEB; color: #08303f; }
    .badge-gris  { background: #e0e0e0; color: #666; }

    .tema-linea2 {
        display: flex;
        gap: 12px;
        font-size: 0.8em;
    }
    .sub-ok   { color: #28a745; font-weight: 600; }
    .sub-off  { color: #bbb; }
    """

    partes = [f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Control de Avance — CNEyT III</title>
<style>{css}</style>
</head>
<body>
<header>
    <h1>📚 Control de Avance — CNEyT III</h1>
    <p>Generado: {fecha}</p>
</header>
"""]

    for g in grupos:
        partes.append('<section class="grupo">')
        partes.append('  <div class="grupo-header">')
        partes.append(f'    <h2>{escape(g["nombre"])}</h2>')
        partes.append(f'    <span class="contador">{g["vistos"]} de {g["total"]} vistos</span>')
        partes.append('  </div>')

        for t in g["temas"]:
            etiqueta, color = ETIQUETAS_ESTADO[t["estado"]]

            subs = []
            if t["estado"] == "visto_presencial":
                subs.append(("📝 Resumen", t["resumen"]))
            if t["estado"] != "pendiente":
                subs.append(("📚 Tarea", t["tarea"]))

            subs_html = ""
            if subs:
                items = []
                for nombre, ok in subs:
                    clase = "sub-ok" if ok else "sub-off"
                    simbolo = "✓" if ok else "○"
                    items.append(f'<span class="{clase}">{simbolo} {nombre}</span>')
                subs_html = f'<div class="tema-linea2">{" ".join(items)}</div>'

            partes.append(f"""  <div class="tema">
    <div class="tema-linea1">
      <div class="tema-titulo">
        <span class="web">{escape(t["web"])}</span> — {escape(t["titulo"])}
      </div>
      <span class="badge badge-{color}">{escape(etiqueta)}</span>
    </div>
    {subs_html}
  </div>""")

        partes.append('</section>')

    partes.append("</body></html>")
    return "\n".join(partes)


def generar_html():
    """Devuelve el HTML completo como string. Lo usan app.py y main()."""
    grupos = recolectar_datos()
    return construir_html(grupos)


def main():
    print("Recolectando datos...")
    html = generar_html()

    print("Guardando archivo...")
    with open(ARCHIVO_SALIDA, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"OK: {ARCHIVO_SALIDA} generado.")
    print("Ábrelo en el navegador o cópialo al celular.")


if __name__ == "__main__":
    main()