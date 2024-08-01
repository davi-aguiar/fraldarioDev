from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from flask_admin import Admin 
from sqlalchemy.orm import relationship


db = SQLAlchemy()

# admin = Admin(  name = "Painel de Controle", template_mode='bootstrap4')

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
    razaoSocial = db.Column(db.String(255), nullable=True)
    cep = db.Column(db.String(9), nullable=True)
    logradouro = db.Column(db.String(255), nullable=True)
    numero = db.Column(db.String(10), nullable=True)
    complemento = db.Column(db.String(255), nullable=True)
    bairro = db.Column(db.String(255), nullable=True)
    cidade = db.Column(db.String(255), nullable=True)
    estado = db.Column(db.String(2), nullable=True)
    documento_liberacao = db.Column(db.BLOB, nullable=True)
    funcoes = db.Column(db.String(255), nullable=True)

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
    is_admin = db.Column(db.Boolean, default=False)
    is_root = db.Column(db.Boolean, default=False)
    funcoes = db.Column(db.String(255), nullable=True)
    def has_function(self, function):
        # Verifica se self.funcoes não é None antes de tentar dividir
        if self.funcoes:
            return function in [func.strip() for func in self.funcoes.split(',')]
        return False  # Retorna False se não houver funções
    @property
    def is_active(self):
        return self.email_confirmed
# class Funcao():
#     __tablename__ = 'funcao'
    
#     id = db.Column(Integer, primary_key=True, autoincrement=True)
#     nome = Column(String, nullable=False)
#     descricao = Column(String)
    
#     # Relacionamento com a tabela de usuários
#     usuarios = relationship("Usuario", secondary="usuario_funcao")

# Tabela de associação entre Usuario e Funcao
# class UsuarioFuncao(Base):
#     __tablename__ = 'usuario_funcao'
    
#     usuario_id = Column(Integer, ForeignKey('usuario.id'), primary_key=True)
#     funcao_id = Column(Integer, ForeignKey('funcao.id'), primary_key=True)

# class Controller(ModelView):
#     def is_acessible(self):
#         return current_user.is_authenticated
#     def not_acessible_message(self):
#         return 'Faça login para acessar esta página'
    

# admin.add_view(Controller(Usuario, db.session))

class Farmacia(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cnpj = db.Column(db.String(18), unique=True, nullable=False)
    cnpj_pesquisado = db.Column(db.String(14), nullable=False, default='')
    nomeFantasia = db.Column(db.String(255), nullable=False)
    razaoSocial = db.Column(db.String(255), nullable=True)  # Adicionada a nova coluna
    quantidade = db.Column(db.Integer, nullable=True, default=0)
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
    documento_liberacao = db.Column(db.BLOB, nullable=True)
    data_cadastro = db.Column(db.DateTime, default=datetime.utcnow)

class Transacao(db.Model):
    __tablename__ = 'transacao'
    id = db.Column(db.Integer, primary_key=True)
    farmacia_id = db.Column(db.Integer, db.ForeignKey('farmacia.id'), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False) 
    marca_fralda_entregue = db.Column(db.String(20), nullable=False)
    data_retirada = db.Column(db.DateTime, default=datetime.utcnow)
    media_tamanho_fralda = db.Column(db.String(10), nullable=True, default="0")
    tamanho_fralda = db.Column(db.String(20), nullable=True, default="0")
    quantidade_total = db.Column(db.Integer, nullable=False, default=0.0)
    nome_beneficiado = db.Column(db.String(100), nullable=False)
    cpf_beneficiado = db.Column(db.String(20), nullable=False)
    farmacia_relacionamento = relationship("Farmacia", backref="transacoes_associadas", overlaps="farmacia,transacoes")
class TransacaoA(db.Model):
    __tablename__ = 'transacaoA'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    autorizador_id = db.Column(db.Integer, db.ForeignKey('autorizador.id'), nullable=False)
    quantidadeBeneficiado = db.Column(db.Integer, nullable=True, default=1)
    total_por_mes = db.Column(db.Float, default=0.0)
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
    __tablename__ = 'beneficiado'

    id = db.Column(db.Integer, primary_key=True)
    nome_beneficiado = db.Column(db.String(255), nullable=False)
    marca_fralda = db.Column(db.String(255), nullable=False)
    cpf_beneficiado = db.Column(db.String(14), nullable=False, unique=True)
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
    licitacao = db.Column(db.LargeBinary)
    id_autorizador = db.Column(db.Integer, db.ForeignKey('autorizador.id'))
    id_prefeitura = db.Column(db.Integer, db.ForeignKey('prefeitura.id'))
    data_cadastro = db.Column(db.DateTime, default=datetime.utcnow)
    data_final = db.Column(db.DateTime, default=datetime.utcnow)
    confirmacao = db.Column(db.Boolean, default=False)
    ativo = db.Column(db.Boolean, default=True)

    # Relationships
    autorizador = db.relationship('Autorizador', backref='beneficiados')
    documentos = db.relationship('Documento', back_populates='beneficiado')
class Dados(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    media_tamanho_fralda = db.Column(db.Float)
    media_quantidade_fralda = db.Column(db.Float)

class DadosA(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

class DadosTemporarios(db.Model):
    __tablename__ = 'dadostemporarios'
    id = db.Column(db.Integer, primary_key=True)
    beneficiado_id = db.Column(db.Integer, db.ForeignKey('beneficiado.id'))
    quantidade_liberada = db.Column(db.Integer)
    tamanho_liberado = db.Column(db.String(50))
    motivo_liberacao = db.Column(db.String(200))
    data_inicio = db.Column(db.Date)
    validade_meses = db.Column(db.Integer)
class JustificativaAutorizador(db.Model):
    __tablename__ = 'justificativaautorizador'
    id = db.Column(db.Integer, primary_key=True)
    autorizador_id = db.Column(db.Integer, db.ForeignKey('autorizador.id'))
    motivo_liberacao = db.Column(db.String(200))
    nome_beneficiado= db.Column(db.String(50))
    cpf_beneficiado=db.Column(db.String(14))
    data_inicio = db.Column(db.Date)
 
    


# pagina inicial

class PaginaInicial(db.Model):
    __tablename__ = 'paginainicial'  # Nome correto da tabela no banco de dados
    
    id = db.Column(db.Integer, primary_key=True)
    capa = db.Column(db.String(100), nullable=True)
    titulo = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    beneficiarios_adultos = db.Column(db.Text, nullable=False)
    beneficiarios_criancas = db.Column(db.Text, nullable=False)
    objetivo1 = db.Column(db.Text, nullable=False)
    objetivo2 = db.Column(db.Text, nullable=False)
    objetivo3 = db.Column(db.Text, nullable=False)

from sqlalchemy import Column, Integer, LargeBinary, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Documento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    beneficiado_id = db.Column(db.Integer, db.ForeignKey('beneficiado.id'))
    licitacao = db.Column(LargeBinary)

    
    # Relationship
    beneficiado = relationship("Beneficiado", back_populates="documentos")
