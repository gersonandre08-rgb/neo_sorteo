import streamlit as st
import random
import time
import pandas as pd

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="Neo Sorteo Pro: Tú decides si eres un ganador",
    page_icon="⚓",
    layout="wide"
)

# --- ESTILOS CSS AVANZADOS (INTERFAZ Y ANIMACIÓN) ---
st.markdown("""
    <style>
    /* Fondo con gradiente y bolillas animadas */
    .stApp {
        background: radial-gradient(circle at center, #1a1f26 0%, #0a0e14 100%);
        overflow: hidden;
    }

    .bolilla-fondo {
        position: fixed;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 50%;
        z-index: -1;
        animation: flotar 15s infinite linear;
    }

    @keyframes flotar {
        from { transform: translateY(110vh) translateX(0); }
        to { transform: translateY(-10vh) translateX(30px); }
    }

    /* Grilla de números interactiva */
    .stButton>button {
        width: 100%;
        height: 60px;
        border-radius: 50% !important;
        font-weight: bold !important;
        font-size: 1.2rem !important;
        transition: 0.3s !important;
    }

    /* Estilos para estados de botón */
    div[data-testid="stHorizontalBlock"] button[kind="primary"] {
        background-color: #e74c3c !important; /* Rojo para ocupado */
        border: 2px solid #fff !important;
        box-shadow: 0 0 15px rgba(231, 76, 60, 0.5);
    }

    div[data-testid="stHorizontalBlock"] button[kind="secondary"] {
        background-color: #2c3e50 !important; /* Oscuro para libre */
        color: #3498db !important;
        border: 1px solid #3498db !important;
    }

    /* Sidebar estilizado */
    [data-testid="stSidebar"] {
        background-color: rgba(15, 23, 42, 0.95) !important;
        border-right: 2px solid #1d4ed8;
    }
    </style>

    <div class="bolilla-fondo" style="width:50px; height:50px; left:10%; animation-delay:0s;"></div>
    <div class="bolilla-fondo" style="width:30px; height:30px; left:35%; animation-delay:5s;"></div>
    <div class="bolilla-fondo" style="width:70px; height:70px; left:60%; animation-delay:2s;"></div>
    <div class="bolilla-fondo" style="width:40px; height:40px; left:85%; animation-delay:8s;"></div>
    """, unsafe_allow_html=True)

# --- INICIALIZACIÓN DE ESTADOS ---
if 'amigos' not in st.session_state:
    st.session_state.amigos = {} # {numero: nombre}
if 'historial' not in st.session_state:
    st.session_state.historial = []
if 'editando_num' not in st.session_state:
    st.session_state.editando_num = None

# --- LÓGICA DE PERSISTENCIA ---
def guardar_amigo(num, nombre):
    st.session_state.amigos[num] = nombre
    st.session_state.editando_num = None

def eliminar_amigo(num):
    if num in st.session_state.amigos:
        del st.session_state.amigos[num]
    st.session_state.editando_num = None

# --- SIDEBAR: GESTIÓN DE AMIGOS ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/5111/5111162.png", width=100)
    st.title("⚓ Panel de Control")
    st.markdown("---")

    # Formulario dinámico de Registro/Edición
    num_a_editar = st.session_state.editando_num
    titulo_form = f"✏️ Editando # {num_a_editar}" if num_a_editar else "📝 Nuevo Registro"
    
    with st.form("form_registro", clear_on_submit=True):
        st.subheader(titulo_form)
        nombre_input = st.text_input("Nombre del Amigo", 
                                     value=st.session_state.amigos.get(num_a_editar, "") if num_a_editar else "")
        numero_input = st.number_input("Número Elegido", 1, 50, 
                                       value=num_a_editar if num_a_editar else 1)
        
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            if st.form_submit_button("✅ Guardar"):
                if nombre_input:
                    if not num_a_editar and numero_input in st.session_state.amigos:
                        st.error("Número ya ocupado")
                    else:
                        guardar_amigo(numero_input, nombre_input)
                        st.rerun()
        with col_f2:
            if num_a_editar:
                if st.form_submit_button("🗑️ Borrar"):
                    eliminar_amigo(num_a_editar)
                    st.rerun()

    st.markdown("---")
    st.subheader("📜 Historial de Ganadores")
    for g in reversed(st.session_state.historial):
        st.write(f"🏆 **#{g['num']}** - {g['nom']}")

    if st.button("🚨 Reiniciar Todo el Sistema"):
        st.session_state.amigos = {}
        st.session_state.historial = []
        st.session_state.editando_num = None
        st.rerun()

# --- PANEL PRINCIPAL ---
st.title("🎰 Neo Sorteo: ¡La Suerte la decides tú!")
st.write("Haz clic en un número para **registrar o editar** a un amigo.")

# GRILLA INTERACTIVA (10x5)
st.subheader("📊 Estado de la Tómbola")
for fila in range(5):
    cols = st.columns(10)
    for columna in range(10):
        n = fila * 10 + columna + 1
        with cols[columna]:
            if n in st.session_state.amigos:
                # Botón ROJO si está ocupado
                if st.button(f"{n}", key=f"n_{n}", type="primary", help=f"Amigo: {st.session_state.amigos[n]}"):
                    st.session_state.editando_num = n
                    st.rerun()
            else:
                # Botón AZUL/OSCURO si está libre
                if st.button(f"{n}", key=f"n_{n}", type="secondary"):
                    st.session_state.editando_num = n
                    st.rerun()

st.markdown("---")

# --- SECCIÓN DE CHOCOLATEO ---
if st.session_state.amigos:
    st.subheader("🎲 ¡Inicia el Chocolateo!")
    if st.button("🔥 ¡GIRAR TÓMBOLA!"):
        placeholder_anim = st.empty()
        nums_activos = list(st.session_state.amigos.keys())
        
        # Animación de suspenso
        for i in range(40):
            n_temp = random.choice(nums_activos)
            color = "#f1c40f" if i > 30 else "#ffffff"
            placeholder_anim.markdown(f"""
                <h1 style='text-align: center; font-size: 80px; color: {color};'>
                    🎲 {n_temp}
                </h1>
            """, unsafe_allow_html=True)
            time.sleep(0.05 + (i/200)) # Se vuelve más lento al final
        
        # Resultado final
        ganador_n = random.choice(nums_activos)
        ganador_nom = st.session_state.amigos[ganador_n]
        
        # Guardar en historial
        st.session_state.historial.append({"num": ganador_n, "nom": ganador_nom})
        
        st.balloons()
        placeholder_anim.markdown(f"""
            <div style="background: linear-gradient(45deg, #f1c40f, #f39c12); 
                        padding: 40px; border-radius: 25px; text-align: center; color: #000;
                        box-shadow: 0 10px 40px rgba(241, 196, 15, 0.6); border: 4px solid white;">
                <h1 style='margin:0; font-size: 50px;'>🎉 ¡GANADOR: NÚMERO {ganador_n}! 🎉</h1>
                <hr style='border-color: black;'>
                <h2 style='margin:10px 0;'>Felicidades, <b>{ganador_nom}</b></h2>
            </div>
        """, unsafe_allow_html=True)
else:
    st.info("💡 Registra al menos a un amigo para habilitar el sorteo.")

st.caption("Neo Sorteo v3.0 | Callao 2026 | Desarrollado por Gerson")
