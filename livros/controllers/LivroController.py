from flask import Blueprint, jsonify, request
from flask_restx import Resource, Namespace, reqparse, fields, marshal_with
from database.request_handler import request_handler

# Entities
from models.entities.Livro import Livro
# Models
from models.LivroModel import LivroModel

##
livro_ = Namespace('livro', description='Livros feature set')

fields_livro = livro_.model('livro', {
    'id': fields.Integer,
    'nome': fields.String,
    'autor': fields.String,
    'genero': fields.String,
    'ano': fields.String,
    'codigo': fields.String
})

@livro_.route('/livros')
class LivroController(Resource):
    def get(self):
        try:
            livros = LivroModel.get_livros()
            return jsonify({'status_message': '',
                            'payload':livros,
                            "codigo":200})
        except Exception as ex:
            return jsonify({'message': str(ex), "codigo": 500})


@livro_.route('/livros/<id>')
class LivroController(Resource):
    def get(self, id):
        try:
            livro = LivroModel.get_livro(id)
            if livro != None:
                return jsonify({'status_message': '',
                            'payload':livro,
                            'codigo':200})
            else:
                return jsonify({'status_message': 'Livro não encontrado',
                            "codigo": 404})
        except Exception as ex:
            return jsonify({'message': str(ex), "codigo": 500})


@livro_.route('/adiciona-livro')
class LivroController(Resource):
    #@livro_.doc(body=fields_livro)
    def post(self):
        try:
            print(request.args)
            requestInformation = request_handler(request)
            args = requestInformation.get_args()
            nome = args['nome'] if 'nome' in args else None
            autor = args['autor'] if 'autor' in args else None
            genero = args['genero'] if 'genero' in args else None
            ano = args['ano'] if 'ano' in args else None
            codigo = args['codigo'] if 'codigo' in args else None
            print(nome)

            affected_rows = LivroModel.add_livro(nome, autor, genero, ano, codigo)
            if affected_rows == 1:
                return jsonify({'message': "Livro adicionado", "codigo": 200})
            else:
                return jsonify({'message': "Erro ao adicionar Livro", "codigo": 500})

        except Exception as ex:
            return jsonify({'message': str(ex), "codigo": 500})


@livro_.route('/edita-livro/<id>')
class LivroController(Resource):
    @livro_.doc(body=fields_livro)
    def put(self, id):
        try:
            requestInformation = request_handler(request)
            args = requestInformation.get_args()
            nome = args['nome'] if 'nome' in args else None
            autor = args['autor'] if 'autor' in args else None
            genero = args['genero'] if 'genero' in args else None
            ano = args['ano'] if 'ano' in args else None
            codigo = args['codigo'] if 'codigo' in args else None
            livro = Livro(id, nome, autor, genero, ano, codigo)

            affected_rows = LivroModel.update_livro(livro)
            if affected_rows == 1:
                return jsonify({'message': "Livro atualizado", "codigo": 200})
            else:
                return jsonify({'message': "Livro não atualizado", "codigo": 400})

        except Exception as ex:
            return jsonify({'message': str(ex), "codigo": 500})


@livro_.route('/delete-livro/<id>')
class LivroController(Resource):
    def delete(self, id):
        try:
            print(id)
            affected_rows = LivroModel.delete_livro(id)

            if affected_rows == 1:
                return jsonify({'message': "Livro deletado!", "codigo": 200})
            else:
                return jsonify({'message': "Livro não deletado!", "codigo": 404})

        except Exception as ex:
            return jsonify({'message': str(ex), "codigo": 500})