import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

# 🔗 Conectar a Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("❌ Faltan las variables SUPABASE_URL o SUPABASE_KEY en el archivo .env")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


def save_message(user_id, role, message):
    try:
        if role not in ["user", "assistant"]:
            print(f"⚠️ Rol inválido '{role}', no se guardará el mensaje.")
            return
        supabase.table("chat_history").insert({
            "user_id": user_id,
            "sender_role": role,  # ✅ Cambiado aquí
            "message": message
        }).execute()
    except Exception as e:
        print(f"❌ Error al guardar mensaje: {e}")



# 📜 Obtener historial de conversación desde Supabase
def get_conversation_history(user_id):
    try:
        response = supabase.table("chat_history").select("*").eq("user_id", user_id).order("timestamp").execute()
        data = response.data

        valid_roles = {"user", "assistant", "system"}
        messages = []
        for row in data:
            role = row.get("sender_role")  # ✅ Cambiado aquí
            message = row.get("message")
            if role in valid_roles and messages:
                messages.append({"role": role, "message": message})

        return messages

    except Exception as e:
        print(f"❌ Error al obtener historial: {e}")
        return []