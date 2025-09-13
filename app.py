import streamlit as st
import pandas as pd
import time

# ---------------- CONFIGURACIÓN DE LA PÁGINA ---------------- #
st.set_page_config(
    page_title="FSF & GNU",
    page_icon="🐧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- ESTILOS ---------------- #
st.markdown(
    """
    <style>
    .title {
        text-align: center;
        color: #2E86C1;
        font-size: 42px;
        font-weight: bold;
    }
    .subtitle {
        text-align: center;
        color: #117864;
        font-size: 28px;
        margin-bottom: 20px;
    }
    .content {
        font-size: 18px;
        text-align: justify;
    }
    .quiz-title {
        text-align: center;
        color: #CB4335;
        font-size: 30px;
        font-weight: bold;
        margin-top: 40px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------------- CABECERA ---------------- #
st.markdown('<p class="title">🐧 Free Software Foundation (FSF)</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">¿Qué es GNU?</p>', unsafe_allow_html=True)

st.image(
    "https://upload.wikimedia.org/wikipedia/commons/3/3f/GNU_and_FSFLA_Logos.svg",
    caption="Logo oficial de GNU y la Free Software Foundation",
    use_column_width=True
)

# ---------------- CONTENIDO PRINCIPAL ---------------- #
st.markdown(
    """
    <div class="content">
    La <b>Free Software Foundation (FSF)</b> fue fundada en 1985 por Richard Stallman para apoyar el movimiento del software libre. 
    Su misión es defender la libertad de los usuarios de computadoras y promover el desarrollo y uso de software libre.

    El sistema <b>GNU</b> (GNU's Not Unix) es un sistema operativo libre, compuesto enteramente de software libre. 
    Fue iniciado en 1983 por Richard Stallman, con la visión de crear un sistema similar a Unix pero que respetara 
    la libertad de los usuarios. Posteriormente, con el núcleo Linux, nació la combinación más conocida: <b>GNU/Linux</b>.
    </div>
    """,
    unsafe_allow_html=True
)

st.info("💡 **Dato clave:** El software libre se define por las **4 libertades esenciales**: usar, estudiar, modificar y compartir.")

# ---------------- QUIZ ---------------- #
st.markdown('<p class="quiz-title">🎯 Quiz interactivo: FSF & GNU</p>', unsafe_allow_html=True)

if "records" not in st.session_state:
    st.session_state.records = []

if "score" not in st.session_state:
    st.session_state.score = 0

if "step" not in st.session_state:
    st.session_state.step = 0

# Preguntas
preguntas = [
    {
        "q": "¿En qué año se fundó la Free Software Foundation?",
        "options": ["1983", "1985", "1991", "2000"],
        "answer": "1985"
    },
    {
        "q": "¿Qué significa GNU?",
        "options": ["Global Network Utility", "GNU's Not Unix", "General New Unix", "Great New Utility"],
        "answer": "GNU's Not Unix"
    },
    {
        "q": "¿Quién fundó la FSF?",
        "options": ["Linus Torvalds", "Bill Gates", "Richard Stallman", "Steve Jobs"],
        "answer": "Richard Stallman"
    },
    {
        "q": "¿Qué libertad NO pertenece a las 4 libertades del software libre?",
        "options": ["Usar el programa", "Vender el programa como propio sin código fuente", "Estudiar y modificar", "Compartir copias"],
        "answer": "Vender el programa como propio sin código fuente"
    },
    {
        "q": "¿Cuál es el núcleo que se unió a GNU para formar GNU/Linux?",
        "options": ["Minix", "Unix", "Linux", "Windows NT"],
        "answer": "Linux"
    }
]

# Lógica del quiz
if st.session_state.step < len(preguntas):
    pregunta_actual = preguntas[st.session_state.step]

    st.subheader(f"Pregunta {st.session_state.step + 1}: {pregunta_actual['q']}")
    respuesta = st.radio("Elige tu respuesta:", pregunta_actual["options"], key=f"q{st.session_state.step}")

    if st.button("Responder", key=f"btn{st.session_state.step}"):
        if respuesta == pregunta_actual["answer"]:
            st.success("✅ Correcto!")
            st.session_state.score += 10
        else:
            st.error(f"❌ Incorrecto. La respuesta correcta es: {pregunta_actual['answer']}")

        time.sleep(1)
        st.session_state.step += 1
        st.rerun()

else:
    st.success(f"🎉 Quiz finalizado. Tu puntaje total es: {st.session_state.score} puntos.")

    nombre = st.text_input("Escribe tu nombre para registrar tu puntaje:")
    if st.button("Guardar resultado"):
        if nombre.strip() != "":
            st.session_state.records.append({"Nombre": nombre, "Puntaje": st.session_state.score})
            st.session_state.score = 0
            st.session_state.step = 0
            st.success("✅ Resultado guardado en la tabla histórica.")
            st.rerun()

    # Mostrar tabla histórica
    if st.session_state.records:
        df = pd.DataFrame(st.session_state.records)
        st.subheader("📊 Tabla histórica de resultados")
        st.dataframe(df)
