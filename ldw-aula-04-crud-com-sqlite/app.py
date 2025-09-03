# do pacote importo o Flask 
# render_template renderiza páginas HTML 
from flask import Flask, render_template
from controllers import routes
from models.database import db
# importando a biblioteca para manipulação do S.O
import os

# Criando uma instância do Flask 
app = Flask(__name__, template_folder='views') # esse parâmetro representa o nome da aplicação

routes.init_app(app)

# extraindo o diretório absoluto do arquivo
dir = os.path.abspath(os.path.dirname(__file__))

# criando o arquivo do banco 
app.config['SQlALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(dir, 'models/games.sqlite3')

# se for executado diretamente peloo interpretador 
# camada de segurança; se eu importar o app em outro arquivo, não vai rodar o servidor;
if __name__ == '__main__':
    # enviando o flask para o SQLALCHEMY
    db.init_app(app=app)
    # verificar no início da aplicação se o banco já existe. Se não, ele cria 
    # a palavra with inicia e termina determinado processo pra não ficar em aberto, é uma questão de segurança 
    with app.test_request_context():
        db.create_all()
    # iniciando o servidor
    app.run(host="localhost", port=5000, debug=True) 

 
