import streamlit as st
import re              # Para buscar patrones en texto (regex)
import pyperclip       # Para copiar texto al portapapeles

# Configuración básica de la app
st.set_page_config(
    page_title="Extractor 🔴 Zotero",
    layout="centered"
)

# Título y descripción
st.title("Extractor de anotaciones 🔴")
st.caption("Pega anotaciones de Zotero y extrae solo lo marcado con 🔴")

# Área donde el usuario pega el texto crudo
raw_text = st.text_area(
    "Pega aquí el texto:",
    height=300,
    placeholder="Pega aquí las anotaciones tal como salen de Zotero…"
)

# Lista donde guardaremos las líneas limpias
output_lines = []

# Solo procesamos si el usuario pegó algo
if raw_text:
    # Recorremos el texto línea por línea
    for line in raw_text.splitlines():

        # Regla central: solo líneas con 🔴
        if "🔴" in line:

            # Buscar texto entre comillas
            # Ejemplo: "sheet steel"
            text_match = re.search(r'"([^"]+)"', line)

            # Buscar número de página
            # Ejemplo: p. 14
            page_match = re.search(r"p\.\s*(\d+)", line)

            # Si encontramos ambos, construimos la línea limpia
            if text_match and page_match:
                clean_line = (
                    f"{text_match.group(1)} "
                    f"(p. {page_match.group(1)})"
                )
                output_lines.append(clean_line)

# Unimos todas las líneas limpias en un solo texto
result = "\n".join(output_lines)

# Mostrar el resultado
st.subheader("Resultado")
st.text_area(
    "Salida limpia:",
    value=result,
    height=150
)

# Botón para copiar al portapapeles
if st.button("📋 Copiar al portapapeles"):
    if result.strip():
        pyperclip.copy(result)
        st.success("Copiado al portapapeles")
    else:
        st.warning("No hay nada para copiar")
