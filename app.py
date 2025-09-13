import streamlit as st
import pandas as pd
from PIL import Image
import time
import os

# ------------------------------
# Configuración de la página
# ------------------------------
st.set_page_config(
    page_title="FSF & GNU",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ------------------------------
# Mostrar imagen al inicio
# ------------------------------
try:
    image = Image.open("img.jpg")
    st.image(image, use_column_width=True)
except:
    st.warning("⚠️ No se encontró 'img.jpg'. Asegúrate de que esté en la misma carpeta que app.py.")

st.title("🌐 Free Software Foundation (FSF) & GNU")
st.markdown("Una exploración interactiva sobre el software libre y sus fundamentos.")

# ------------------------------
# Tabs principales
# ------------------------------
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📖 Free Software Foundation",
    "💻 GNU",
    "🌍 Importancia",
    "❓ Quiz Interactivo",
    "🏆 Histórico de Puntajes"
])

# ------------------------------
# TAB 1: FSF
# ------------------------------
with tab1:
    st.header("📖 Free Software Foundation (FSF)")
    st.markdown("""
    La **Free Software Foundation (FSF)** fue creada el **4 de octubre de 1985** por **Richard Stallman**.  
    Es una **organización sin fines de lucro** dedicada a **defender la libertad de los usuarios de software**.

    ### Objetivos principales:
    - Promover el desarrollo y uso de **software libre**.
    - Defender los **derechos de los usuarios**.
    - Mantener la **licencia GNU GPL** (General Public License).
    - Educar sobre la importancia de la **libertad tecnológica**.
    """)

# ------------------------------
# TAB 2: GNU
# ------------------------------
with tab2:
    st.header("💻 Proyecto GNU")
    st.markdown("""
    El **Proyecto GNU** fue iniciado en **1983** por Richard Stallman.  
    Su objetivo fue crear un sistema operativo **completamente libre**.

    ### Características clave:
    - Incluye compiladores, bibliotecas, editores de texto, herramientas de red.
    - Usa la **Licencia Pública General de GNU (GPL)** para garantizar que siga siendo libre.
    - Dio origen al término **GNU/Linux**, ya que muchas distribuciones usan el kernel de Linux junto con las herramientas GNU.
    """)

# ------------------------------
# TAB 3: Importancia
# ------------------------------
with tab3:
    st.header("🌍 Importancia del Software Libre")
    st.markdown("""
    El **software libre** no significa gratuito, sino que garantiza **libertades esenciales**:

    1. **Libertad de usar** el programa con cualquier propósito.
    2. **Libertad de estudiar** cómo funciona y adaptarlo.
    3. **Libertad de compartir** copias.
    4. **Libertad de mejorar** el programa y compartir esas mejoras.

    ### Beneficios globales:
    - Evita la **dependencia tecnológica** de corporaciones.
    - Favorece la **colaboración y transparencia**.
    - Ha impulsado proyectos como **Linux, Firefox, LibreOffice**.
    """)

# ------------------------------
# TAB 4: Quiz
# ------------------------------
with tab4:
    st.header("❓ Quiz Interactivo")
    st.markdown("Pon a prueba lo que aprendiste sobre **FSF y GNU**. El puntaje baja mientras más demores ⏳.")

    name = st.text_input("✍️ Ingresa tu nombre para comenzar:")

    if name:
        if "quiz_started" not in st.session_state:
            st.session_state.quiz_started = False
            st.session_state.start_time = None

        if not st.session_state.quiz_started:
            if st.button("🚀 Comenzar Quiz"):
                st.session_state.quiz_started = True
                st.session_state.start_time = time.time()
                st.rerun()
        else:
            questions = [
                {
                    "q": "¿En qué año se fundó la Free Software Foundation?",
                    "options": ["1980", "1985", "1990"],
                    "answer": "1985"
                },
                {
                    "q": "¿Quién fundó la Free Software Foundation?",
                    "options": ["Linus Torvalds", "Bill Gates", "Richard Stallman"],
                    "answer": "Richard Stallman"
                },
                {
                    "q": "¿Qué significa GNU?",
                    "options": ["GNU is Not Unix", "General New Utility", "Global Network Union"],
                    "answer": "GNU is Not Unix"
                },
                {
                    "q": "¿Qué licencia mantiene la FSF?",
                    "options": ["MIT", "GNU GPL", "Apache"],
                    "answer": "GNU GPL"
                },
                {
                    "q": "¿Qué libertad NO pertenece al software libre?",
                    "options": [
                        "Usar el programa con cualquier propósito",
                        "Estudiar y modificar el código",
                        "Prohibir que otros usen el programa"
                    ],
                    "answer": "Prohibir que otros usen el programa"
                }
            ]

            score = 0
            for i, q in enumerate(questions):
                st.subheader(f"Pregunta {i+1}")
                answer = st.radio(q["q"], q["options"], key=f"q{i}")
                if answer == q["answer"]:
                    score += 20  # cada respuesta vale 20 puntos

            if st.button("✅ Finalizar"):
                end_time = time.time()
                elapsed = int(end_time - st.session_state.start_time)

                # Penalización por tiempo: pierde 1 punto cada 2 segundos
                penalty = elapsed // 2
                final_score = max(score - penalty, 0)

                st.success(f"{name}, tu puntaje final es: **{final_score} / 100** ⏱️ (Tiempo: {elapsed} segundos)")

                # Guardar en CSV
                record_file = "scores.csv"
                new_entry = pd.DataFrame([[name, final_score, elapsed]], columns=["Nombre", "Puntaje", "Tiempo"])

                if os.path.exists(record_file):
                    df = pd.read_csv(record_file)
                    df = pd.concat([df, new_entry], ignore_index=True)
                else:
                    df = new_entry

                df.to_csv(record_file, index=False)
                st.rerun()

# ------------------------------
# TAB 5: Histórico
# ------------------------------
with tab5:
    st.header("🏆 Histórico de Puntajes")
    record_file = "scores.csv"
    if os.path.exists(record_file):
        df = pd.read_csv(record_file)
        st.dataframe(df.sort_values(by="Puntaje", ascending=False), use_container_width=True)
    else:
        st.info("Aún no hay registros. ¡Sé el primero en jugar el quiz!")
