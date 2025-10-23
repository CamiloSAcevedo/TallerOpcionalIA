import streamlit as st
import pandas as pd
from supabase import create_client

st.set_page_config(page_title="Dashboard de Agente IA", layout="wide")
st.title("Monitoring Dashboard del Agente IA")

# --- Ingreso de credenciales Supabase ---
st.sidebar.header("Configuración de Supabase")
url = st.sidebar.text_input("SUPABASE_URL", type="default")
key = st.sidebar.text_input("SUPABASE_KEY", type="password")

# Solo crear el cliente si ambas claves fueron ingresadas
if url and key:
    try:
        supabase = create_client(url, key)
    except Exception as e:
        st.error(f"Error al conectar con Supabase: {e}")
        st.stop()
else:
    st.warning("Por favor ingresa tus credenciales de Supabase en el panel lateral.")
    st.stop()

# --- Función para cargar los datos ---
def load_all_data():
    """Carga todos los chats de la base de datos."""
    try:
        response = (
            supabase.table("chat_history")
            .select("*")
            .order("timestamp", desc=True)
            .execute()
        )
        return pd.DataFrame(response.data)
    except Exception as e:
        st.error(f"Error al cargar datos: {e}")
        return pd.DataFrame()

# --- Cuerpo de la App ---
df = load_all_data()

if df.empty:
    st.warning("Aún no hay conversaciones en la base de datos.")
else:
    st.header("Visor de Conversaciones")

    # 1. Filtro por Usuario
    all_users = df["user_id"].unique()
    selected_user = st.selectbox("Selecciona un User ID para ver su chat:", all_users)

    if selected_user:
        st.subheader(f"Historial de Chat para: {selected_user}")

        # Filtrar DF para ese usuario y ordenar por tiempo
        user_chat_df = df[df["user_id"] == selected_user].sort_values(by="timestamp")

        # Mostrar el chat en formato tipo chat
        for _, row in user_chat_df.iterrows():
            with st.chat_message(name=row["sender_role"]):
                st.write(f"**{row['sender_role']}:**")
                st.write(row["message"])
                st.caption(f"_{row['timestamp']}_")

    # 2. Vista de Datos Crudos
    with st.expander("Ver todos los datos crudos (Raw Data)"):
        st.dataframe(df)

# Botón para refrescar
if st.button("Refrescar Datos"):
    st.rerun()
