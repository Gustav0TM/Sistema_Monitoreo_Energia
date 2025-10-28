from flask import Flask 
from controllers.monitor_controller import monitor_bp
from controllers.login_controller import login_bp
from controllers.api_controller import api_bp
from controllers.reporte_controller import reporte_bp
from models.monitor_model import generar_datos_simulados, obtener_lecturas
import os
import threading
import time

# -------------------------------------------------------------------
# 🌎 CONFIGURACIÓN DE ZONA HORARIA LOCAL (PERÚ)
# -------------------------------------------------------------------
os.environ['TZ'] = 'America/Lima'
time.tzset()

# -------------------------------------------------------------------
# CONFIGURACIÓN GENERAL DE LA APLICACIÓN FLASK
# -------------------------------------------------------------------
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, 'Layout', 'templates'),
    static_folder=os.path.join(BASE_DIR, 'Layout', 'static')
)

# Clave secreta para las sesiones
app.secret_key = 'clave_secreta_segura'

# -------------------------------------------------------------------
# REGISTRO DE BLUEPRINTS (controladores)
# -------------------------------------------------------------------
app.register_blueprint(monitor_bp)
app.register_blueprint(login_bp)
app.register_blueprint(api_bp)
app.register_blueprint(reporte_bp)

# -------------------------------------------------------------------
# RUTA PRINCIPAL (REDIRECCIÓN AL LOGIN)
# -------------------------------------------------------------------
@app.route('/')
def home():
    return "<script>window.location.href='/login';</script>"

# -------------------------------------------------------------------
# HILO DE SEGUNDO PLANO: GENERACIÓN PERIÓDICA DE DATOS SIMULADOS
# -------------------------------------------------------------------
db_lock = threading.Lock()

def hilo_generar_datos():
    while True:
        try:
            with db_lock:
                dispositivos = obtener_lecturas(limit_per_device=None)
                generar_datos_simulados(dispositivos)
        except Exception as e:
            print(f"❌ Error en hilo_generar_datos: {e}")
        time.sleep(2)  # espera 2 segundos antes de la siguiente generación

# -------------------------------------------------------------------
# EJECUCIÓN PRINCIPAL
# -------------------------------------------------------------------
if __name__ == '__main__':
    print("🚀 Sistema de Monitoreo Inteligente ejecutándose...")
    threading.Thread(target=hilo_generar_datos, daemon=True).start()

    port = int(os.environ.get("PORT", 5000))  # Render asigna este puerto automáticamente
    app.run(host='0.0.0.0', port=port, debug=False)