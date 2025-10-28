import sqlite3
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

    # Insertar dispositivos actuales
    dispositivos_actuales = [
        ("Tuya1", "Enchufe 1"),
        ("Tuya2", "Enchufe 2"),
        ("Tuya3", "Enchufe 3"),
        ("Tuya4", "Enchufe 4"),
        ("Tuya5", "Interruptor 1")
    ]

    for nombre, tipo in dispositivos_actuales:
        cursor.execute("SELECT * FROM dispositivos WHERE nombre = ?", (nombre,))
        if not cursor.fetchone():
            cursor.execute(
                "INSERT INTO dispositivos (nombre, tipo) VALUES (?, ?)",
                (nombre, tipo)
            )
            print(f"💡 Dispositivo creado: {nombre} / {tipo}")

    conn.commit()
    conn.close()
    print("✅ Base de datos 'energia.db' inicializada correctamente.")

if __name__ == "__main__":
    inicializar_bd()
