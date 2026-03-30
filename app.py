import streamlit as st
import random
import time
import pandas as pd
from streamlit_gsheets import GSheetsConnection

# --- 1. CONFIGURACIÓN DE PÁGINA (Layout Ancho) ---
st.set_page_config(
    page_title="Neo Sorteo: ¡La Suerte no es una opción, el número ganador es tuyo!",
    page_icon="⚓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. CONEXIÓN A GOOGLE SHEETS (PERSISTENCIA TOTAL) ---
# Se requiere configurar el link del Excel en los secrets de Streamlit
conn = st.connection("gsheets", type=GSheetsConnection)

def leer_datos():
    try:
        df = conn.read(ttl="1s")
        if df.empty:
            return pd.DataFrame(columns=["Numero", "Nombre"])
        return df
    except Exception:
        return pd.DataFrame(columns=["Numero", "Nombre"])

def guardar_registro(n, nom):
    df = leer_datos()
    df = df[df["Numero"].astype(int) != int(n)]
    nuevo = pd.DataFrame([{"Numero": int(n), "Nombre": nom}])
    df_final = pd.concat([df, nuevo], ignore_index=True)
    conn.update(data=df_final)

def borrar_registro(n):
    df = leer_datos()
    df_final = df[df["Numero"].astype(int) != int(n)]
    conn.update(data=df_final)

# --- 3. ESTILOS CSS COMPLETOS (INTERFAZ CASINO PRO + KEYCAPS) ---
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

    /* 2.3 Sidebar Estilizado */
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

    /* 2.5 BOTONES DE ACCIÓN - ESTILO TECLA RECTANGULAR (KEYCAP) */
    .stButton>button {
        width: 100%;
        background-color: #1d4ed8 !important;
        color: white !important;
        border-radius: 10px !important;
        border: 1px solid #3498db !important;
        border-bottom: 6px solid #0c204d !important;
        padding: 12px 24px;
        font-size: 18px;
        font-weight: bold;
        transition: 0.1s;
    }

    /* Efecto al presionar la tecla */
    .stButton>button:active {
        border-bottom: 2px solid #0c204d !important;
        transform: translateY(4px);
    }

    /* Ajuste específico para botones en el Sidebar (Ahora Rectangulares) */
    section[data-testid="stSidebar"] .stButton>button {
        border-radius: 8px !important;
        font-size: 0.85rem !important;
        padding: 8px !important;
        height: auto !important;
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
    
    /* 2.7 CSS PARA GIF SUPERIOR DERECHA */
    .gif-superior-derecha {
        position: fixed;
        top: 100px;
        right: 30px;
        width: 150px;
        height: auto;
        z-index: 1000;
        border-radius: 15px;
        box-shadow: 0 0 20px rgba(52, 152, 219, 0.6);
        border: 2px solid #3498db;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 4. INICIALIZACIÓN DE VARIABLES DE SESIÓN ---
if 'historial' not in st.session_state:
    st.session_state.historial = [] 
if 'editando_num' not in st.session_state:
    st.session_state.editando_num = None 

# --- 5. FUNCIONES DE APOYO ---
def reproducir_audio(url):
    st.markdown(f"""
        <audio autoplay>
            <source src="{url}" type="audio/mpeg">
        </audio>
        """, unsafe_allow_html=True)

# Cargar datos desde Google Sheets
df_nube = leer_datos()
amigos_dict = dict(zip(df_nube["Numero"].astype(int), df_nube["Nombre"]))

# --- 6. SIDEBAR: PANEL DE CONTROL ---
with st.sidebar:
    st.image("https://media.tenor.com/o8bWC-23Vy4AAAAM/bingo.gif", width=180)
    st.title("⚓ Panel de Control")
    st.markdown("---")

    n_edit = st.session_state.editando_num
    titulo_accion = f"✏️ Editando Número {n_edit}" if n_edit else "📝 Nuevo Registro"
    
    with st.form("form_gestion", clear_on_submit=True):
        st.subheader(titulo_accion)
        nombre_input = st.text_input("Nombre del Amigo", 
                                     value=amigos_dict.get(n_edit, "") if n_edit else "")
        numero_input = st.number_input("Número Elegido", 1, 50, 
                                       value=n_edit if n_edit else 1)
        
        c1, c2 = st.columns(2)
        with c1:
            if st.form_submit_button("💾 GUARDAR"):
                if nombre_input:
                    guardar_registro(numero_input, nombre_input)
                    st.session_state.editando_num = None
                    st.rerun()
                else:
                    st.error("⚠️ Por favor, pon un nombre.")
        
        with c2:
            if n_edit: 
                if st.form_submit_button("🗑️ BORRAR"):
                    borrar_registro(n_edit)
                    st.session_state.editando_num = None
                    st.rerun()

    st.markdown("---")
    st.subheader("📜 Ganadores Anteriores")
    if st.session_state.historial:
        for item in reversed(st.session_state.historial):
            st.write(f"🏆 **#{item['num']}** - {item['nom']}")
    else:
        st.caption("Aún no hay ganadores.")

    if st.button("🚨 Reiniciar Sorteo (Historial)"):
        st.session_state.historial = []
        st.rerun()

# --- 7. PANEL PRINCIPAL ---
st.markdown("""
    <img src="https://media.tenor.com/ctw2cS4i4CEAAAAM/lotto-lotto-balls.gif" class="gif-superior-derecha">
    """, unsafe_allow_html=True)

st.title("🎰 Neo Sorteo: ¡La Suerte la decides tú!")
st.write("Gestiona tus sorteos con estilo y persistencia en la nube.")

# 7.1 Grilla Interactiva (10x5)
st.subheader("📊 Estado de la Tómbola (1-50)")
for fila in range(5):
    cols = st.columns(10)
    for columna in range(10):
        numero_celda = fila * 10 + columna + 1
        with cols[columna]:
            if numero_celda in amigos_dict:
                if st.button(f"{numero_celda}", key=f"btn_{numero_celda}", type="primary", 
                             help=f"Amigo: {amigos_dict[numero_celda]}"):
                    st.session_state.editando_num = numero_celda
                    st.rerun()
            else:
                if st.button(f"{numero_celda}", key=f"btn_{numero_celda}", type="secondary"):
                    st.session_state.editando_num = numero_celda
                    st.rerun()

st.markdown("---")

# 7.2 Botón de Transparencia
with st.expander("👁️ VER LISTA DE PARTICIPANTES (TRANSPARENCIA)"):
    if amigos_dict:
        df_trans = pd.DataFrame([
            {"Número": k, "Nombre": v} 
            for k, v in sorted(amigos_dict.items())
        ])
        st.table(df_trans)
    else:
        st.info("No hay registros para mostrar.")

st.markdown("---")

# --- 8. EL MOMENTO DEL SORTEO (LÓGICA DE EXTRACCIÓN ÚNICA) ---
if len(amigos_dict) > 0:
    # FILTRO DE EXTRACCIÓN ÚNICA
    ganadores_previos = [item['num'] for item in st.session_state.historial]
    participantes_disponibles = [n for n in amigos_dict.keys() if n not in ganadores_previos]

    if not participantes_disponibles:
        st.info("🎊 ¡Todos los participantes registrados ya ganaron! Reinicia el historial para una nueva ronda.")
    else:
        st.subheader(f"🎲 ¡Inicia el Chocolateo! ({len(participantes_disponibles)} bolillas en juego)")
        
        if st.button("🔥 ¡GIRAR TÓMBOLA AHORA!", use_container_width=True):
            reproducir_audio("https://www.soundjay.com/misc/sounds/bingo-ball-machine-1.mp3")
            
            espacio_gif = st.empty()
            espacio_numero = st.empty()
            
            espacio_gif.image("https://media4.giphy.com/media/v1.Y2lkPTZjMDliOTUyZThwb2FvMm94ZHl4MWl0YjZpODIwOW1yNGV0dTM4c2oybzNsbXNmNSZlcD12MV9naWZzX3NlYXJjaCZjdD1n/4RaPld0hPNRXEk1cfv/200w.gif")
            
            # Chocolateo visual (usamos a todos para la emoción)
            lista_para_animar = list(amigos_dict.keys())
            for i in range(35):
                n_azar = random.choice(lista_para_animar)
                color_text = "#f1c40f" if i > 25 else "#ffffff"
                espacio_numero.markdown(f"<h1 style='text-align:center; font-size:100px; color:{color_text};'>🎲 {n_azar}</h1>", unsafe_allow_html=True)
                time.sleep(0.06 + (i/300)) 
            
            # GANADOR REAL (Solo de los que no han ganado)
            ganador_final = random.choice(participantes_disponibles)
            nombre_ganador = amigos_dict[ganador_final]
            
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
                    <p style='font-size: 18px;'>La suerte te acompaña hoy. Este número sale de la tómbola.</p>
                </div>
            """, unsafe_allow_html=True)
else:
    st.warning("⚠️ Necesitas registrar al menos a un amigo para habilitar el sorteo.")

st.sidebar.caption("Neo Sorteo v4.5 | Callao 2026 | Cloud Persistence")
