import streamlit as st
import random
import time
import pandas as pd

# --- 1. CONFIGURACIÓN DE PÁGINA (Layout Ancho) ---
st.set_page_config(
    page_title="Neo Sorteo: ¡La Suerte no es una opción, el número ganador es tuyo!",
    page_icon="⚓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. ESTILOS CSS COMPLETOS (INTERFAZ CASINO PRO) ---
st.markdown("""
    <style>
    /* 2.1 Fondo de Casino Oscuro Profundo (La Tinka style) */
    .stApp {
        background: radial-gradient(circle at center, #10151f 0%, #080a10 100%);
        color: #e6edf3 !important;
    }

    /* 2.2 Títulos en Gama de Azules y Blanco */
    h1, h2, h3, h4, p {
        color: #e6edf3 !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    /* 2.3 Sidebar Estilizado (Tipo Tinka Sidebar) */
    [data-testid="stSidebar"] {
        background-color: #121826 !important;
        border-right: 2px solid #3498db;
    }

    /* 2.4 Panel de Sorteo (BOLILLAS DE BINGO CIRCULARES) */
    div[data-testid="stHorizontalBlock"] button {
        border-radius: 50% !important;
        width: 60px !important;
        height: 60px !important;
        font-weight: bold !important;
        font-size: 1.4rem !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        transition: 0.3s !important;
        box-shadow: 2px 4px 10px rgba(0,0,0,0.5) !important;
    }

    /* Bolilla OCUPADA (Roja Neón) */
    div[data-testid="stHorizontalBlock"] button[kind="primary"] {
        background-color: #f12c3c !important;
        color: white !important;
        border: 2px solid white !important;
        box-shadow: 0 0 15px rgba(241, 44, 60, 0.7) !important;
    }
    
    /* Bolilla DISPONIBLE (Blanca Bingo) */
    div[data-testid="stHorizontalBlock"] button[kind="secondary"] {
        background-color: #ffffff !important;
        color: #1a233a !important;
        border: 2px solid #3498db !important;
    }

    /* 2.5 Botones de Acción (Tipo Casino) */
    .stButton>button {
        width: 100%;
        background-color: #1d4ed8;
        color: white;
        border-radius: 12px;
        border: none;
        padding: 12px 24px;
        font-size: 18px;
        font-weight: bold;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #2563eb;
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(37, 99, 235, 0.4);
    }
    
    /* 2.6 Bloque de Ganador (Casino Celebration Style) */
    .celebracion-ganador {
        background: linear-gradient(135deg, #1d4ed8 0%, #0c204d 100%);
        padding: 40px;
        border-radius: 20px;
        text-align: center;
        border: 4px solid #f1c40f;
        box-shadow: 0 15px 40px rgba(241, 196, 15, 0.5);
    }
    .celebracion-ganador h1 { color: #f1c40f !important; margin: 0; font-size: 60px; }
    .celebracion-ganador h2 { color: white !important; margin: 10px 0; }
    
    /* 2.7 CSS para posicionar el tercer GIF en la superior derecha (FIXED) */
    .gif-superior-derecha {
        position: fixed;
        top: 60px;
        right: 20px;
        width: 110px;
        z-index: 1000;
        border-radius: 10px;
        box-shadow: 0 0 15px rgba(52, 152, 219, 0.6);
        border: 1px solid #3498db;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. INICIALIZACIÓN DE VARIABLES DE SESIÓN (PERSISTENCIA) ---
if 'amigos' not in st.session_state:
    st.session_state.amigos = {} 
if 'historial' not in st.session_state:
    st.session_state.historial = [] 
if 'editando_num' not in st.session_state:
    st.session_state.editando_num = None 

# --- 4. FUNCIONES DE APOYO (DATOS Y AUDIO) ---
def guardar_amigo(n, nom):
    st.session_state.amigos[n] = nom
    st.session_state.editando_num = None

def eliminar_amigo(n):
    if n in st.session_state.amigos:
        del st.session_state.amigos[n]
    st.session_state.editando_num = None

def reproducir_audio(url):
    st.markdown(f"""
        <audio autoplay>
            <source src="{url}" type="audio/mpeg">
        </audio>
        """, unsafe_allow_html=True)

# --- 5. SIDEBAR: PANEL DE CONTROL (GIF 1) ---
with st.sidebar:
    st.image("https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExNHRkbWRqZ2ZueWZueWZueWZueWZueWZueWZueWZueWZueWZueZ/l41lTfuxV5N97S99e/giphy.gif", width=150)
    st.title("⚓ Panel de Control")
    st.markdown("---")

    n_edit = st.session_state.editando_num
    titulo_accion = f"✏️ Editando Número {n_edit}" if n_edit else "📝 Nuevo Registro"
    
    with st.form("form_gestion", clear_on_submit=True):
        st.subheader(titulo_accion)
        nombre_input = st.text_input("Nombre del Amigo", 
                                     value=st.session_state.amigos.get(n_edit, "") if n_edit else "")
        numero_input = st.number_input("Número Elegido", 1, 50, 
                                       value=n_edit if n_edit else 1)
        
        c1, c2 = st.columns(2)
        with c1:
            if st.form_submit_button("✅ Guardar"):
                if nombre_input:
                    if not n_edit and numero_input in st.session_state.amigos:
                        st.error("⚠️ El número ya está ocupado.")
                    else:
                        guardar_amigo(numero_input, nombre_input)
                        st.rerun()
                else:
                    st.error("⚠️ Por favor, pon un nombre.")
        
        with c2:
            if n_edit: 
                if st.form_submit_button("🗑️ Eliminar"):
                    eliminar_amigo(n_edit)
                    st.rerun()

    st.markdown("---")
    st.subheader("📜 Ganadores Anteriores")
    if st.session_state.historial:
        for item in reversed(st.session_state.historial):
            st.write(f"🏆 **#{item['num']}** - {item['nom']}")
    else:
        st.caption("Aún no hay ganadores.")

    if st.button("🚨 Reiniciar Base de Datos"):
        st.session_state.amigos = {}
        st.session_state.historial = []
        st.session_state.editando_num = None
        st.rerun()

# --- 6. PANEL PRINCIPAL (GIF 3 SUPERIOR DERECHA) ---
st.markdown("""
    <img src="https://media.tenor.com/ctw2cS4i4CEAAAAM/lotto-lotto-balls.gif" class="gif-superior-derecha">
    """, unsafe_allow_html=True)

st.title("🎰 Neo Sorteo: ¡La Suerte la decides tú!")
st.write("Gestiona tus sorteos con estilo y transparencia.")

# 6.3 Grilla Interactiva (10x5) estilo Casino
st.subheader("📊 Estado de la Tómbola (1-50)")
for fila in range(5):
    cols = st.columns(10)
    for columna in range(10):
        numero_celda = fila * 10 + columna + 1
        with cols[columna]:
            if numero_celda in st.session_state.amigos:
                # Bolilla ROJA OCUPADA
                if st.button(f"{numero_celda}", key=f"btn_{numero_celda}", type="primary", 
                             help=f"Amigo: {st.session_state.amigos[numero_celda]}"):
                    st.session_state.editando_num = numero_celda
                    st.rerun()
            else:
                # Bolilla BLANCA DISPONIBLE
                if st.button(f"{numero_celda}", key=f"btn_{numero_celda}", type="secondary"):
                    st.session_state.editando_num = numero_celda
                    st.rerun()

st.markdown("---")

# --- ACTUALIZACIÓN: BOTÓN DE TRANSPARENCIA ---
with st.expander("👁️ VER LISTA DE PARTICIPANTES (TRANSPARENCIA)"):
    if st.session_state.amigos:
        df_trans = pd.DataFrame([
            {"Número": k, "Nombre": v} 
            for k, v in sorted(st.session_state.amigos.items())
        ])
        st.table(df_trans)
    else:
        st.info("No hay registros para mostrar.")

st.markdown("---")

# --- 7. EL MOMENTO DEL SORTEO (GIF 2 CHOCOLATEO Y CELEBRACIÓN) ---
if len(st.session_state.amigos) > 0:
    st.subheader("🎲 ¡Inicia el Chocolateo!")
    
    if st.button("🔥 ¡GIRAR TÓMBOLA AHORA!", use_container_width=True):
        reproducir_audio("https://www.soundjay.com/misc/sounds/bingo-ball-machine-1.mp3")
        
        espacio_gif = st.empty()
        espacio_numero = st.empty()
        
        espacio_gif.image("https://media4.giphy.com/media/v1.Y2lkPTZjMDliOTUyZThwb2FvMm94ZHl4MWl0YjZpODIwOW1yNGV0dTM4c2oybzNsbXNmNSZlcD12MV9naWZzX3NlYXJjaCZjdD1n/4RaPld0hPNRXEk1cfv/200w.gif")
        
        lista_participantes = list(st.session_state.amigos.keys())
        for i in range(35):
            n_azar = random.choice(lista_participantes)
            color_text = "#f1c40f" if i > 25 else "#ffffff"
            espacio_numero.markdown(f"<h1 style='text-align:center; font-size:100px; color:{color_text};'>🎲 {n_azar}</h1>", unsafe_allow_html=True)
            time.sleep(0.06 + (i/300)) 
        
        ganador_final = random.choice(lista_participantes)
        nombre_ganador = st.session_state.amigos[ganador_final]
        
        st.session_state.historial.append({"num": ganador_final, "nom": nombre_ganador})
        
        espacio_gif.empty()
        reproducir_audio("https://www.myinstants.com/media/sounds/drum-roll-sound-effect.mp3")
        st.balloons()
        
        espacio_numero.markdown(f"""
            <div class="celebracion-ganador">
                <img src="https://media2.giphy.com/media/v1.Y2lkPTZjMDliOTUyZThwb2FvMm94ZHl4MWl0YjZpODIwOW1yNGV0dTM4c2oybzNsbXNmNSZlcD12MV9naWZzX3NlYXJjaCZjdD1n/kfRlTZDvhLCPvOEey8/200w.gif" width="180">
                <h1 style='font-size: 55px;'>🎉 ¡NÚMERO {ganador_final}! 🎉</h1>
                <hr style='border-color: rgba(255,255,255,0.2);'>
                <h2 style='font-size: 35px;'>Felicidades, <b>{nombre_ganador}</b>!</h2>
                <p style='font-size: 18px;'>La suerte te acompaña hoy.</p>
            </div>
        """, unsafe_allow_html=True)
else:
    st.warning("⚠️ Necesitas registrar al menos a un amigo para habilitar el sorteo.")

st.sidebar.caption("Neo Sorteo v4.0 | Callao 2026 | Desarrollado por Gerson")
