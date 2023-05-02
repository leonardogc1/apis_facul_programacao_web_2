from flask import Blueprint
from flask_restx import Api

from controllers.LivroController import livro_

blueprint = Blueprint('api_livros', __name__, url_prefix='/livros/v1.0')
api = Api(blueprint, title = 'Livros API', version = '1.0', description = 'Livros features', contact = '', catch_all_404s = True, ordered = True)

api.add_namespace(livro_)
