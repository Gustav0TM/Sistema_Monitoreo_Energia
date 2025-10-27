from flask import Blueprint, render_template, request, redirect, url_for, session
from models.usuario_model import validar_usuario

login_bp = Blueprint('login', __name__)

@login_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        password = request.form['password']
        if validar_usuario(usuario, password):
            session['usuario'] = usuario
            return redirect(url_for('monitor.principal'))
        else:
            return render_template('login.html', error='Usuario o contraseña incorrectos')
    return render_template('login.html')

@login_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login.login'))
