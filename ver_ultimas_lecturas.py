import sqlite3

# Conexión a la base de datos
conn = sqlite3.connect('energia.db')
cursor = conn.cursor()

# Consulta para obtener las últimas 10 lecturas con el nombre del dispositivo
cursor.execute("""
SELECT l.id, d.nombre, l.voltaje, l.corriente, l.potencia, l.estado, l.fecha, l.hora
FROM lecturas l
JOIN dispositivos d ON l.dispositivo_id = d.id
ORDER BY l.id DESC
LIMIT 10
""")

filas = cursor.fetchall()

print("Últimas 10 lecturas:")
for fila in filas:
    print(fila)

conn.close()
