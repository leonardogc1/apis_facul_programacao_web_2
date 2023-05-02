from database.database import get_connection
from models.entities.Produto import Produto
from database.request_handler import request_handler
from flask import request
import logging

class ProdutoModel():

    @classmethod
    def get_produtos(self):
        try:
            request_information = request_handler(request)
            args = request_information.get_args()

            connection = get_connection()
            produtos = []

            with connection.cursor() as cursor:
                sql = '''
                    SELECT id, 
                           prd_nome, 
                           prd_categoria,
                           prd_preco,
                           prd_quantidade,
                           prd_lote
                           FROM produtos                          
                           ORDER BY prd_nome;
                '''
                cursor.execute(sql,)
                resultset = cursor.fetchall()

                for row in resultset:
                    produto = Produto(row[0], row[1], row[2], row[3], row[4], row[5])
                    produtos.append(produto.to_JSON())

            connection.close()
            return produtos
        except Exception as ex:
            logging.exception(ex)
            connection.rollback()
            raise Exception(ex)


    @classmethod
    def get_produto(self, id):
        try:
            connection = get_connection()

            with connection.cursor() as cursor:
                sql = '''
                    SELECT id, 
                           prd_nome, 
                           prd_categoria,
                           prd_preco,
                           prd_quantidade,
                           prd_lote
                           FROM produtos 
                           WHERE id = %s
                '''
                cursor.execute(sql, (id))
                row = cursor.fetchone()
                
                produto = None
                if row != None:
                    produto = Produto(row[0], row[1], row[2], row[3], row[4], row[5])
                    produto = produto.to_JSON()

            connection.close()
            return produto
        except Exception as ex:
            raise Exception(ex)


    @classmethod
    def add_produto(self, nome, categoria, preco, quantidade, lote):
        try:
            connection = get_connection()
            
            id = int(ProdutoModel.get_id() + 1)

            with connection.cursor() as cursor:
                sql = '''
                    INSERT INTO produtos (
                           id, 
                           prd_nome, 
                           prd_categoria,
                           prd_preco,
                           prd_quantidade,
                           prd_lote)
                    VALUES(
                            %s,
                            %s,
                            %s,
                            %s,
                            %s,
                            %s
                        )
                    '''             
                cursor.execute(sql, [id, nome, categoria, preco, quantidade, lote])

                affected_rows = cursor.rowcount
                connection.commit()

            connection.close()
            return affected_rows
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def update_produto(self, produto):
        try:
            connection = get_connection()

            with connection.cursor() as cursor:
                sql = '''
                    UPDATE produtos
                    SET prd_nome = %s,
                        prd_categoria = %s,
                        prd_preco = %s,
                        prd_quantidade = %s,
                        prd_lote = %s
                    WHERE id = %s
                    '''
                cursor.execute(sql, (produto.nome, produto.categoria,
                    produto.preco, produto.quantidade, produto.lote, produto.id))
                
                affected_rows = cursor.rowcount
                connection.commit()

            connection.close()
            return affected_rows
        except Exception as ex:
            raise Exception(ex)
        

    @classmethod
    def delete_produto(self, id):
        try:
            
            connection = get_connection()
            with connection.cursor() as cursor:
                sql = '''
                    DELETE FROM produtos
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
                    FROM produtos
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