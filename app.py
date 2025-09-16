import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Configuración de la página
st.set_page_config(
    page_title="Cronología de Distribuciones Linux",
    page_icon="🐧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado para el tema Linux
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
        color: #ffffff;
    }
    
    .stApp {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    }
    
    .title-container {
        background: linear-gradient(90deg, #2196F3 0%, #21CBF3 100%);
        padding: 2rem;
        border-radius: 15px;
        margin: 1rem 0;
        text-align: center;
        box-shadow: 0 8px 32px rgba(33, 150, 243, 0.3);
    }
    
    .distro-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        transition: transform 0.3s ease;
    }
    
    .distro-card:hover {
        transform: translateY(-5px);
    }
    
    .timeline-item {
        background: linear-gradient(45deg, #FF6B6B, #4ECDC4);
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        color: white;
        font-weight: bold;
    }
    
    .feature-box {
        background: rgba(76, 175, 80, 0.2);
        border-left: 4px solid #4CAF50;
        padding: 1rem;
        border-radius: 5px;
        margin: 0.5rem 0;
    }
    
    .difference-box {
        background: rgba(255, 152, 0, 0.2);
        border-left: 4px solid #FF9800;
        padding: 1rem;
        border-radius: 5px;
        margin: 0.5rem 0;
    }
    
    h1, h2, h3 {
        color: #21CBF3 !important;
    }
    
    .stSelectbox > div > div {
        background-color: rgba(255, 255, 255, 0.1);
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Título principal
st.markdown("""
<div class="title-container">
    <h1>🐧 Cronología del Desarrollo de las Distribuciones Linux</h1>
    <p style="font-size: 1.2em; margin-top: 1rem;">Un viaje a través de la evolución del ecosistema Linux</p>
</div>
""", unsafe_allow_html=True)

# Sidebar con navegación
st.sidebar.markdown("## 📋 Navegación")
seccion = st.sidebar.selectbox(
    "Selecciona una sección:",
    ["🏠 Inicio", "📅 Cronología", "🔍 Comparación de Distros", "📊 Estadísticas", "🌳 Árbol Genealógico"]
)

# Datos de las distribuciones
distros_data = {
    "Slackware": {"año": 1993, "fundador": "Patrick Volkerding", "descripción": "Una de las primeras distribuciones Linux, conocida por su estabilidad y simplicidad.", "familia": "Independiente"},
    "Debian": {"año": 1993, "fundador": "Ian Murdock", "descripción": "Base de muchas otras distribuciones, famosa por su estabilidad y sistema de paquetes APT.", "familia": "Debian"},
    "Red Hat": {"año": 1994, "fundador": "Marc Ewing", "descripción": "Distribución comercial que dio origen a muchas otras distros empresariales.", "familia": "Red Hat"},
    "SUSE": {"año": 1994, "fundador": "Roland Dyroff", "descripción": "Distribución alemana enfocada en el mercado empresarial.", "familia": "SUSE"},
    "Ubuntu": {"año": 2004, "fundador": "Mark Shuttleworth", "descripción": "Basada en Debian, popularizó Linux en el escritorio con su facilidad de uso.", "familia": "Debian"},
    "CentOS": {"año": 2004, "fundador": "Gregory Kurtzer", "descripción": "Versión gratuita de Red Hat Enterprise Linux.", "familia": "Red Hat"},
    "Fedora": {"año": 2003, "fundador": "Red Hat Inc.", "descripción": "Versión comunitaria de Red Hat con tecnologías de vanguardia.", "familia": "Red Hat"},
    "openSUSE": {"año": 2005, "fundador": "Novell", "descripción": "Versión comunitaria de SUSE Linux.", "familia": "SUSE"},
    "Arch Linux": {"año": 2002, "fundador": "Judd Vinet", "descripción": "Distribución rolling release enfocada en simplicidad y personalización.", "familia": "Independiente"},
    "Gentoo": {"año": 2002, "fundador": "Daniel Robbins", "descripción": "Distribución source-based que compila todo desde el código fuente.", "familia": "Independiente"},
    "Mint": {"año": 2006, "fundador": "Clement Lefebvre", "descripción": "Basada en Ubuntu, enfocada en facilidad de uso y multimedia.", "familia": "Debian"},
    "Elementary OS": {"año": 2011, "fundador": "Daniel Foré", "descripción": "Distribución elegante basada en Ubuntu con interfaz similar a macOS.", "familia": "Debian"},
    "Manjaro": {"año": 2011, "fundador": "Roland Singer", "descripción": "Basada en Arch Linux pero más fácil de usar.", "familia": "Arch"},
    "Kali Linux": {"año": 2013, "fundador": "Mati Aharoni", "descripción": "Distribución especializada en seguridad y hacking ético.", "familia": "Debian"},
    "Pop!_OS": {"año": 2017, "fundador": "System76", "descripción": "Basada en Ubuntu, optimizada para gaming y desarrollo.", "familia": "Debian"}
}

if seccion == "🏠 Inicio":
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        <div class="distro-card">
        <h2>¿Qué es una Distribución Linux? 🤔</h2>
        <p>Una distribución Linux (o "distro") es un sistema operativo basado en el kernel Linux que incluye:</p>
        
        <div class="feature-box">
        • <strong>Kernel Linux:</strong> El núcleo del sistema operativo<br>
        • <strong>Software del sistema:</strong> Herramientas básicas y utilidades<br>
        • <strong>Gestor de paquetes:</strong> Sistema para instalar/actualizar software<br>
        • <strong>Entorno de escritorio:</strong> Interfaz gráfica de usuario<br>
        • <strong>Aplicaciones:</strong> Programas preinstalados
        </div>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown("""
        <div class="distro-card">
        <h3>📈 Estadísticas Rápidas</h3>
        """, unsafe_allow_html=True)
        
        st.metric("Distribuciones activas", "600+", "🔥")
        st.metric("Años desde la primera", "31", "📅")
        st.metric("Familias principales", "6", "🌳")
        
        st.markdown("</div>", unsafe_allow_html=True)

elif seccion == "📅 Cronología":
    st.markdown("## 📅 Línea Temporal del Desarrollo de Linux")
    
    # Crear timeline interactivo
    df_timeline = pd.DataFrame([
        {"Distro": distro, "Año": info["año"], "Fundador": info["fundador"], "Familia": info["familia"]} 
        for distro, info in distros_data.items()
    ])
    
    fig = px.scatter(df_timeline, x="Año", y="Distro", color="Familia", size_max=20,
                     hover_data=["Fundador"], title="Evolución de las Distribuciones Linux")
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='white',
        height=600
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Eventos importantes por década
    st.markdown("### 🎯 Eventos Importantes por Década")
    
    decadas = {
        "1990s": [
            "1991: Linus Torvalds lanza el kernel Linux",
            "1993: Nacen Slackware y Debian",
            "1994: Red Hat y SUSE inician operaciones",
            "1998: Se acuña el término 'Open Source'"
        ],
        "2000s": [
            "2002: Gentoo y Arch Linux aparecen",
            "2003: Fedora se independiza de Red Hat",
            "2004: Ubuntu revoluciona Linux desktop",
            "2006: Linux Mint ofrece multimedia out-of-box"
        ],
        "2010s": [
            "2011: Elementary OS y Manjaro democratizan el diseño",
            "2013: Kali Linux unifica herramientas de seguridad",
            "2017: Pop!_OS optimiza para gaming",
            "2019: Microsoft lanza WSL2 con kernel Linux real"
        ]
    }
    
    for decada, eventos in decadas.items():
        st.markdown(f"#### {decada}")
        for evento in eventos:
            st.markdown(f'<div class="timeline-item">{evento}</div>', unsafe_allow_html=True)

elif seccion == "🔍 Comparación de Distros":
    st.markdown("## 🔍 Comparación Detallada de Distribuciones")
    
    # Selector de distribuciones para comparar
    distros_seleccionadas = st.multiselect(
        "Selecciona las distribuciones a comparar:",
        list(distros_data.keys()),
        default=["Ubuntu", "Fedora", "Arch Linux"]
    )
    
    if distros_seleccionadas:
        # Tabla comparativa
        comparacion_data = []
        for distro in distros_seleccionadas:
            info = distros_data[distro]
            comparacion_data.append({
                "Distribución": distro,
                "Año": info["año"],
                "Fundador": info["fundador"],
                "Familia": info["familia"],
                "Descripción": info["descripción"]
            })
        
        df_comparacion = pd.DataFrame(comparacion_data)
        st.dataframe(df_comparacion, use_container_width=True)
        
        # Características técnicas detalladas
        st.markdown("### ⚙️ Características Técnicas")
        
        caracteristicas = {
            "Ubuntu": {
                "Gestor de paquetes": "APT (Advanced Package Tool)",
                "Ciclo de lanzamiento": "6 meses (LTS cada 2 años)",
                "Entorno predeterminado": "GNOME",
                "Filosofía": "Linux para seres humanos",
                "Uso recomendado": "Escritorio, servidores, principiantes"
            },
            "Fedora": {
                "Gestor de paquetes": "DNF (Dandified YUM)",
                "Ciclo de lanzamiento": "6 meses",
                "Entorno predeterminado": "GNOME",
                "Filosofía": "Innovación y tecnologías de vanguardia",
                "Uso recomendado": "Desarrolladores, usuarios avanzados"
            },
            "Arch Linux": {
                "Gestor de paquetes": "Pacman",
                "Ciclo de lanzamiento": "Rolling release",
                "Entorno predeterminado": "Ninguno (instalación mínima)",
                "Filosofía": "Simplicidad y control total del usuario",
                "Uso recomendado": "Usuarios expertos, personalización extrema"
            },
            "Debian": {
                "Gestor de paquetes": "APT",
                "Ciclo de lanzamiento": "2-3 años",
                "Entorno predeterminado": "GNOME",
                "Filosofía": "Software libre universal",
                "Uso recomendado": "Servidores, estabilidad crítica"
            },
            "Mint": {
                "Gestor de paquetes": "APT",
                "Ciclo de lanzamiento": "Basado en Ubuntu LTS",
                "Entorno predeterminado": "Cinnamon",
                "Filosofía": "Elegante, moderno, cómodo",
                "Uso recomendado": "Transición desde Windows"
            }
        }
        
        for distro in distros_seleccionadas:
            if distro in caracteristicas:
                st.markdown(f"#### {distro}")
                caract = caracteristicas[distro]
                
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f'<div class="difference-box"><strong>Gestor de paquetes:</strong> {caract["Gestor de paquetes"]}</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="difference-box"><strong>Ciclo de lanzamiento:</strong> {caract["Ciclo de lanzamiento"]}</div>', unsafe_allow_html=True)
                
                with col2:
                    st.markdown(f'<div class="difference-box"><strong>Entorno predeterminado:</strong> {caract["Entorno predeterminado"]}</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="difference-box"><strong>Filosofía:</strong> {caract["Filosofía"]}</div>', unsafe_allow_html=True)
                
                st.markdown(f'<div class="feature-box"><strong>Uso recomendado:</strong> {caract["Uso recomendado"]}</div>', unsafe_allow_html=True)

elif seccion == "📊 Estadísticas":
    st.markdown("## 📊 Estadísticas y Análisis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Gráfico de distribución por familia
        familias_count = {}
        for distro, info in distros_data.items():
            familia = info["familia"]
            familias_count[familia] = familias_count.get(familia, 0) + 1
        
        fig_familias = px.pie(
            values=list(familias_count.values()),
            names=list(familias_count.keys()),
            title="Distribución por Familias"
        )
        fig_familias.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white'
        )
        st.plotly_chart(fig_familias, use_container_width=True)
    
    with col2:
        # Gráfico de distribuciones por década
        decadas_count = {"1990s": 0, "2000s": 0, "2010s": 0}
        for distro, info in distros_data.items():
            año = info["año"]
            if año < 2000:
                decadas_count["1990s"] += 1
            elif año < 2010:
                decadas_count["2000s"] += 1
            else:
                decadas_count["2010s"] += 1
        
        fig_decadas = px.bar(
            x=list(decadas_count.keys()),
            y=list(decadas_count.values()),
            title="Nuevas Distribuciones por Década",
            color=list(decadas_count.values()),
            color_continuous_scale="Viridis"
        )
        fig_decadas.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white',
            showlegend=False
        )
        st.plotly_chart(fig_decadas, use_container_width=True)
    
    # Popularidad estimada
    st.markdown("### 🏆 Popularidad Estimada (DistroWatch Rankings)")
    
    popularidad_data = {
        "Ubuntu": 2500,
        "Mint": 2200,
        "Debian": 1800,
        "Fedora": 1500,
        "openSUSE": 1200,
        "Arch Linux": 1100,
        "Manjaro": 1000,
        "Elementary OS": 800,
        "Pop!_OS": 600,
        "Kali Linux": 500
    }
    
    fig_popularidad = px.bar(
        x=list(popularidad_data.keys()),
        y=list(popularidad_data.values()),
        title="Hits por Día en DistroWatch (Estimado)",
        color=list(popularidad_data.values()),
        color_continuous_scale="Blues"
    )
    fig_popularidad.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='white',
        showlegend=False,
        xaxis_tickangle=-45
    )
    st.plotly_chart(fig_popularidad, use_container_width=True)

