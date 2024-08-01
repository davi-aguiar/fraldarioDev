#importações
from datetime import datetime
import socket
import uuid
import subprocess
from flask import Flask, redirect, url_for, flash, request, render_template, session,jsonify, send_file, abort
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
from decimal import Decimal, ROUND_HALF_UP
from fpdf import FPDF
import pandas as pd
from werkzeug.utils import secure_filename
from datetime import datetime
import os
from flask import send_from_directory
from flask import Flask, make_response
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from sqlalchemy import LargeBinary, func
from itsdangerous import URLSafeTimedSerializer
from flask import current_app
from itsdangerous import BadSignature, URLSafeTimedSerializer, SignatureExpired
from itsdangerous import URLSafeTimedSerializer, SignatureExpired,BadSignature
from flask import Flask, render_template, request, send_file,make_response
from openpyxl import Workbook
from io import BytesIO
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mail import Mail, Message
import pandas as pd
from sqlalchemy import func
from dashboards.dash_app import create_dash_app
from dashboards.dashA import create_dashboard_autorizador
from dashboards.dashBeneficiados import create_dashboard_beneficiado
from sqlalchemy import func
from datetime import datetime
from collections import Counter
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
import requests
from routes.inicio import inicio_route
from routes.prefeitura import prefeitura_route
from routes.farmacia import farmacia_route
from routes.autorizador import autorizador_route 
# Criar instância do Flask
app = Flask(__name__, template_folder='templates')
#duração das flash message
app.config['MESSAGE_FLASHING_OPTIONS'] = {'duration': 5}
app.register_blueprint(inicio_route)
app.register_blueprint(prefeitura_route, url_prefix='/prefeitura')
app.register_blueprint(autorizador_route, url_prefix='/autorizador')
app.register_blueprint(farmacia_route, url_prefix='/farmacia')
# Configurar o SQLAlchemy
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)

# Configurar o envio de email
app.secret_key = os.urandom(24)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587  # Porta do servidor SMTP do Gmail
app.config['MAIL_USE_TLS'] = True  # Usar TLS (Transport Layer Security)
app.config['MAIL_USERNAME'] = 'kevynlevi0@gmail.com'  # Seu email do Gmail
app.config['MAIL_PASSWORD'] = 'tzgw vnhu rbhp xftg'  # Sua senha do Gmail
app.config['MAIL_DEFAULT_SENDER'] = 'kevynlevi0@gmail.com'  # Configuração do remetente padrão
app.config['TIMEZONE'] = 'America/Sao_Paulo'
s = URLSafeTimedSerializer(app.config['SECRET_KEY'],salt="activate")
mail = Mail(app)

# Configurar o LoginManager
login_manager = LoginManager(app)
login_manager.init_app(app)

# Definir as extensões de arquivo permitidas para upload
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


def capitalize_string(s):
    return s.capitalize() if s else s


class User(UserMixin):
    def __init__(self, user_id):
        self.id = user_id


class UsuarioTemp(db.Model):
    __tablename__ = 'usuariotemp'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    senha = db.Column(db.String(255), nullable=False)
    tipo_login = db.Column(db.String(255))
    tipos_fralda = db.Column(db.String(20), nullable=True)
    tamanho_fralda = db.Column(db.String(20), nullable=True)
    cpf = db.Column(db.String(11), nullable=True)
    cnpj = db.Column(db.String(14), nullable=True)
    nome = db.Column(db.String(255), nullable=False)
    cep = db.Column(db.String(9), nullable=True)
    logradouro = db.Column(db.String(255), nullable=True)
    numero = db.Column(db.String(10), nullable=True)
    complemento = db.Column(db.String(255), nullable=True)
    bairro = db.Column(db.String(255), nullable=True)
    cidade = db.Column(db.String(255), nullable=True)
    estado = db.Column(db.String(2), nullable=True)
    documento_liberacao = db.Column(db.BLOB, nullable=True)
    
