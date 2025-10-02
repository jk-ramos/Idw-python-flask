from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Modelo para Leitores
class Leitor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150))
    telefone = db.Column(db.String(20))
    data_cadastro = db.Column(db.String(10))
    
    # Relacionamento com empréstimos
    emprestimos = db.relationship('Emprestimo', backref='leitor', lazy=True, cascade='all, delete-orphan')
    
    def __init__(self, nome, email, telefone, data_cadastro):
        self.nome = nome
        self.email = email
        self.telefone = telefone
        self.data_cadastro = data_cadastro


# Modelo para Livros
class Livro(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    autor = db.Column(db.String(150), nullable=False)
    ano = db.Column(db.Integer)
    categoria = db.Column(db.String(100))
    isbn = db.Column(db.String(50))
    quantidade = db.Column(db.Integer, default=1)
    disponivel = db.Column(db.String(10), default='Sim')
    
    # Relacionamento com empréstimos
    emprestimos = db.relationship('Emprestimo', backref='livro', lazy=True, cascade='all, delete-orphan')
    
    def __init__(self, titulo, autor, ano, categoria, isbn, quantidade):
        self.titulo = titulo
        self.autor = autor
        self.ano = ano
        self.categoria = categoria
        self.isbn = isbn
        self.quantidade = quantidade
        self.disponivel = 'Sim' if quantidade > 0 else 'Não'


# Modelo para Empréstimos (relacionamento entre Leitores e Livros)
class Emprestimo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    leitor_id = db.Column(db.Integer, db.ForeignKey('leitor.id'), nullable=False)
    livro_id = db.Column(db.Integer, db.ForeignKey('livro.id'), nullable=False)
    data_emprestimo = db.Column(db.String(10), nullable=False)
    data_devolucao = db.Column(db.String(10))
    status = db.Column(db.String(20), default='Emprestado')
    
    def __init__(self, leitor_id, livro_id, data_emprestimo, data_devolucao):
        self.leitor_id = leitor_id
        self.livro_id = livro_id
        self.data_emprestimo = data_emprestimo
        self.data_devolucao = data_devolucao
        self.status = 'Emprestado'