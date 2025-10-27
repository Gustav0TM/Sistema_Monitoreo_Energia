from flask import Blueprint, jsonify
from models.monitor_model import obtener_lecturas, generar_datos_simulados
from models.dispositivo_model import obtener_dispositivos

api_bp = Blueprint('api', __name__)

@api_bp.route('/api/lecturas')
def api_lecturas():
    # Solo las últimas 10 lecturas para el gráfico histórico
    lecturas = obtener_lecturas(limit_per_device=10)
    return jsonify(lecturas)

@api_bp.route('/api/simular')
def api_simular():
    dispositivos = obtener_dispositivos()
    lecturas = generar_datos_simulados(dispositivos)
    return jsonify(lecturas)
