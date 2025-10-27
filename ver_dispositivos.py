import sqlite3
import os

# Ruta de la base de datos
BASE_DIR = os.getcwd()  # carpeta raíz de tu proyecto
DB_PATH = os.path.join(BASE_DIR, "energia.db")

# Conexión a la base de datos
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

try:
    # Mostrar todos los dispositivos
    cursor.execute("SELECT * FROM dispositivos")
    dispositivos = cursor.fetchall()

    if dispositivos:
        print("Tabla dispositivos:")
        for d in dispositivos:
            print(d)
    else:
        print("La tabla dispositivos está vacía.")
except sqlite3.OperationalError as e:
    print("Error:", e)

conn.close()
