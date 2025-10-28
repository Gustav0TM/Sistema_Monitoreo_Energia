import sqlite3
import os

DB_PATH = os.path.join(os.getcwd(), 'energia.db')

def limpiar_lecturas():
    if not os.path.exists(DB_PATH):
        print("❌ No se encontró la base de datos 'energia.db'.")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Borrar todas las lecturas
    cursor.execute("DELETE FROM lecturas")
    print("🗑️ Todas las lecturas han sido eliminadas.")

    # Reiniciar contador AUTOINCREMENT
    cursor.execute("DELETE FROM sqlite_sequence WHERE name='lecturas'")
    print("🔄 Contador de ID de lecturas reiniciado.")

    conn.commit()
    conn.close()
    print("✅ Base de datos lista para nuevas lecturas.")

if __name__ == "__main__":
    limpiar_lecturas()
