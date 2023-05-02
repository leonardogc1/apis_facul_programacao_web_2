from flask import Blueprint
from flask_restx import Api

from controllers.ProdutoController import produto_

blueprint = Blueprint('api_produtos', __name__, url_prefix='/produtos/v1.0')
api = Api(blueprint, title = 'Produtos API', version = '1.0', description = 'Produtos features', contact = '', catch_all_404s = True, ordered = True)

api.add_namespace(produto_)
