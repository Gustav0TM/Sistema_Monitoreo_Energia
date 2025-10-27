# limpiar_lecturas.py
from config.db_config import get_connection

def limpiar_lecturas():
    conn = get_connection()
    cursor = conn.cursor()
    
    # Borrar todas las lecturas
    cursor.execute("DELETE FROM lecturas")
    
    # Reiniciar el autoincrement del id
    cursor.execute("DELETE FROM sqlite_sequence WHERE name='lecturas'")
    
    conn.commit()
    conn.close()
    print("✅ Tabla 'lecturas' reiniciada correctamente. Lista para nuevas simulaciones.")

if __name__ == "__main__":
    limpiar_lecturas()
