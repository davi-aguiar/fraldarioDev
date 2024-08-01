from flask import Blueprint, redirect, url_for, flash, request, render_template, session, jsonify, send_file, abort, make_response, current_app
from flask_login import login_required, current_user
from sqlalchemy import extract
from models import db, Farmacia, Transacao
from io import BytesIO
import csv
import pandas as pd
import pytz

# Criação do blueprint
gerarcsv_route = Blueprint('gerarcsv', __name__, template_folder='templates')

@gerarcsv_route.route('/gerar_csv', methods=['POST'])
@login_required
def gerar_csv():
    ano_filter = request.form.get('ano_filter')
    mes_filter = request.form.get('mes_filter')

    current_app.logger.info('Gerando CSV para o mês de %s/%s', mes_filter, ano_filter)

    usuario = current_user
    farmacia = usuario.farmacia

    if not farmacia:
        return "Usuário não associado a uma farmácia", 400

    query = db.session.query(Farmacia, Transacao).join(Transacao, Farmacia.id == Transacao.farmacia_id).filter(Farmacia.id == farmacia.id)

    if ano_filter:
        try:
            ano_filter = int(ano_filter)
            query = query.filter(extract('year', Transacao.data_retirada) == ano_filter)
        except ValueError:
            return "Ano inválido", 400
        
    if mes_filter:
        try:
            mes_filter = int(mes_filter)
            query = query.filter(extract('month', Transacao.data_retirada) == mes_filter)
        except ValueError: 
            return "Mês inválido", 400
    
    dados = query.all()

    if not dados:
        return "Nenhum dado encontrado", 400
    
    data = []

    for farmacia, transacao in dados:
        try:
            data_retirada = transacao.data_retirada.replace(tzinfo=pytz.timezone('UTC')).astimezone(pytz.timezone('America/Sao_Paulo'))
        except Exception as e:
            current_app.logger.error(f"Erro ao processar data_retirada: {e}")
            return "Erro ao processar as datas", 500

        data.append([
                farmacia.nomeFantasia,
                farmacia.cnpj,
                transacao.nome_beneficiado,
                transacao.cpf_beneficiado,          
                transacao.marca_fralda_entregue,
                transacao.tamanho_fralda,   
                transacao.quantidade,
                transacao.quantidade_total,
                data_retirada.strftime('%d-%m-%Y %H:%M:%S')
        ])

    df = pd.DataFrame(data, columns=[
'Nome Fantasia', 'CNPJ', 'Nome do beneficiado contemplado','CPF do beneficiado contemplado',  'Marca', 'Tamanho', 'Quantidade Pega', 'Quantidade','Data'
    ])

    output = BytesIO()
    df.to_csv(output, index=False)
    output.seek(0)

    response = make_response(output.getvalue().decode('utf-8'))
    response.headers['Content-Type'] = 'text/csv'
    response.headers['Content-Disposition'] = f'attachment; filename=planilha_{mes_filter or "Todos"}_{ano_filter or "Todos"}.csv'

    return response