class Usuario(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    senha = db.Column(db.String(255), nullable=False)
    tipo_usuario = db.Column(db.String(255))
    farmacia = db.relationship('Farmacia', back_populates='usuario', uselist=False, overlaps="farmacia,usuario")
    autorizador = db.relationship('Autorizador', back_populates='usuario', uselist=False, overlaps="autorizador,usuario")
    prefeitura = db.relationship('Prefeitura', back_populates='usuario', uselist=False, overlaps="prefeitura,usuario")
    email_confirmed = db.Column(db.Boolean, default=False)
    first_login = db.Column(db.Boolean, default=True)
    ativo = db.Column(db.Boolean, default=True)
    
    @property
    def is_active(self):
        return self.email_confirmed

class Farmacia(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cnpj = db.Column(db.String(18), unique=True, nullable=False)
    cnpj_pesquisado = db.Column(db.String(14), nullable=False, default='')
    nomeFantasia = db.Column(db.String(255), nullable=False)
    quantidadeTotal = db.Column(db.Integer, nullable=True, default=0)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    usuario = db.relationship('Usuario', back_populates='farmacia')
    data_retirada = db.Column(db.DateTime, default=datetime.utcnow) 
    transacoes = db.relationship('Transacao', backref='farmacia', lazy=True)
    data_criacao = db.Column(db.Date)
    tipos_fralda = db.Column(db.String(20), nullable=False)
    tamanho_fralda = db.Column(db.String(20), nullable=True)
    cep = db.Column(db.String(9), nullable=True)
    logradouro = db.Column(db.String(255), nullable=False)
    numero = db.Column(db.String(10), nullable=False)
    complemento = db.Column(db.String(255))
    bairro = db.Column(db.String(255))
    cidade = db.Column(db.String(255), nullable=False)
    estado = db.Column(db.String(2), nullable=False)
    documento_liberacao = db.Column(db.LargeBinary, nullable=False, default=None)

class Transacao(db.Model):
    __tablename__ = 'transacao'
    id = db.Column(db.Integer, primary_key=True)
    quantidadeTotal = db.Column(db.Integer, nullable=True, default=0)
    farmacia_id = db.Column(db.Integer, db.ForeignKey('farmacia.id'), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    marca_fralda_entregue = db.Column(db.String(20), nullable=False)
    data_retirada = db.Column(db.DateTime, default=datetime.utcnow) 
    #mes = db.Column(db.String(7), nullable=True, default="0")
    media_tamanho_fralda = db.Column(db.String(10), nullable=True, default="0") 
    tamanho_fralda = db.Column(db.String(20), nullable=True, default="0")
    #tamanho_fralda = db.Column(db.String(50), nullable=True)
    media_marca_fralda = db.Column(db.String(20), nullable=False, default=0.0)
class TransacaoA(db.Model):
    __tablename__ = 'transacaoA'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    autorizador_id = db.Column(db.Integer, db.ForeignKey('autorizador.id'), nullable=False)
    quantidadeBeneficiado = db.Column(db.Integer, nullable=True, default=1)
    total_por_mes = db.Column(db.Float, default=0.0)  # Use db.Float para total_por_mes
    detalhes_beneficiados = db.Column(db.String(255))
    cpf_beneficiadoA = db.Column(db.String(40))
    media = db.Column(db.Float)
    data_retirada = db.Column(db.DateTime, default=datetime.utcnow)

    # Relacionamento com Autorizador
    autorizador = db.relationship('Autorizador', backref='transacoes')
class Autorizador(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cpf = db.Column(db.String(11), unique=True, nullable=False)
    cpf_pesquisado = db.Column(db.String(11), nullable=False, default='')
    nomeAutorizador = db.Column(db.String(255), nullable=False)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    usuario = db.relationship('Usuario', back_populates='autorizador')
    documento_liberacao = db.Column(db.LargeBinary, nullable=True, default=None)

class Prefeitura(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    cpf_prefeitura = db.Column(db.String(11), unique=True, nullable=False, default='')
    nomePrefeitura = db.Column(db.String(255), nullable=False)
    usuario = db.relationship('Usuario', back_populates='prefeitura')
    documento_liberacao = db.Column(db.LargeBinary, nullable=True, default=None)
class Beneficiado(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome_beneficiado = db.Column(db.String(255), nullable=False)
    marca_fralda = db.Column(db.String(255), nullable=False)
    cpf_beneficiado = db.Column(db.String(14), nullable=False, default='')
    cpfPesquisado = db.Column(db.String(14), nullable=False, default='valor_padrão')
    usuarioPendente = db.Column(db.String(14), nullable=False, default='valor_padrão')
    pendente = db.Column(db.Boolean, default=False)
    cartao_sus = db.Column(db.String(20), nullable=False)
    nome_autorizado = db.Column(db.String(255), nullable=False)
    cpf_autorizado = db.Column(db.String(14), nullable=False)
    quantidade_liberada = db.Column(db.Integer, nullable=False)
    quantidade_pego = db.Column(db.Integer, nullable=False, default=0)
    quantidade_restante = db.Column(db.Integer, nullable=False, default=0)
    quantidadeTotal = db.Column(db.Integer, nullable=False, default=0)
    usuario_pendente = db.Column(db.String(255), nullable=False)
    tamanho_liberado = db.Column(db.String(50), nullable=False)
    motivo_liberacao = db.Column(db.String(255), nullable=False)
    data_inicio = db.Column(db.Date, nullable=False)
    validade_meses = db.Column(db.Integer, nullable=False)
    documento = db.Column(db.BLOB, nullable=False)
    licitacao = db.Column(db.BLOB, nullable=True, default=0)
    id_autorizador = db.Column(db.Integer, db.ForeignKey('autorizador.id'))
    id_prefeitura = db.Column(db.Integer, db.ForeignKey('prefeitura.id'))  # Chave estrangeira para autorizador

    # Relacionamento com Autorizador
    autorizador = db.relationship('Autorizador', backref='beneficiados')

class Dados(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    media_tamanho_fralda = db.Column(db.Float)
    media_quantidade_fralda = db.Column(db.Float)
class DadosA(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)