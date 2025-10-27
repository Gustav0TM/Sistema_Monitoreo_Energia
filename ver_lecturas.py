import sqlite3

conn = sqlite3.connect('energia.db')
cursor = conn.cursor()

cursor.execute("SELECT * FROM lecturas")
filas = cursor.fetchall()

for fila in filas:
    print(fila)

conn.close()