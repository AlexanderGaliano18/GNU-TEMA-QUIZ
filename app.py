import streamlit as st
import pandas as pd
import time

# ---------------- CONFIGURACIÓN ---------------- #
st.set_page_config(
    page_title="FSF & GNU",
    page_icon="🐧",
    layout="wide"
)

# ---------------- ESTILOS ---------------- #
st.markdown(
    """
    <style>
    .title {
        text-align: center;
        color: #1A5276;
        font-size: 40px;
        font-weight: bold;
        margin-bottom: 10px;
    }
    .subtitle {
        text-align: center;
        color: #117864;
        font-size: 24px;
        margin-bottom: 20px;
    }
    .content {
        font-size: 18px;
        text-align: justify;
    }
    .quiz-title {
        text-align: center;
        color: #CB4335;
        font-size: 28px;
        font-weight: bold;
        margin-top: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------------- TABS ---------------- #
tab1, tab2, tab3, tab4 = st.tabs(["📖 FSF", "💻 GNU", "🔑 Libertades", "🎯 Quiz"])

# ---------------- TAB 1: FSF ---------------- #
with tab1:
    st.markdown('<p class="title">Free Software Foundation (FSF)</p>', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="content">
        La <b>Free Software Foundation (FSF)</b> fue fundada en 1985 por Richard Stallman. 
        Es una organización sin fines de lucro que promueve la libertad de los usuarios de software.  
        
        Su objetivo principal es <b>proteger los derechos de los usuarios</b>, asegurando que el software pueda ser:  
        - Usado libremente.  
        - Estudiado para comprender cómo funciona.  
        - Modificado para adaptarse a las necesidades.  
        - Compartido con otros usuarios.  

        La FSF es clave en la defensa del movimiento del software libre y en la creación de licencias como la **GNU General Public License (GPL)**.
        </div>
        """,
        unsafe_allow_html=True
    )

# ---------------- TAB 2: GNU ---------------- #
with tab2:
    st.markdown('<p class="title">Proyecto GNU</p>', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="content">
        El <b>proyecto GNU</b> fue iniciado en 1983 por Richard Stallman con el objetivo de desarrollar un sistema operativo completamente libre.  
        
        GNU significa: <b>“GNU’s Not Unix”</b>, un acrónimo recursivo.  
        
        El proyecto creó programas esenciales como:  
        - El compilador **GCC**.  
        - El editor de texto **Emacs**.  
        - Utilidades del sistema operativo.  

        Cuando en 1991 apareció el <b>núcleo Linux</b>, se unió con GNU y nació lo que hoy conocemos como **GNU/Linux**, uno de los sistemas operativos más usados en servidores y dispositivos.
        </div>
        """,
        unsafe_allow_html=True
    )

# ---------------- TAB 3: Libertades ---------------- #
with tab3:
    st.markdown('<p class="title">🔑 Las 4 Libertades del Software Libre</p>', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="content">
        Según la FSF, un software es libre si respeta estas 4 libertades:  

        1️⃣ **Libertad 0**: Usar el programa con cualquier propósito.  
        2️⃣ **Libertad 1**: Estudiar cómo funciona el programa y modificarlo. (Acceso al código fuente es indispensable).  
        3️⃣ **Libertad 2**: Distribuir copias para ayudar a otros.  
        4️⃣ **Libertad 3**: Mejorar el programa y hacer públicas las mejoras, para beneficio de toda la comunidad.  

        Estas libertades garantizan que el software sea un bien común y no una caja negra controlada por una empresa.
        </div>
        """,
        unsafe_allow_html=True
    )

# ---------------- TAB 4: Quiz ---------------- #
with tab4:
    st.markdown('<p class="quiz-title">Quiz interactivo: FSF & GNU</p>', unsafe_allow_html=True)

    # Estado
    if "records" not in st.session_state:
        st.session_state.records = []
    if "score" not in st.session_state:
        st.session_state.score = 0
    if "step" not in st.session_state:
        st.session_state.step = 0
    if "nombre" not in st.session_state:
        st.session_state.nombre = ""
    if "start_time" not in st.session_state:
        st.session_state.start_time = None

    # Pedir nombre
    if st.session_state.nombre == "":
        nombre = st.text_input("✍️ Ingresa tu nombre para comenzar el quiz:")
        if st.button("Empezar"):
            if nombre.strip() == "":
                st.warning("⚠️ Por favor, escribe tu nombre para poder continuar.")
            else:
                st.session_state.nombre = nombre
                st.session_state.step = 0
                st.session_state.score = 0
                st.session_state.start_time = time.time()
                st.rerun()
    else:
        # Preguntas
        preguntas = [
            {"q": "¿En qué año se fundó la Free Software Foundation?", 
             "options": ["1983", "1985", "1991", "2000"], "answer": "1985"},
            {"q": "¿Qué significa GNU?", 
             "options": ["Global Network Utility", "GNU's Not Unix", "General New Unix", "Great New Utility"], "answer": "GNU's Not Unix"},
            {"q": "¿Quién fundó la FSF?", 
             "options": ["Linus Torvalds", "Bill Gates", "Richard Stallman", "Steve Jobs"], "answer": "Richard Stallman"},
            {"q": "¿Qué libertad NO pertenece a las 4 libertades del software libre?", 
             "options": ["Usar el programa", "Vender el programa como propio sin código fuente", "Estudiar y modificar", "Compartir copias"], "answer": "Vender el programa como propio sin código fuente"},
            {"q": "¿Cuál es el núcleo que se unió a GNU para formar GNU/Linux?", 
             "options": ["Minix", "Unix", "Linux", "Windows NT"], "answer": "Linux"}
        ]

        if st.session_state.step < len(preguntas):
            pregunta_actual = preguntas[st.session_state.step]

            st.subheader(f"Pregunta {st.session_state.step + 1}: {pregunta_actual['q']}")
            respuesta = st.radio("Elige tu respuesta:", pregunta_actual["options"], key=f"q{st.session_state.step}")

            # Tiempo transcurrido
            tiempo_transcurrido = int(time.time() - st.session_state.start_time)
            st.progress(min(tiempo_transcurrido, 10), text=f"⏳ Tiempo: {tiempo_transcurrido}s")

            if st.button("Responder", key=f"btn{st.session_state.step}"):
                puntos = max(0, 10 - tiempo_transcurrido)  # Se reduce con el tiempo
                if respuesta == pregunta_actual["answer"]:
                    st.success(f"✅ Correcto! +{puntos} puntos")
                    st.session_state.score += puntos
                else:
                    st.error(f"❌ Incorrecto. La respuesta correcta es: {pregunta_actual['answer']}")

                st.session_state.step += 1
                st.session_state.start_time = time.time()
                st.rerun()

        else:
            st.success(f"🎉 Quiz finalizado, {st.session_state.nombre}. Tu puntaje total es: {st.session_state.score} puntos.")

            if st.button("Guardar resultado"):
                st.session_state.records.append({"Nombre": st.session_state.nombre, "Puntaje": st.session_state.score})
                st.session_state.score = 0
                st.session_state.step = 0
                st.session_state.nombre = ""
                st.success("✅ Resultado guardado en la tabla histórica.")
                st.rerun()

            if st.session_state.records:
                df = pd.DataFrame(st.session_state.records)
                st.subheader("📊 Tabla histórica de resultados")
                st.dataframe(df)
