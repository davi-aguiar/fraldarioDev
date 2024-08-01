#importações
from datetime import datetime
from flask import Blueprint, Flask, redirect, url_for, flash, request, render_template, session,jsonify, send_file, abort
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from jinja2 import TemplateNotFound

# from teste import Farmacia

#instanciando a blueprint
prefeitura_route = Blueprint('prefeitura', __name__,
                        template_folder='templates')

#rota de inicio quando loga na prefeitura
@prefeitura_route.route('/prefeitura')
@login_required
def prefeitura():
    tipo_usuario = session.get('tipo_usuario')
    if 'nomePrefeitura' in session:
        nomePrefeitura = session['nomePrefeitura']
    else:
        nomePrefeitura = 'Prefeitura'
    return render_template("prefeitura.html", tipo_usuario=tipo_usuario, nomePrefeitura=nomePrefeitura)
@prefeitura_route.route('/pagina_prefeitura')
@login_required
def pagina_prefeitura():
    tipo_usuario = session.get('tipo_usuario','3')
    if tipo_usuario=='3':
        if 'nomePrefeitura' in session:
            nomePrefeitura = session['nomePrefeitura']
        else:
            nomePrefeitura = 'Prefeitura'

        return render_template('prefeitura.html', nomePrefeitura=nomePrefeitura,  tipo_usuario=tipo_usuario, title="Prefeitura")
    else:
        print("entrou no else")
        return redirect(url_for('rota_protegida'))
    

# @prefeitura_route.route('/list-files-farmacia/<int:farmacia_id>', methods=['GET'])
# def list_files_farmacia(farmacia_id):
    
#     farmacia = Farmacia.query.filter_by(id=farmacia_id).first()
#     if farmacia:
#         documentos = []
        
#         if farmacia.documento_liberacao:
            
#             documentos.append({
#                 'filename': f"{farmacia.id}_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf",
#                 'url': url_for('get_documents_farmacia', farmacia_id=farmacia_id)
#             })
#         else:
           
#             return jsonify(documentos)
    
#     return jsonify([])

# @prefeitura_route.route('/get-documento-farmacia/<int:farmacia_id>', methods=['GET'])
# @login_required
# def get_documents_farmacia(farmacia_id):
    
#     farmacia = Farmacia.query.filter_by(id=farmacia_id).first()
#     if farmacia and farmacia.documento_liberacao:
#         documento_blob = farmacia.documento_liberacao
#         file_name = f"{farmacia_id}_documento_{datetime.now().strftime('%Y-%m-%d')}.pdf"
#         return send_file(io.BytesIO(documento_blob), mimetype='application/pdf', as_attachment=True, download_name=file_name)
#     else:
        
#         return "Documento não encontrado!", 404