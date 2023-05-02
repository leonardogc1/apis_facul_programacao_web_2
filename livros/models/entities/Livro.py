class Livro():
    
    def __init__(self, id, nome, autor, genero, ano, codigo):
        self.id = id
        self.nome = nome
        self.autor = autor
        self.genero = genero
        self.ano = ano
        self.codigo = codigo
    
    def to_JSON(self):
       return {
            'id': self.id,
            'nome': self.nome,
            'autor': self.autor,
            'genero': self.genero,
            'ano': self.ano,
            'codigo': self.codigo
       }