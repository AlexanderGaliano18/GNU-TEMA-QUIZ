import streamlit as st
import pandas as pd
import numpy as np
import time
import json
from datetime import datetime
from pathlib import Path

# -------------------------------
# Config
# -------------------------------
st.set_page_config(page_title="FSF & GNU - Aprendizaje interactivo", layout="wide", page_icon="🧑‍💻")
DATAFILE = Path("records.json")

# -------------------------------
# Estilos (CSS)
# -------------------------------
st.markdown("""
<style>
    .big-title {font-size:34px; font-weight:700;}
    .subtitle {color:#6b7280; font-size:16px}
    .card {background: linear-gradient(135deg, #ffffff 0%, #f3f7ff 100%); padding:18px; border-radius:14px; box-shadow: 0 6px 18px rgba(20,40,100,0.08);}
    .accent {color:#0b5cff; font-weight:600}
    .quiz-box {background:#0b1220; color:white; padding:18px; border-radius:12px}
</style>
""", unsafe_allow_html=True)

# -------------------------------
# Helper: load/save records
# -------------------------------

def load_records():
    if DATAFILE.exists():
        try:
            with open(DATAFILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []


def save_record(record):
    records = load_records()
    records.append(record)
    with open(DATAFILE, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)


# -------------------------------
# Contenido estático: FSF / GNU
# -------------------------------

col1, col2 = st.columns([2, 1])
with col1:
    st.markdown('<div class="big-title">Free Software Foundation (FSF) & ¿Qué es GNU?</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Explora los conceptos, la historia y la filosofía del software libre —y pon a prueba lo aprendido con un quiz interactivo.</div>', unsafe_allow_html=True)

with col2:
    st.markdown('''
    <div style="text-align:right">
    <h3 style="margin:0">🛡️ ¿Listo?</h3>
    <p style="margin:0.1rem">Aprende. Responde. Deja tu récord.</p>
    </div>
    ''', unsafe_allow_html=True)

st.markdown("---")

# Cards con información
info_cols = st.columns(3)

with info_cols[0]:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.header("¿Qué es la FSF?")
    st.write("La Free Software Foundation (FSF) es una organización fundada en 1985 por Richard Stallman que promueve la libertad de los usuarios para usar, estudiar, compartir y mejorar el software. La FSF defiende las 4 libertades esenciales del software libre.")
    st.markdown('</div>', unsafe_allow_html=True)

with info_cols[1]:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.header("¿Qué es GNU?")
    st.write("GNU es un proyecto iniciado por Richard Stallman en 1983 con el objetivo de crear un sistema operativo completamente libre. GNU significa 'GNU's Not Unix' y proporciona muchas herramientas esenciales para sistemas operativos libres.")
    st.markdown('</div>', unsafe_allow_html=True)

with info_cols[2]:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.header("Licencias y filosofía")
    st.write("La FSF promueve licencias copyleft, como la GNU GPL, que permiten distribuir software libre conservando las mismas libertades para los usuarios posteriores.")
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")

# Sección detallada
st.subheader("Conceptos clave")
st.markdown("""
- **4 libertades del software libre**: libertad para usar el programa, estudiar y modificar su código, distribuir copias, y distribuir versiones modificadas.
- **Copyleft**: técnica legal que usa licencias (p. ej. GPL) para asegurar que todas las versiones derivadas sigan siendo libres.
- **Diferencia con 'open source'**: el movimiento "Free Software" se centra en la ética y derechos; "Open Source" suele enfatizar prácticas de desarrollo y beneficios prácticos.
""")

st.subheader("Breve historia")
st.write("GNU fue iniciado en 1983; la FSF nació en 1985. Muchas herramientas del proyecto GNU combinadas con el kernel Linux dieron lugar a sistemas operativos conocidos como 'distribuciones GNU/Linux'.")

st.markdown("---")

# -------------------------------
# Quiz interactivo
# -------------------------------

st.subheader("Quiz: Pon a prueba tus conocimientos ✍️")
st.write("Responde las 5 preguntas. Cada pregunta tiene una puntuación máxima y el tiempo que tardes reducirá los puntos que puedes ganar.")

# Preguntas (lista de dicts)
QUESTIONS = [
    {
        "q": "¿Quién fundó la Free Software Foundation (FSF)?",
        "options": ["Linus Torvalds", "Richard Stallman", "Bill Gates", "Steve Jobs"],
        "answer": 1
    },
    {
        "q": "¿Qué significa la sigla GNU?",
        "options": ["GNU's Not Unix", "General New Unix", "Global Network Utility", "Great New User"],
        "answer": 0
    },
    {
        "q": "¿Cuál de estas es una 'libertad' del software libre?",
        "options": ["Libertad de cobrar por software", "Libertad para ejecutar el programa para cualquier propósito", "Libertad de evitar actualizaciones", "Libertad de usar sólo en servidores"],
        "answer": 1
    },
    {
        "q": "¿Qué es copyleft?",
        "options": ["Una patente de software", "Una licencia que prohíbe compartir el código", "Una forma de asegurar que las versiones derivadas permanezcan libres", "Un tipo de hardware"],
        "answer": 2
    },
    {
        "q": "¿Qué licencia es promovida por la FSF como ejemplo de copyleft fuerte?",
        "options": ["MIT", "BSD", "GNU GPL", "Apache"],
        "answer": 2
    }
]

# Parámetros de puntuación
MAX_POINTS_PER_QUESTION = 100
DECAY_PER_SECOND = 5  # cada segundo reduce 5 puntos
MIN_POINTS_PER_QUESTION = 10

# Session state inicial
if 'quiz_index' not in st.session_state:
    st.session_state.quiz_index = 0
    st.session_state.score = 0
    st.session_state.started = False
    st.session_state.start_time = None
    st.session_state.responses = []

# Contenedor del quiz
quiz_col1, quiz_col2 = st.columns([3,1])
with quiz_col1:
    if not st.session_state.started:
        st.markdown('<div class="quiz-box">', unsafe_allow_html=True)
        st.markdown('### 🧭 Instrucciones rápidas')
        st.write(f"Serán {len(QUESTIONS)} preguntas. Cada pregunta vale hasta {MAX_POINTS_PER_QUESTION} puntos; el tiempo reduce la puntuación ({DECAY_PER_SECOND} pt/s). Al finalizar deja tu nombre y guarda el récord.")
        if st.button("Comenzar Quiz"):
            st.session_state.started = True
            st.session_state.quiz_index = 0
            st.session_state.score = 0
            st.session_state.responses = []
            st.session_state.start_time = time.time()
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        idx = st.session_state.quiz_index
        if idx < len(QUESTIONS):
            q = QUESTIONS[idx]
            st.markdown(f"**Pregunta {idx+1} de {len(QUESTIONS)}**")
            st.write(q['q'])
            choice = st.radio("Elige una opción:", q['options'], key=f"q{idx}")

            # Mostrar tiempo transcurrido en la pregunta (calculado al enviar)
            if st.button("Enviar respuesta"):
                elapsed = time.time() - st.session_state.start_time if st.session_state.start_time else 0
                elapsed = max(0, elapsed)
                # calcular puntos
                points_lost = int(elapsed * DECAY_PER_SECOND)
                points_awarded = max(MIN_POINTS_PER_QUESTION, MAX_POINTS_PER_QUESTION - points_lost)
                selected_index = q['options'].index(choice)
                correct = (selected_index == q['answer'])
                earned = points_awarded if correct else 0
                st.session_state.responses.append({
                    'question': q['q'],
                    'selected': choice,
                    'correct': q['options'][q['answer']],
                    'is_correct': correct,
                    'time': round(elapsed,2),
                    'points_awarded': earned
                })
                st.session_state.score += earned
                st.session_state.quiz_index += 1
                st.session_state.start_time = time.time()  # reiniciar para la siguiente pregunta
                st.experimental_rerun()
        else:
            # Fin del quiz
            st.success(f"🎉 ¡Quiz completado! Puntaje total: {st.session_state.score} pts")
            st.write("Revisión de tus respuestas:")
            for r in st.session_state.responses:
                st.write(f"- **{r['question']}** — Tu respuesta: *{r['selected']}* — Correcta: *{r['correct']}* — Tiempo: {r['time']}s — Pts: {r['points_awarded']}")

            name = st.text_input("Ingresa tu nombre para guardar el récord:")
            if 'saved' not in st.session_state:
                st.session_state.saved = False

            if st.button("Guardar récord") and name.strip() != "":
                record = {
                    'name': name.strip(),
                    'score': st.session_state.score,
                    'date': datetime.utcnow().isoformat(),
                    'details': st.session_state.responses
                }
                save_record(record)
                st.session_state.saved = True
                st.success("Récord guardado ✅")

            if st.session_state.saved:
                st.write("Puedes ver la tabla de récords en la columna de la derecha.")

            if st.button("Reiniciar quiz"):
                st.session_state.started = False
                st.session_state.quiz_index = 0
                st.session_state.score = 0
                st.session_state.responses = []
                st.session_state.start_time = None
                st.session_state.saved = False
                st.experimental_rerun()

with quiz_col2:
    st.header("🏆 Récords históricos")
    records = load_records()
    if records:
        df = pd.DataFrame(records)
        # Mostrar top 10
        df_display = df.sort_values('score', ascending=False).reset_index(drop=True)[['name','score','date']]
        df_display['date'] = pd.to_datetime(df_display['date']).dt.tz_localize(None)
        st.dataframe(df_display.head(10))

        # Descargar CSV
        csv = df_display.to_csv(index=False).encode('utf-8')
        st.download_button("Descargar tabla (CSV)", data=csv, file_name="records_fsf_quiz.csv", mime='text/csv')

        # Mostrar el mejor
        top = df_display.iloc[0]
        st.markdown(f"**Récord actual:** {top['name']} — {top['score']} pts")
    else:
        st.info("Aún no hay récords. ¡Sé el primero en participar!")

    st.markdown("---")
    st.markdown("**Consejos de estudio**")
    st.write("Revisa las 4 libertades, el concepto de copyleft y la historia de GNU/FSF para mejorar tu puntaje.")

# Footer
st.markdown("---")
st.caption("App educativa sobre FSF y GNU — desarrollada con ❤️. Los datos se almacenan localmente en records.json en el servidor de la aplicación.")
