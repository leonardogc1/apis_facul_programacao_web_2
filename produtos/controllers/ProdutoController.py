from flask import Blueprint, jsonify, request
from flask_restx import Resource, Namespace, reqparse, fields, marshal_with
from database.request_handler import request_handler

# Entities
from models.entities.Produto import Produto
# Models
from models.ProdutoModel import ProdutoModel

##
produto_ = Namespace('produto', description='Produtos feature set')

fields_produto = produto_.model('produto', {
    'id': fields.Integer,
    'nome': fields.String,
    'categoria': fields.String,
    'preco': fields.String,
    'quantidade': fields.String,
    'lote': fields.String
})

@produto_.route('/produtos')
class ProdutoController(Resource):
    def get(self):
        try:
            produtos = ProdutoModel.get_produtos()
            return jsonify({'status_message': '',
                            'payload':produtos,
                            "codigo":200})
        except Exception as ex:
            return jsonify({'message': str(ex), "codigo": 500})


@produto_.route('/produtos/<id>')
class ProdutoController(Resource):
    def get(self, id):
        try:
            produto = ProdutoModel.get_produto(id)
            if produto != None:
                return jsonify({'status_message': '',
                            'payload':produto,
                            'codigo':200})
            else:
                return jsonify({'status_message': 'Produto não encontrado',
                            "codigo": 404})
        except Exception as ex:
            return jsonify({'message': str(ex), "codigo": 500})


@produto_.route('/adiciona-produto')
class ProdutoController(Resource):
    #@produto_.doc(body=fields_produto)
    def post(self):
        try:
            requestInformation = request_handler(request)
            args = requestInformation.get_args()
            nome = args['nome'] if 'nome' in args else None
            categoria = args['categoria'] if 'categoria' in args else None
            preco = float(args['preco']) if 'preco' in args else None
            quantidade = int(args['quantidade']) if 'quantidade' in args else None
            lote = args['lote'] if 'lote' in args else None

            affected_rows = ProdutoModel.add_produto(nome, categoria, preco, quantidade, lote)
            if affected_rows == 1:
                return jsonify({'message': "Produto adicionado", "codigo": 200})
            else:
                return jsonify({'message': "Erro ao adicionar Produto", "codigo": 500})

        except Exception as ex:
            return jsonify({'message': str(ex), "codigo": 500})


@produto_.route('/edita-produto/<id>')
class ProdutoController(Resource):
    @produto_.doc(body=fields_produto)
    def put(self, id):
        try:
            requestInformation = request_handler(request)
            args = requestInformation.get_args()
            nome = args['nome'] if 'nome' in args else None
            categoria = args['categoria'] if 'categoria' in args else None
            preco = float(args['preco']) if 'preco' in args else None
            quantidade = int(args['quantidade']) if 'quantidade' in args else None
            lote= args['lote'] if 'lote' in args else None
            produto = Produto(id, nome, categoria, preco, quantidade, lote)

            affected_rows = ProdutoModel.update_produto(produto)
            if affected_rows == 1:
                return jsonify({'message': "Produto atualizado", "codigo": 200})
            else:
                return jsonify({'message': "Produto não atualizado", "codigo": 400})

        except Exception as ex:
            return jsonify({'message': str(ex), "codigo": 500})


@produto_.route('/delete-produto/<id>')
class ProdutoController(Resource):
    def delete(self, id):
        try:
            affected_rows = ProdutoModel.delete_produto(id)

            if affected_rows == 1:
                return jsonify({'message': "Produto deletado!", "codigo": 200})
            else:
                return jsonify({'message': "Produto não deletado!", "codigo": 404})

        except Exception as ex:
            return jsonify({'message': str(ex), "codigo": 500})