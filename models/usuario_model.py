import sqlite3
import os

# Ruta base del proyecto (sube un nivel para llegar a /config)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, 'energia.db')

def validar_usuario(usuario, password):
    """Valida usuario y contraseña directamente desde la base de datos."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM usuarios WHERE usuario = ? AND password = ?", (usuario, password))
        resultado = cursor.fetchone()

        conn.close()
        return resultado is not None
    except Exception as e:
        print("Error al validar usuario:", e)
        return False

def insertar_usuario(usuario, password):
    """Permite agregar nuevos usuarios a la tabla usuarios."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute("INSERT INTO usuarios (usuario, password) VALUES (?, ?)", (usuario, password))
        conn.commit()
        conn.close()
        print(f"Usuario '{usuario}' agregado correctamente.")
    except sqlite3.IntegrityError:
        print(f"⚠️ El usuario '{usuario}' ya existe.")
    except Exception as e:
        print("Error al insertar usuario:", e)
