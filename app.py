import streamlit as st
import random
import time
import pandas as pd

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="Neo Sorteo: La Suerte del Callao",
    page_icon="⚓",
    layout="wide"
)

# --- ESTILOS CSS (FONDO INTERACTIVO Y GRILLA) ---
st.markdown("""
    <style>
    /* Fondo con Gradiente Radial Profundo */
    .stApp {
        background: radial-gradient(circle at center, #1a1f26 0%, #0a0e14 100%);
    }

    /* Animación de Bolillas Flotantes */
    .bolilla-fondo {
        position: fixed;
        width: 40px; 
        height: 40px;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 50%;
        z-index: -1;
        animation: flotar 15s infinite linear;
    }

    @keyframes flotar {
        from { transform: translateY(110vh); }
        to { transform: translateY(-10vh); }
    }

    /* Estilo de la Grilla de Números */
    .numero-celda {
        display: inline-block;
        width: 60px; 
        height: 60px;
        line-height: 60px;
        margin: 8px;
        border-radius: 50%;
        text-align: center;
        font-weight: bold;
        font-size: 1.2rem;
        transition: 0.3s;
    }

    .ocupado { 
        background-color: #e74c3c; 
        color: white; 
        box-shadow: 0 0 15px rgba(231, 76, 60, 0.6); 
        border: 2px solid #ff7675;
    }

    .disponible { 
        background-color: #2c3e50; 
        color: #3498db; 
        border: 1px solid #3498db; 
        opacity: 0.7;
    }

    /* Sidebar Estilizado */
    [data-testid="stSidebar"] {
        background-color: rgba(15, 23, 42, 0.95) !important;
        border-right: 1px solid #1e293b;
    }
    </style>

    <div class="bolilla-fondo" style="left:10%; animation-delay:0s;"></div>
    <div class="bolilla-fondo" style="left:35%; animation-delay:5s; width:20px; height:20px;"></div>
    <div class="bolilla-fondo" style="left:60%; animation-delay:2s; width:50px; height:50px;"></div>
    <div class="bolilla-fondo" style="left:85%; animation-delay:8s;"></div>
    """, unsafe_allow_html=True)

# --- INICIALIZACIÓN DE DATOS ---
if 'participantes' not in st.session_state:
    st.session_state.participantes = {} # Diccionario {numero: nombre}

# --- SIDEBAR: PANEL DE CONTROL ---
with st.sidebar:
    st.markdown("## ⚓ Panel de Control")
    st.image("https://cdn-icons-png.flaticon.com/512/5111/5111162.png", width=80)
    
    with st.form("registro_vecino", clear_on_submit=True):
        st.subheader("📝 Registrar Vecino")
        nombre_input = st.text_input("Nombre Completo")
        numero_input = st.number_input("Número Elegido (1-50)", 1, 50, step=1)
        submit_btn = st.form_submit_button("✅ Registrar Número")
        
        if submit_btn:
            if not nombre_input:
                st.error("Por favor, ingresa un nombre.")
            elif numero_input in st.session_state.participantes:
                st.error(f"¡El número {numero_input} ya está ocupado!")
            else:
                st.session_state.participantes[numero_input] = nombre_input
                st.success(f"¡Registrado: {nombre_input} en el {numero_input}!")

    st.markdown("---")
    if st.button("🚨 Reiniciar Sorteo"):
        st.session_state.participantes = {}
        st.rerun()

# --- CUERPO PRINCIPAL ---
st.title("🎰 Neo Sorteo: ¡La Suerte del Callao!")
st.write("Gestiona tus sorteos con estilo y transparencia.")

# Sección 1: Visualización de Números Ocupados (Grilla 1-50)
st.subheader("📊 Estado de la Tabla")
cols = st.columns(10)
for i in range(1, 51):
    with cols[(i-1) % 10]:
        if i in st.session_state.participantes:
            nombre_v = st.session_state.participantes[i]
            st.markdown(f'<div class="numero-celda ocupado" title="Dueño: {nombre_v}">{i}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="numero-celda disponible">{i}</div>', unsafe_allow_html=True)

st.markdown("---")

# Sección 2: El Sorteo Real
if st.session_state.participantes:
    st.subheader("🎲 ¡Inicia el Chocolateo!")
    if st.button("🔥 ¡GIRAR LA TÓMBOLA!"):
        placeholder_anim = st.empty()
        numeros_en_juego = list(st.session_state.participantes.keys())
        
        # Efecto de suspenso (2 segundos de giro rápido)
        for _ in range(30):
            n_temp = random.choice(numeros_en_juego)
            placeholder_anim.markdown(f"<h1 style='text-align: center; color: #f1c40f;'>🎲 {n_temp}...</h1>", unsafe_allow_html=True)
            time.sleep(0.06)
        
        # Selección final
        ganador_n = random.choice(numeros_en_juego)
        ganador_nom = st.session_state.participantes[ganador_n]
        
        st.balloons()
        placeholder_anim.markdown(f"""
            <div style="background: linear-gradient(135deg, #f1c40f 0%, #f39c12 100%); 
                        padding: 30px; border-radius: 20px; text-align: center; color: black;
                        box-shadow: 0 10px 30px rgba(241, 196, 15, 0.4);">
                <h1 style='margin:0;'>🎉 ¡GANADOR: NÚMERO {ganador_n}! 🎉</h1>
                <hr style='border-color: black;'>
                <h2 style='margin:10px 0;'>Felicidades, {ganador_nom}</h2>
            </div>
        """, unsafe_allow_html=True)
else:
    st.info("💡 Comienza registrando vecinos en el panel de la izquierda para activar el sorteo.")

# Pie de página
st.markdown("---")
st.caption("Neo Sorteo v2.5 | Callao 2026 | Desarrollado para Gerson")
