from flask_sqlalchemy import SQLAlchemy

# criando a instância do SQLAlchemy 
db = SQLAlchemy()

# quando eu rodar a aplicação pela primeira vez, a ORM vai criar as entidades 
class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150))
    year = db.Column(db.Integer)
    category = db.Column(db.String(150))
    plataform = db.Column(db.String(150))
    price = db.Column(db.Float)
    quantity = db.Column(db.Integer)
    
    # método construtor da classe
    def __init__(self, title, year, category, plataform, price, quantity):
        self.title = title
        self.year = year
        self.category = category
        self.plataform = plataform
        self.price = price
        self.quantity = quantity
        
    
    
    
    
    