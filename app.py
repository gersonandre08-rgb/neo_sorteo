import streamlit as st
import random
import time
import pandas as pd

# --- 1. CONFIGURACIÓN DE PÁGINA (SIEMPRE PRIMERO) ---
st.set_page_config(
    page_title="Neo Sorteo Pro: La Suerte la decides Tú",
    page_icon="⚓",
    layout="wide"
)

# --- 2. ESTILOS CSS COMPLETOS (ANIMACIONES Y DISEÑO) ---
st.markdown("""
    <style>
    /* Fondo General */
    .stApp {
        background: radial-gradient(circle at center, #1a1f26 0%, #0a0e14 100%);
    }

    /* Animación de Bolillas Flotantes en el fondo */
    .bolilla-fondo {
        position: fixed;
        background: rgba(255, 255, 255, 0.07);
        border-radius: 50%;
        z-index: -1;
        animation: flotar 15s infinite linear;
    }

    @keyframes flotar {
        0% { transform: translateY(110vh) translateX(0); opacity: 0; }
        10% { opacity: 1; }
        90% { opacity: 1; }
        100% { transform: translateY(-10vh) translateX(50px); opacity: 0; }
    }

    /* Estilo de los botones de la tómbola (Grilla) */
    .stButton>button {
        width: 100% !important;
        height: 60px !important;
        border-radius: 50% !important;
        font-weight: bold !important;
        font-size: 1.1rem !important;
        transition: all 0.3s ease;
    }

    /* Color cuando el número está OCUPADO (Rojo/Coral) */
    div[data-testid="stHorizontalBlock"] button[kind="primary"] {
        background-color: #e74c3c !important;
        border: 2px solid #ffffff !important;
        box-shadow: 0 0 15px rgba(231, 76, 60, 0.6);
    }

    /* Color cuando el número está LIBRE (Azul Oscuro) */
    div[data-testid="stHorizontalBlock"] button[kind="secondary"] {
        background-color: #1c2833 !important;
        color: #3498db !important;
        border: 1px solid #3498db !important;
    }

    /* Ajuste del Sidebar */
    [data-testid="stSidebar"] {
        background-color: rgba(10, 14, 20, 0.98) !important;
        border-right: 2px solid #3498db;
    }
    </style>

    <div class="bolilla-fondo" style="width:60px; height:60px; left:5%; animation-delay:0s;"></div>
    <div class="bolilla-fondo" style="width:30px; height:30px; left:25%; animation-delay:4s;"></div>
    <div class="bolilla-fondo" style="width:80px; height:80px; left:55%; animation-delay:2s;"></div>
    <div class="bolilla-fondo" style="width:40px; height:40px; left:85%; animation-delay:8s;"></div>
    """, unsafe_allow_html=True)

# --- 3. INICIALIZACIÓN DE VARIABLES DE SESIÓN ---
if 'amigos' not in st.session_state:
    st.session_state.amigos = {} # Diccionario {numero: nombre}
if 'historial' not in st.session_state:
    st.session_state.historial = [] # Lista de ganadores
if 'editando_num' not in st.session_state:
    st.session_state.editando_num = None

# --- 4. FUNCIONES DE APOYO ---
def procesar_guardado(n, nom):
    st.session_state.amigos[n] = nom
    st.session_state.editando_num = None

def procesar_borrado(n):
    if n in st.session_state.amigos:
        del st.session_state.amigos[n]
    st.session_state.editando_num = None

# --- 5. SIDEBAR: GESTIÓN DE PARTICIPANTES ---
with st.sidebar:
    st.image("https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExNHJpbm56amZidGpxbmZueWZueWZueWZueWZueWZueWZueWZueWZueZ/3o7TKVUn7iM8FMEU24/giphy.gif", width=150)
    st.title("⚓ Panel de Control")
    st.markdown("---")

    # Formulario dinámico (Cambia entre Registro y Edición)
    num_fijado = st.session_state.editando_num
    titulo_accion = f"✏️ Editando Número {num_fijado}" if num_fijado else "📝 Nuevo Registro"
    
    with st.form("form_gestion", clear_on_submit=True):
        st.subheader(titulo_accion)
        nombre_input = st.text_input("Nombre del Amigo", 
                                     value=st.session_state.amigos.get(num_fijado, "") if num_fijado else "")
        numero_input = st.number_input("Número Elegido", 1, 50, 
                                       value=num_fijado if num_fijado else 1)
        
        c1, c2 = st.columns(2)
        with c1:
            btn_guardar = st.form_submit_button("✅ Guardar")
        with c2:
            btn_borrar = st.form_submit_button("🗑️ Eliminar") if num_fijado else None

        if btn_guardar and nombre_input:
            procesar_guardado(numero_input, nombre_input)
            st.rerun()
        
        if btn_borrar:
            procesar_borrado(num_fijado)
            st.rerun()

    st.markdown("---")
    st.subheader("🏆 Ganadores Anteriores")
    if st.session_state.historial:
        for item in reversed(st.session_state.historial):
            st.write(f"🌟 **#{item['num']}** - {item['nom']}")
    else:
        st.caption("Aún no hay ganadores.")

    if st.button("🚨 Reiniciar Base de Datos"):
        st.session_state.amigos = {}
        st.session_state.historial = []
        st.session_state.editando_num = None
        st.rerun()

