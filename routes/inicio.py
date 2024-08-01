#importações
from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound
from models import db, PaginaInicial

#instanciando a blueprint
inicio_route = Blueprint('inicio', __name__,
                        template_folder='templates')

#rota para a tela inicial
@inicio_route.route('/')
def index():
    pagina = PaginaInicial.query.first()
    

    
    return render_template('TelaInicial.html', 
                           titulo=pagina.titulo,
                           descricao=pagina.descricao,
                           beneficiarios_adultos=pagina.beneficiarios_adultos,
                           beneficiarios_criancas=pagina.beneficiarios_criancas,
                           objetivo1=pagina.objetivo1,
                           objetivo2=pagina.objetivo2,
                           objetivo3=pagina.objetivo3,
                           capa=pagina.capa)

#rota para fazer o login
@inicio_route.route('/LoginInicial')
def indexHtml():
    return render_template("Login.html")

#rota para o faleconosco
@inicio_route.route('/faleconosco')
def faleconoscoo():
    return render_template("faleconosco.html")