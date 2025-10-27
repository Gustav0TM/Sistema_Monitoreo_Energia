import sqlite3
import os

# Ruta a tu base de datos
DB_PATH = os.path.join(os.getcwd(), 'energia.db')

# Conectar a la base de datos
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Ejecutar consulta para ver todos los dispositivos
cursor.execute("SELECT * FROM dispositivos")
dispositivos = cursor.fetchall()

# Mostrar resultados
for d in dispositivos:
    print(d)

# Cerrar conexión
conn.close()
