import random
from datetime import datetime
from config.db_config import get_connection
import threading

# Límites eléctricos
LIMITE_VOLT = 230
LIMITE_POTENCIA = 1800
LIMITE_CORRIENTE = 10.0
MAX_LECTURAS = 200  # máximo de lecturas por dispositivo

# Lock para evitar conflictos en el hilo
lock = threading.Lock()

# 🔹 Genera lecturas simuladas y guarda en BD
def generar_datos_simulados(dispositivos):
    lecturas = []
    with lock:
        conn = get_connection()
        cursor = conn.cursor()

        for disp in dispositivos:
            nombre = disp.get('nombre') or f"Dispositivo {disp['id']}"
            tipo = disp.get('tipo') or "Desconocido"

            voltaje = round(random.uniform(210, 240), 2)
            corriente = round(random.uniform(0.1, 10.0), 2)
            potencia = round(voltaje * corriente, 2)
            frecuencia = 60
            estado = random.choice(['ON', 'OFF'])
            fecha = datetime.now().strftime('%Y-%m-%d')
            hora = datetime.now().strftime('%H:%M:%S')

            # Detectar alertas
            alertas = []
            sugerencia = None
            if voltaje > LIMITE_VOLT:
                alertas.append(f"⚠️ Voltaje alto ({voltaje}V)")
            if corriente > LIMITE_CORRIENTE:
                alertas.append(f"⚠️ Corriente alta ({corriente}A)")
            if potencia > LIMITE_POTENCIA:
                alertas.append(f"⚠️ Potencia excesiva ({potencia}W)")

            if alertas:
                sugerencia = f"Recomendación: apaga {nombre} para evitar sobreconsumo."

            # Inserta en BD
            cursor.execute("""
                INSERT INTO lecturas (dispositivo_id, voltaje, corriente, potencia, estado, frecuencia, fecha, hora)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (disp['id'], voltaje, corriente, potencia, estado, frecuencia, fecha, hora))

            # Limitar lecturas a MAX_LECTURAS por dispositivo
            cursor.execute("""
                DELETE FROM lecturas 
                WHERE id NOT IN (
                    SELECT id FROM lecturas
                    WHERE dispositivo_id = ?
                    ORDER BY id DESC
                    LIMIT ?
                ) AND dispositivo_id = ?
            """, (disp['id'], MAX_LECTURAS, disp['id']))

            # Guardar lectura en lista
            lecturas.append({
                'id': disp['id'],
                'nombre': nombre,
                'tipo': tipo,
                'voltaje': voltaje,
                'corriente': corriente,
                'potencia': potencia,
                'frecuencia': frecuencia,
                'estado': estado,
                'alertas': alertas,
                'sugerencia': sugerencia,
                'fecha': fecha,
                'hora': hora
            })

        conn.commit()
        conn.close()
    return lecturas

# 🔹 Recupera últimas lecturas por dispositivo
def obtener_lecturas(limit_per_device=1):
    lecturas = []
    conn = get_connection()
    cursor = conn.cursor()

    if limit_per_device is None:
        cursor.execute("""
            SELECT d.id, d.nombre, d.tipo, l.voltaje, l.corriente, l.potencia,
                   l.frecuencia, l.estado, l.fecha, l.hora
            FROM dispositivos d
            LEFT JOIN (
                SELECT * FROM lecturas
                WHERE id IN (
                    SELECT MAX(id) FROM lecturas GROUP BY dispositivo_id
                )
            ) l ON l.dispositivo_id = d.id
            ORDER BY d.id
        """)
        filas = cursor.fetchall()
    else:
        dispositivos = cursor.execute("SELECT id, nombre, tipo FROM dispositivos").fetchall()
        filas = []
        for disp in dispositivos:
            cursor.execute("""
                SELECT id, voltaje, corriente, potencia, frecuencia, estado, fecha, hora
                FROM lecturas
                WHERE dispositivo_id = ?
                ORDER BY id DESC
                LIMIT ?
            """, (disp[0], limit_per_device))
            rows = cursor.fetchall()
            for row in rows:
                filas.append((
                    disp[0],  # id dispositivo
                    disp[1],  # nombre
                    disp[2],  # tipo
                    row[1],   # voltaje
                    row[2],   # corriente
                    row[3],   # potencia
                    row[4],   # frecuencia
                    row[5],   # estado
                    row[6],   # fecha
                    row[7]    # hora
                ))

    conn.close()

    for fila in filas:
        voltaje = fila[3] or 0
        corriente = fila[4] or 0
        potencia = fila[5] or 0

        alertas = []
        sugerencia = None
        if voltaje > LIMITE_VOLT:
            alertas.append(f"⚠️ Voltaje alto ({voltaje}V)")
        if corriente > LIMITE_CORRIENTE:
            alertas.append(f"⚠️ Corriente alta ({corriente}A)")
        if potencia > LIMITE_POTENCIA:
            alertas.append(f"⚠️ Potencia excesiva ({potencia}W)")

        if alertas:
            sugerencia = f"Recomendación: apaga {fila[1]} para evitar sobreconsumo."

        lecturas.append({
            'id': fila[0],
            'nombre': fila[1] or f"Dispositivo {fila[0]}",
            'tipo': fila[2] or "Desconocido",
            'voltaje': voltaje,
            'corriente': corriente,
            'potencia': potencia,
            'frecuencia': fila[6] or 0,
            'estado': fila[7] or "OFF",
            'fecha': fila[8] or "",
            'hora': fila[9] or "",
            'alertas': alertas,
            'sugerencia': sugerencia
        })

    return lecturas
