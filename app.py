import streamlit as st
import random
import time
import pandas as pd

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Neo Sorteo - Edición Gala", layout="wide")

# --- ESTILOS CSS (EL ALMA VISUAL) ---
st.markdown("""
    <style>
    /* Fondo con Gradiente y Animación de Bolillas Flotantes */
    .stApp {
        background: radial-gradient(circle at center, #1a1f26 0%, #0a0e14 100%);
    }

    .fondo-bolilla {
        position: fixed; width: 30px; height: 30px;
        background: rgba(0, 212, 255, 0.15);
        border-radius: 50%; border: 1px solid rgba(255,255,255,0.1);
        z-index: -1; animation: flotar 12s infinite linear;
    }
    @keyframes flotar {
        0% { transform: translateY(110vh) scale(0.5); opacity: 0; }
        50% { opacity: 0.6; }
        100% { transform: translateY(-10vh) scale(1.2); opacity: 0; }
    }

    /* Tablero de Números Estilo Tómbola */
    .numero-box {
        padding: 10px; border-radius: 50%; text-align: center;
        margin: 5px; font-weight: bold; width: 50px; height: 50px;
        line-height: 30px; font-size: 18px; transition: all 0.3s;
    }
    .vendido { 
        background: linear-gradient(135deg, #ff3131, #8b0000); 
        color: white; border: 2px solid #ffd700; box-shadow: 0px 0px 15px #ff3131;
    }
    .libre { 
        background: rgba(255,255,255,0.05); color: #00d4ff; 
        border: 1px solid #1a1f26; 
    }

    /* Efectos de Texto y Bolilla Gigante */
    .bolilla-show {
        background: radial-gradient(circle at 30% 30%, #ffd700, #b8860b);
        color: black; border-radius: 50%; width: 220px; height: 220px;
        display: flex; align-items: center; justify-content: center;
        font-size: 110px; font-weight: bold; margin: auto;
        border: 10px solid white; box-shadow: 0px 0px 60px rgba(255, 215, 0, 0.7);
    }
    
    .msg-animado {
        font-size: 45px; color: #00ffcc; text-align: center;
        font-weight: bold; text-shadow: 2px 2px 15px black;
        margin-top: 30px;
    }

    .conteo-regresivo {
        font-size: 180px; color: #ffffff; text-align: center;
        font-weight: bold; text-shadow: 0px 0px 30px #ffd700;
    }
    </style>
    """, unsafe_allow_html=True)

# Generar bolillas animadas de fondo
for i in range(12):
    st.markdown(f'<div class="fondo-bolilla" style="left:{random.randint(0,95)}vw; animation-delay:{random.randint(0,10)}s;"></div>', unsafe_allow_html=True)

# --- LÓGICA DE DATOS ---
if 'db_sorteo' not in st.session_state:
    st.session_state.db_sorteo = {}

# --- SIDEBAR: GESTIÓN DE PARTICIPANTES ---
with st.sidebar:
    st.title("⚓ Panel de Control")
    st.subheader("📝 Registrar Vecino")
    
    with st.form("registro_form", clear_on_submit=True):
        nombre = st.text_input("Nombre Completo")
        numero = st.number_input("Número Elegido (1-50)", 1, 50, step=1)
        if st.form_submit_button("Registrar Número"):
            if nombre:
                st.session_state.db_sorteo[numero] = nombre
                st.success(f"¡Número {numero} asignado!")
                st.rerun()
            else:
                st.warning("Por favor, pon un nombre.")

    st.write("---")
    st.subheader("📋 Lista de Participantes")
    if st.session_state.db_sorteo:
        # Mostrar tabla para control
        data = [{"#": k, "Nombre": v} for k, v in st.session_state.db_sorteo.items()]
        df = pd.DataFrame(data).sort_values("#")
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        # Opción para borrar
        num_a_borrar = st.selectbox("Seleccionar # para borrar:", df["#"])
        if st.button("❌ Eliminar Registro"):
            del st.session_state.db_sorteo[num_a_borrar]
            st.rerun()
    
    if st.button("🚨 Reiniciar Todo"):
        st.session_state.db_sorteo = {}
        st.rerun()

# --- CUERPO PRINCIPAL ---
st.title("🎰 Neo Sorteo: ¡La Suerte del Callao!")
st.write("Visualización en tiempo real de los números ocupados.")

# Dibujar Tablero
cols = st.columns(10)
for n in range(1, 51):
    with cols[(n-1)%10]:
        clase = "vendido" if n in st.session_state.db_sorteo else "libre"
        st.markdown(f'<div class="numero-box {clase}">{n}</div>', unsafe_allow_html=True)

st.write("---")

# --- PROCESO DE SORTEO ---
if len(st.session_state.db_sorteo) > 0:
    if st.button("🔥 ¡INICIAR EL GRAN CHOCOLATEO! 🔥", type="primary", use_container_width=True):
        area_accion = st.empty()
        
        # 1. Mensajes de Aliento
        frases = ["¡VAMOS CALLAO! ⚓", "¡LA SUERTE ESTÁ ECHADA! ✨", "¡CHOCOLATEANDO LAS BOLILLAS! 🍫"]
        for f in frases:
            area_accion.markdown(f'<div class="msg-animado">{f}</div>', unsafe_allow_html=True)
            time.sleep(1.5)

        # 2. Chocolateo Visual (Efecto Tómbola)
        for _ in range(25):
            n_fake = random.randint(1, 50)
            area_accion.markdown(f"""
                <div style="text-align:center;">
                    <div class="bolilla-show" style="background: radial-gradient(circle, #00d4ff, #0072ff);">{n_fake}</div>
                    <h2 style="color:white; margin-top:15px;">¡Buscando al afortunado...!</h2>
                </div>
            """, unsafe_allow_html=True)
            time.sleep(0.1)

        # 3. Cuenta Regresiva
        for i in ["3", "2", "1"]:
            area_accion.markdown(f'<div class="conteo-regresivo">{i}</div>', unsafe_allow_html=True)
            time.sleep(1)

        # 4. Revelación del Ganador Real
        ganador_num = random.choice(list(st.session_state.db_sorteo.keys()))
        ganador_nom = st.session_state.db_sorteo[ganador_num]
        
        area_accion.empty()
        with area_accion.container():
            st.markdown(f'<div class="bolilla-show">{ganador_num}</div>', unsafe_allow_html=True)
            time.sleep(0.8)
            st.markdown(f"""
                <div style="background:white; color:black; padding:30px; border-radius:25px; 
                font-size:65px; font-weight:bold; text-align:center; border:8px solid #ffd700; margin-top:25px;">
                🏆 {ganador_nom} 🏆
                </div>
            """, unsafe_allow_html=True)
            st.balloons()
            st.snow()
            
            # Formato WhatsApp
            st.write("---")
            st.info("Copia este mensaje para el grupo:")
            st.code(f"⚓ *RESULTADO NEO SORTEO* ⚓\n\n🎉 ¡Felicidades {ganador_nom}!\n🔢 Ganaste con el número: {ganador_num}\n\n¡Gracias a todos por participar! 🔥", language="text")