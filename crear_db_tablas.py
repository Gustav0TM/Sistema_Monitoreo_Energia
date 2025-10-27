import sqlite3
from datetime import datetime
import os

DB_PATH = os.path.join(os.getcwd(), 'energia.db')

def inicializar_bd():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Tabla usuarios
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    # Tabla dispositivos
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS dispositivos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            tipo TEXT,
            ubicacion TEXT,
            estado TEXT
        )
    """)

    # Tabla lecturas
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS lecturas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        dispositivo_id INTEGER,
        voltaje REAL,
        corriente REAL,
        potencia REAL,
        estado TEXT,
        frecuencia REAL,
        fecha TEXT,
        hora TEXT,
        FOREIGN KEY(dispositivo_id) REFERENCES dispositivos(id)
        )
    """)

    # Insertar usuario admin por defecto
    cursor.execute("SELECT * FROM usuarios WHERE usuario = 'admin'")
    if not cursor.fetchone():
        cursor.execute("INSERT INTO usuarios (usuario, password) VALUES (?, ?)", ('admin', 'admin123'))
        print("👤 Usuario administrador creado: admin / admin123")

    conn.commit()
    conn.close()
    print("✅ Base de datos 'energia.db' inicializada correctamente.")

if __name__ == "__main__":
    inicializar_bd()
