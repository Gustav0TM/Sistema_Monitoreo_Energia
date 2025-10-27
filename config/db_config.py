import sqlite3
import os

# -------------------------------------------------------------------
# RUTA CORRECTA: la BD estará en la raíz del proyecto
# -------------------------------------------------------------------
BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))  # sube un nivel
DB_PATH = os.path.join(BASE_DIR, 'energia.db')

def get_connection():
    """Devuelve la conexión a la base de datos SQLite existente."""
    if not os.path.exists(DB_PATH):
        print(f"❌ La base de datos no existe en: {DB_PATH}")
        return None

    try:
        conn = sqlite3.connect(DB_PATH)
        return conn
    except Exception as e:
        print("❌ Error al conectar con la base de datos:", e)
        return None
