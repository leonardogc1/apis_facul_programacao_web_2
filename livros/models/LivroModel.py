from database.database import get_connection
from models.entities.Livro import Livro
from database.request_handler import request_handler
from flask import request
import logging

class LivroModel():

    @classmethod
    def get_livros(self):
        try:
            request_information = request_handler(request)
            args = request_information.get_args()

            connection = get_connection()
            livros = []

            with connection.cursor() as cursor:
                sql = '''
                    SELECT id, 
                           lvr_nome, 
                           lvr_autor,
                           lvr_genero,
                           lvr_ano,
                           lvr_codigo
                           FROM livros                          
                           ORDER BY lvr_nome;
                '''
                cursor.execute(sql,)
                resultset = cursor.fetchall()

                for row in resultset:
                    livro = Livro(row[0], row[1], row[2], row[3], row[4], row[5])
                    livros.append(livro.to_JSON())

            connection.close()
            return livros
        except Exception as ex:
            logging.exception(ex)
            connection.rollback()
            raise Exception(ex)


    @classmethod
    def get_livro(self, id):
        try:
            connection = get_connection()

            with connection.cursor() as cursor:
                sql = '''
                    SELECT id, 
                           lvr_nome, 
                           lvr_autor,
                           lvr_genero,
                           lvr_ano,
                           lvr_codigo
                           FROM livros 
                           WHERE id = %s
                '''
                cursor.execute(sql, (id))
                row = cursor.fetchone()
                
                livro = None
                if row != None:
                    livro = Livro(row[0], row[1], row[2], row[3], row[4], row[5])
                    livro = livro.to_JSON()

            connection.close()
            return livro
        except Exception as ex:
            raise Exception(ex)


    @classmethod
    def add_livro(self, nome, autor, genero, ano, codigo):
        try:
            connection = get_connection()
            
            id = int(LivroModel.get_id() + 1)

            with connection.cursor() as cursor:
                sql = '''
                    INSERT INTO livros (
                           id, 
                           lvr_nome, 
                           lvr_autor,
                           lvr_genero,
                           lvr_ano,
                           lvr_codigo)
                    VALUES(
                            %s,
                            %s,
                            %s,
                            %s,
                            %s,
                            %s
                        )
                    '''             
                cursor.execute(sql, [id, nome, autor, genero, ano, codigo])

                affected_rows = cursor.rowcount
                connection.commit()

            connection.close()
            return affected_rows
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def update_livro(self, livro):
        try:
            connection = get_connection()

            with connection.cursor() as cursor:
                sql = '''
                    UPDATE livros
                    SET lvr_nome = %s,
                        lvr_autor = %s,
                        lvr_genero = %s,
                        lvr_ano = %s,
                        lvr_codigo = %s
                    WHERE id = %s
                    '''
                cursor.execute(sql, (livro.nome, livro.autor,
                    livro.genero, livro.ano, livro.codigo, livro.id))
                
                affected_rows = cursor.rowcount
                connection.commit()

            connection.close()
            return affected_rows
        except Exception as ex:
            raise Exception(ex)
        

    @classmethod
    def delete_livro(self, id):
        try:
            
            connection = get_connection()
            with connection.cursor() as cursor:
                sql = '''
                    DELETE FROM livros
                    WHERE id = %s
                '''
                cursor.execute(sql, (id, ))
                affected_rows = cursor.rowcount
                connection.commit()

            connection.close()
            
            return affected_rows
        except Exception as ex:
            raise Exception(ex)
    

    @classmethod
    def get_id(self):
        try:
            connection = get_connection()
            
            with connection.cursor() as cursor:
                sql = '''
                    SELECT id
                    FROM livros
                    ORDER BY id DESC
                    LIMIT 1;
                '''
                cursor.execute(sql)
                resultone = cursor.fetchall()
                id = resultone[0][0]

            connection.close()
            return id
        except Exception as ex:
            raise Exception(ex)