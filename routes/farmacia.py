from flask import Blueprint, redirect, url_for, flash, request, render_template, session, jsonify, send_file, abort
from datetime import datetime, timedelta
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from jinja2 import TemplateNotFound
from models import db,Farmacia
from io import BytesIO, StringIO

# instanciando a blueprint
farmacia_route = Blueprint('farmacia', __name__, template_folder='templates',url_prefix='/farmacia')


        

# rota de início quando loga na prefeitura
@farmacia_route.route('/pagina_farmacia')
@login_required
def pagina_farmacia():
    tipo_usuario = session.get('tipo_usuario', '1')
    if tipo_usuario == '1':
        nomeFantasia = session.get('nomeFantasia', 'Farmácia')

        # Verifique se o ID da farmácia está na sessão
        farmacia_id = session.get('farmacia_id')
        if farmacia_id is None:
            flash('ID da farmácia não encontrado na sessão.', 'error')
            return redirect(url_for('rota_protegida'))

        # Verifique se o ID da farmácia é válido
        farmacia = Farmacia.query.get(farmacia_id)
        if farmacia is None:
            flash('Farmácia não encontrada.', 'error')
            return redirect(url_for('rota_protegida'))

        # Obtenha os dados para os dashboards
        total_fraldas_entregues = sum(transacao.quantidade for transacao in farmacia.transacoes)
        marca_mais_vendida = obter_marca_mais_vendida(farmacia.transacoes)
        media_fraldas_semana = calcular_media_fraldas_semana(farmacia.transacoes)

        return render_template(
            'farmacia.html', 
            nomeFantasia=nomeFantasia, 
            tipo_usuario=tipo_usuario, 
            title="Farmácia",
            total_fraldas_entregues=total_fraldas_entregues,
            marca_mais_vendida=marca_mais_vendida if marca_mais_vendida else 'Nenhuma transação encontrada',
            media_fraldas_semana=media_fraldas_semana,
            farmacia_id=farmacia_id
        )
    else:
        return redirect(url_for('rota_protegida'))    


def obter_marca_mais_vendida(transacoes):
    if not transacoes:
        return None  # ou algum valor padrão que faça sentido

    marca_contagem = {}
    for transacao in transacoes:
        marca = transacao.marca_fralda_entregue  # Certifique-se de que o nome do atributo está correto
        if marca in marca_contagem:
            marca_contagem[marca] += transacao.quantidade
        else:
            marca_contagem[marca] = transacao.quantidade
    
    return max(marca_contagem, key=marca_contagem.get)

def calcular_media_fraldas_semana(transacoes):
    from collections import defaultdict
    from datetime import timedelta
    
    if not transacoes:
        return 0  # ou algum valor padrão que faça sentido

    semanas = defaultdict(int)
    for transacao in transacoes:
        semana = transacao.data_retirada - timedelta(days=transacao.data_retirada.weekday())
        semanas[semana] += transacao.quantidade

    if semanas:
        return sum(semanas.values()) / len(semanas)
    return 0
@farmacia_route.route("/visualizarDocumentos")
def visualizarDocumentos():
    farmacia_id = session.get('farmacia_id')
    if farmacia_id is None:
        flash('ID da farmácia não encontrado na sessão.', 'error')
        return redirect(url_for('rota_protegida'))
    
    # Simulação de um objeto Farmacia
    farmacia = Farmacia()

    documentos = []
    if farmacia.documento_liberacao:
        documentos.append({
            'filename': f"{farmacia.cnpj}_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf",
            'url': url_for('farmacia_route.get_documentos_farmacia')
        })

    return jsonify(documentos)

@farmacia_route.route('/get-documento-farmacia')
def get_documentos_farmacia():
    farmacia_id = session.get('farmacia_id')
    if farmacia_id is None:
        flash('ID da farmácia não encontrado na sessão.', 'error')
        return redirect(url_for('rota_protegida'))
    
    # Simulação de um objeto Farmacia
    farmacia = Farmacia()

    if farmacia and farmacia.documento_liberacao:
        documento_blob = farmacia.documento_liberacao
        file_name = f"{farmacia.cnpj}_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
        return send_file(
            io.BytesIO(documento_blob),
            mimetype="application/pdf",
            as_attachment=True,
            download_name=file_name
        )
    else:
        return "Arquivo não encontrado", 404
        
