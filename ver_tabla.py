import sqlite3

# Conexión a la base de datos
conexion = sqlite3.connect("energia.db")
cursor = conexion.cursor()

# Mostrar la estructura de la tabla 'lecturas'
cursor.execute("PRAGMA table_info(lecturas)")
columnas = cursor.fetchall()

print("\n📋 Estructura de la tabla 'lecturas':\n")
for col in columnas:
    print(f"ID: {col[0]}, Nombre: {col[1]}, Tipo: {col[2]}")

conexion.close()