# --- 6. PANEL PRINCIPAL: GRILLA INTERACTIVA ---
st.title("🎰 Neo Sorteo: ¡La Suerte la decides tú!")
st.write("Selecciona un número de la tómbola para registrar o modificar datos.")

st.subheader("📊 Estado de la Tabla (1-50)")
# Generamos la grilla de 10 columnas x 5 filas
for fila in range(5):
    cols = st.columns(10)
    for columna in range(10):
        numero_celda = fila * 10 + columna + 1
        with cols[columna]:
            # Si el número está registrado, botón ROJO (primary)
            if numero_celda in st.session_state.amigos:
                if st.button(f"{numero_celda}", key=f"btn_{numero_celda}", type="primary", 
                             help=f"Registrado a: {st.session_state.amigos[numero_celda]}"):
                    st.session_state.editando_num = numero_celda
                    st.rerun()
            # Si está libre, botón AZUL (secondary)
            else:
                if st.button(f"{numero_celda}", key=f"btn_{numero_celda}", type="secondary"):
                    st.session_state.editando_num = numero_celda
                    st.rerun()

st.markdown("---")

# --- 7. SECCIÓN DE SORTEO (CHOCOLATEO CON GIFS) ---
if len(st.session_state.amigos) > 0:
    st.subheader("🎲 ¡Es hora del Chocolateo!")
    if st.button("🔥 ¡GIRAR TÓMBOLA AHORA!", use_container_width=True):
        
        # Áreas de visualización dinámica
        espacio_gif = st.empty()
        espacio_numero = st.empty()
        
        # 1. Mostrar GIF de tómbola girando
        espacio_gif.image("https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExNHJpbm56amZidGpxbmZueWZueWZueWZueWZueWZueWZueWZueWZueZ/l41lTfuxV5N97S99e/giphy.gif")
        
        # 2. Animación de números aleatorios (Suspenso)
        lista_participantes = list(st.session_state.amigos.keys())
        for i in range(35):
            n_azar = random.choice(lista_participantes)
            color_text = "#f1c40f" if i > 25 else "#ffffff"
            espacio_numero.markdown(f"<h1 style='text-align:center; font-size:100px; color:{color_text};'>🎲 {n_azar}</h1>", unsafe_allow_html=True)
            time.sleep(0.06 + (i/300)) # Se ralentiza gradualmente
        
        # 3. Resultado Final
        ganador_final = random.choice(lista_participantes)
        nombre_ganador = st.session_state.amigos[ganador_final]
        
        # Registrar en historial
        st.session_state.historial.append({"num": ganador_final, "nom": nombre_ganador})
        
        # Limpiar y mostrar pantalla de victoria
        espacio_gif.empty()
        st.balloons()
        espacio_numero.markdown(f"""
            <div style="background: linear-gradient(135deg, #f1c40f 0%, #f39c12 100%); 
                        padding: 60px; border-radius: 35px; text-align: center; color: #1a1a1a;
                        box-shadow: 0 15px 50px rgba(243, 156, 18, 0.5); border: 5px solid #fff;">
                <img src="https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExNHJpbm56amZidGpxbmZueWZueWZueWZueWZueWZueWZueWZueWZueZ/26DOoDHe45G56u2pW/giphy.gif" width="180">
                <h1 style='margin:10px 0; font-size: 55px;'>🎉 ¡NÚMERO {ganador_final}! 🎉</h1>
                <hr style='border-color: rgba(0,0,0,0.2);'>
                <h2 style='font-size: 35px;'>¡Felicidades, <b>{nombre_ganador}</b>!</h2>
                <p style='font-size: 18px;'>La suerte te acompaña hoy.</p>
            </div>
        """, unsafe_allow_html=True)
else:
    st.warning("⚠️ Necesitas registrar al menos a un amigo para iniciar el sorteo.")

st.sidebar.caption("Neo Sorteo v4.0 | Callao 2026 | Dev: Gerson")
