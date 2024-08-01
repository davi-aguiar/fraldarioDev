#importações
from flask import Blueprint, Flask, redirect, url_for, flash, request, render_template, session,jsonify, send_file, abort
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from jinja2 import TemplateNotFound

#instanciando a blueprint
autorizador_route = Blueprint('autorizador', __name__,
                        template_folder='templates')

#rota de inicio quando loga na prefeitura
@autorizador_route.route('/pagina_autorizador')
@login_required
def pagina_autorizador():
    tipo_usuario = session.get('tipo_usuario', '2')
    if tipo_usuario=='2':
       # Lógica para a página do autorizador
        nomeAutorizador = session.get('nomeAutorizador', 'Autorizador')
        return render_template('autorizador.html', nomeAutorizador=nomeAutorizador,  tipo_usuario=tipo_usuario)
    else:
        print("entrou no else")
        return redirect(url_for('rota_protegida'))