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
# Funciones para resultados
# ------------------------------
record_file = "scores.csv"

def load_results():
    if os.path.exists(record_file):
        return pd.read_csv(record_file).to_dict(orient="records")
    return []

def save_results(resultados):
    df = pd.DataFrame(resultados)
    df.to_csv(record_file, index=False)

# ------------------------------
# Mostrar imagen al inicio
# ------------------------------
try:
    image = Image.open("img.jpg")
    st.image(image, use_container_width=True)
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

# --------------------------
# TAB 4: QUIZ INTERACTIVO
# --------------------------
with tab4:
    st.header("📝 Quiz sobre FSF y GNU")
    st.write("Responde las preguntas una por una. Tu puntaje dependerá del tiempo ⏳.")

    # Configuración inicial
    if "quiz_started" not in st.session_state:
        st.session_state.quiz_started = False
        st.session_state.quiz_start_time = None
        st.session_state.current_q = 0
        st.session_state.correct = 0
        st.session_state.incorrect = 0
        st.session_state.answers = []
        st.session_state.name = ""

    preguntas = [
        {
            "pregunta": "¿En qué año se fundó la Free Software Foundation (FSF)?",
            "opciones": ["1980", "1983", "1985", "1990"],
            "respuesta": "1985"
        },
        {
            "pregunta": "¿Quién fundó la Free Software Foundation?",
            "opciones": ["Linus Torvalds", "Richard Stallman", "Dennis Ritchie", "Bill Gates"],
            "respuesta": "Richard Stallman"
        },
        {
            "pregunta": "¿Qué significa GNU?",
            "opciones": ["General Network Utility", "GNU's Not Unix", "Global New Unix", "General New Utility"],
            "respuesta": "GNU's Not Unix"
        },
        {
            "pregunta": "¿Qué relación tiene GNU con Linux?",
            "opciones": ["Ninguna", "Linux es parte de GNU", "GNU provee herramientas y utilidades para Linux", "GNU fue creado después de Linux"],
            "respuesta": "GNU provee herramientas y utilidades para Linux"
        },
        {
            "pregunta": "¿Cuál es uno de los principales objetivos de la FSF?",
            "opciones": ["Promover software privativo", "Defender la libertad de los usuarios de software", "Vender licencias comerciales", "Eliminar Linux"],
            "respuesta": "Defender la libertad de los usuarios de software"
        }
    ]

    # Nombre
    if not st.session_state.quiz_started:
        name = st.text_input("Ingresa tu nombre para comenzar:", "")
        if name:
            if st.button("Comenzar Quiz"):
                st.session_state.quiz_started = True
                st.session_state.quiz_start_time = time.time()
                st.session_state.name = name
                st.rerun()
    else:
        q_index = st.session_state.current_q
        if q_index < len(preguntas):
            q = preguntas[q_index]
            st.subheader(f"Pregunta {q_index+1} de {len(preguntas)}")
            r = st.radio(q["pregunta"], q["opciones"], key=f"q{q_index}")

            if st.button("Responder"):
                if r == q["respuesta"]:
                    st.success("✅ ¡Correcto!")
                    st.session_state.correct += 1
                else:
                    st.error(f"❌ Incorrecto. La respuesta era: {q['respuesta']}")
                    st.session_state.incorrect += 1

                st.session_state.answers.append(r)
                st.session_state.current_q += 1
                st.rerun()
        else:
            elapsed_time = time.time() - st.session_state.quiz_start_time
            base_points = 100
            score = max(10, base_points - int(elapsed_time)) * st.session_state.correct

            st.success(f"🎉 {st.session_state.name}, terminaste el quiz")
            st.info(f"✅ Correctas: {st.session_state.correct} | ❌ Incorrectas: {st.session_state.incorrect}")
            st.info(f"🏆 Puntaje final: {score}")

            resultados = load_results()
            resultados.append({
                "Nombre": st.session_state.name,
                "Puntaje": score,
                "Correctas": st.session_state.correct,
                "Incorrectas": st.session_state.incorrect,
                "Tiempo": round(elapsed_time, 2)
            })
            save_results(resultados)
            st.balloons()

            if st.button("Reiniciar Quiz"):
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.rerun()

    st.markdown("---")
    st.subheader("📊 Resultados Históricos")
    resultados = load_results()
    if resultados:
        df = pd.DataFrame(resultados)
        st.dataframe(df, use_container_width=True)
    else:
        st.write("Aún no hay resultados registrados.")

# ------------------------------
# TAB 5: Histórico
# ------------------------------
with tab5:
    st.header("🏆 Histórico de Puntajes")
    if os.path.exists(record_file):
        df = pd.read_csv(record_file)
        df = df.sort_values(by="Puntaje", ascending=False).reset_index(drop=True)

        medals = ["🥇", "🥈", "🥉"]
        df["Ranking"] = df.index + 1
        df.loc[:2, "Ranking"] = medals[:len(df)]

        st.subheader("📋 Tabla de posiciones")
        st.dataframe(df[["Ranking", "Nombre", "Puntaje", "Tiempo"]], use_container_width=True)

        st.subheader("🔥 Podio")
        for i, row in df.head(3).iterrows():
            st.markdown(f"**{row['Ranking']} {row['Nombre']}** → {row['Puntaje']} puntos ⏱️ {row['Tiempo']}s")

        st.subheader("📊 Ranking visual")
        st.bar_chart(df.set_index("Nombre")["Puntaje"])
    else:
        st.info("Aún no hay registros. ¡Sé el primero en jugar el quiz!")
