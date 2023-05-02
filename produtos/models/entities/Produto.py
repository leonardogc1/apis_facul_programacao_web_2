class Produto():
    
    def __init__(self, id, nome, categoria, preco, quantidade, lote):
        self.id = id
        self.nome = nome
        self.categoria = categoria
        self.preco = float(preco) if preco != None else 0
        self.quantidade = quantidade
        self.lote = lote
    
    def to_JSON(self):
       return {
            'id': self.id,
            'nome': self.nome,
            'categoria': self.categoria,
            'preco': self.preco,
            'quantidade': self.quantidade,
            'lote': self.lote
       }