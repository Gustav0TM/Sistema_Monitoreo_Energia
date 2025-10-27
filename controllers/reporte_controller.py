# -------------------------------------------------------------------
# CONTROLADOR DE REPORTES Y REGISTROS
# -------------------------------------------------------------------
# Este controlador unifica:
#  - Generación automática de reportes PDF (gráfico, tabla, análisis)
#  - Historial de reportes PDF generados en /Layout/static/reports/
#  - Registro de mayor consumo en ultimo_reporte.json
# -------------------------------------------------------------------

from flask import Blueprint, render_template, send_file, current_app
from models.monitor_model import generar_datos_simulados
from models.dispositivo_model import obtener_dispositivos
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime
import io
import matplotlib
matplotlib.use('Agg')  # Evita advertencia GUI en Flask
import matplotlib.pyplot as plt
import os
import json

# -------------------------------------------------------------------
# CONFIGURACIÓN DEL BLUEPRINT
# -------------------------------------------------------------------
reporte_bp = Blueprint('reporte', __name__)

# -------------------------------------------------------------------
# RUTA: /registros
# -------------------------------------------------------------------
@reporte_bp.route('/registros')
def registros():
    try:
        # 🔹 Carpeta absoluta de reportes
        reports_dir = os.path.join(current_app.root_path, 'Layout', 'static', 'reports')
        os.makedirs(reports_dir, exist_ok=True)

        # Listado de PDFs
        reportes = [f for f in os.listdir(reports_dir) if f.endswith('.pdf')]
        reportes.sort(reverse=True)

        # Leer JSON del último reporte
        mayor_consumo_total = None
        ruta_json = os.path.join(reports_dir, 'ultimo_reporte.json')
        if os.path.exists(ruta_json):
            with open(ruta_json, 'r', encoding='utf-8') as f:
                mayor_consumo_total = json.load(f)

        # Para mostrar gráfico rápido del mayor consumo (inline)
        grafico_path = None
        if mayor_consumo_total:
            fig, ax = plt.subplots(figsize=(4,2))
            ax.bar([mayor_consumo_total['nombre']], [mayor_consumo_total['potencia']],
                   color='#ff4c4c' if mayor_consumo_total['potencia']>1800 else '#28a745')
            ax.set_ylabel("Potencia (W)")
            ax.set_title("Mayor consumo")
            plt.tight_layout()
            grafico_path = os.path.join(reports_dir, 'grafico_consumo.png')
            fig.savefig(grafico_path)
            plt.close(fig)

        return render_template('registros.html',
                               reportes=reportes,
                               mayor_consumo_total=mayor_consumo_total,
                               grafico_path=grafico_path)
    except Exception as e:
        return f"❌ Error al cargar registros: {e}"

# -------------------------------------------------------------------
# RUTA: /reporte/pdf
# -------------------------------------------------------------------
@reporte_bp.route('/reporte/pdf')
def generar_reporte_pdf():
    try:
        dispositivos = obtener_dispositivos()
        lecturas = generar_datos_simulados(dispositivos)

        ahora = datetime.now()
        for l in lecturas:
            l["fecha"] = ahora.strftime("%d/%m/%Y")
            l["hora"] = ahora.strftime("%H:%M:%S")

        nombres = [d['nombre'] for d in lecturas]
        potencias = [d['potencia'] for d in lecturas]
        colores = ['#ff4c4c' if p>1800 else '#28a745' for p in potencias]

        plt.figure(figsize=(6,3))
        plt.bar(nombres, potencias, color=colores)
        plt.xlabel('Dispositivos')
        plt.ylabel('Potencia (W)')
        plt.title('Consumo Instantáneo de Energía')
        plt.tight_layout()

        reports_dir = os.path.join(current_app.root_path, 'Layout', 'static', 'reports')
        os.makedirs(reports_dir, exist_ok=True)
        grafico_path = os.path.join(reports_dir, 'grafico_temp.png')
        plt.savefig(grafico_path)
        plt.close()

        buffer = io.BytesIO()
        estilos = getSampleStyleSheet()
        estilo_titulo = estilos['Heading1']
        estilo_normal = estilos['BodyText']

        fecha_nombre = ahora.strftime("%Y-%m-%d_%H-%M-%S")
        nombre_pdf = f"reporte_{fecha_nombre}.pdf"
        pdf_path = os.path.join(reports_dir, nombre_pdf)

        doc = SimpleDocTemplate(buffer, pagesize=A4)
        elementos = []

        # Encabezado
        logo_path = os.path.join(current_app.root_path, 'Layout', 'static', 'img', 'logo.png')
        if os.path.exists(logo_path):
            elementos.append(Image(logo_path, width=80, height=60))
        elementos.append(Paragraph("<b>SISTEMA DE MONITOREO INTELIGENTE</b>", estilo_titulo))
        elementos.append(Paragraph("Gestión y Optimización del Consumo de Energía en Hogares", estilo_normal))
        elementos.append(Spacer(1,12))
        elementos.append(Paragraph(f"🕒 Reporte generado el: {ahora.strftime('%d/%m/%Y %H:%M:%S')}", estilo_normal))
        elementos.append(Spacer(1,10))

        # Gráfico
        elementos.append(Image(grafico_path, width=400, height=200))
        elementos.append(Spacer(1,10))

        # Tabla de lecturas
        tabla_datos = [["Fecha","Hora","Dispositivo","Voltaje (V)","Corriente (A)","Potencia (W)","Estado"]]
        for d in lecturas:
            tabla_datos.append([d["fecha"], d["hora"], d["nombre"], d["voltaje"], d["corriente"], d["potencia"], d["estado"]])

        tabla = Table(tabla_datos, repeatRows=1)
        tabla.setStyle(TableStyle([
            ('BACKGROUND',(0,0),(-1,0), colors.HexColor('#007bff')),
            ('TEXTCOLOR',(0,0),(-1,0), colors.whitesmoke),
            ('ALIGN',(0,0),(-1,-1),'CENTER'),
            ('GRID',(0,0),(-1,-1),0.5,colors.gray),
            ('FONTNAME',(0,0),(-1,0),'Helvetica-Bold')
        ]))
        elementos.append(tabla)
        elementos.append(Spacer(1,12))

        # Análisis
        mayor_consumo = max(lecturas, key=lambda x: x['potencia'])
        analisis = f"💡 <b>Mayor consumo:</b> {mayor_consumo['nombre']} ({mayor_consumo['potencia']} W)"
        if mayor_consumo['potencia']>1800:
            analisis += " ⚠️ Sobreconsumo detectado"
        elementos.append(Paragraph(analisis, estilo_normal))
        elementos.append(Spacer(1,20))

        # Guardar JSON
        ruta_json = os.path.join(reports_dir, 'ultimo_reporte.json')
        with open(ruta_json, 'w', encoding='utf-8') as f:
            json.dump(mayor_consumo, f)

        # Firma
        elementos.append(Paragraph("<b>______________________________</b>", estilo_normal))
        elementos.append(Paragraph("<b>Administrador del Sistema</b>", estilo_normal))
        elementos.append(Paragraph("Universidad César Vallejo - Proyecto Integrador", estilo_normal))

        # Guardar PDF
        doc.build(elementos)
        buffer.seek(0)
        with open(pdf_path, 'wb') as f:
            f.write(buffer.getvalue())

        if os.path.exists(grafico_path):
            os.remove(grafico_path)

        buffer.seek(0)
        return send_file(buffer, as_attachment=True, download_name=nombre_pdf, mimetype='application/pdf')

    except Exception as e:
        return f"❌ Error al generar el reporte: {e}"
