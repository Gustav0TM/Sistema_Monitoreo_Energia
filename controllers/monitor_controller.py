from flask import Blueprint, render_template, redirect, url_for, session, jsonify
from models.monitor_model import obtener_lecturas
from models.dispositivo_model import obtener_dispositivos

monitor_bp = Blueprint('monitor', __name__)

# Middleware: verificación de sesión
@monitor_bp.before_request
def verificar_sesion():
    if 'usuario' not in session and not session.get('ruta_publica'):
        return redirect(url_for('login.login'))

# Rutas principales
@monitor_bp.route('/')
def inicio():
    return redirect(url_for('monitor.principal'))

@monitor_bp.route('/principal')
def principal():
    dispositivos = obtener_dispositivos()
    lecturas = obtener_lecturas()
    return render_template('principal.html', dispositivos=dispositivos, lecturas=lecturas)

@monitor_bp.route('/grafico')
def grafico():
    dispositivos = obtener_dispositivos()
    return render_template('grafico.html', dispositivos=dispositivos)

