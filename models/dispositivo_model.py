from config.db_config import get_connection

def obtener_dispositivos():
    """
    Devuelve todos los dispositivos registrados en la BD como lista de diccionarios.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id, nombre, tipo, ubicacion, estado FROM dispositivos")
    filas = cursor.fetchall()
    conn.close()

    dispositivos = []
    for fila in filas:
        dispositivos.append({
            'id': fila[0],
            'nombre': fila[1],
            'tipo': fila[2],
            'ubicacion': fila[3],
            'estado': fila[4]
        })
    return dispositivos