elif seccion == "🌳 Árbol Genealógico":
    st.markdown("## 🌳 Árbol Genealógico de las Distribuciones")
    
    st.markdown("""
    <div class="distro-card">
    <h3>Familia Debian (APT)</h3>
    <p>📦 Gestor de paquetes: APT/DPKG</p>
    <div style="margin-left: 20px;">
        🌱 <strong>Debian (1993)</strong><br>
        ├── 🍃 <strong>Ubuntu (2004)</strong><br>
        │   ├── 🌿 Linux Mint (2006)<br>
        │   ├── 🎨 Elementary OS (2011)<br>
        │   └── 🚀 Pop!_OS (2017)<br>
        └── 🔒 Kali Linux (2013)
    </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="distro-card">
    <h3>Familia Red Hat (RPM)</h3>
    <p>📦 Gestor de paquetes: YUM/DNF</p>
    <div style="margin-left: 20px;">
        🎩 <strong>Red Hat (1994)</strong><br>
        ├── 🔴 Red Hat Enterprise Linux (RHEL)<br>
        │   └── 🏢 CentOS (2004)<br>
        └── 🎓 Fedora (2003)
    </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="distro-card">
    <h3>Familia SUSE (RPM)</h3>
    <p>📦 Gestor de paquetes: Zypper/RPM</p>
    <div style="margin-left: 20px;">
        🦎 <strong>SUSE (1994)</strong><br>
        ├── 💼 SUSE Linux Enterprise<br>
        └── 🌐 openSUSE (2005)
    </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="distro-card">
    <h3>Familia Arch (Pacman)</h3>
    <p>📦 Gestor de paquetes: Pacman</p>
    <div style="margin-left: 20px;">
        🏛️ <strong>Arch Linux (2002)</strong><br>
        └── 🌊 Manjaro (2011)
    </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="distro-card">
    <h3>Distribuciones Independientes</h3>
    <div style="margin-left: 20px;">
        🛡️ <strong>Slackware (1993)</strong> - Portage<br>
        ⚗️ <strong>Gentoo (2002)</strong> - Emerge/Portage<br>
        🐧 <strong>Linux From Scratch (LFS)</strong> - Manual
    </div>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("""
<div style="margin-top: 3rem; padding: 2rem; background: rgba(0,0,0,0.3); border-radius: 15px; text-align: center;">
    <h4>🐧 ¡Explora el mundo de Linux!</h4>
    <p>Cada distribución tiene su propósito y comunidad. La diversidad es la fortaleza del ecosistema Linux.</p>
    <p><em>"Linux is not just an operating system, it's a philosophy of freedom and collaboration."</em></p>
</div>
""", unsafe_allow_html=True)
