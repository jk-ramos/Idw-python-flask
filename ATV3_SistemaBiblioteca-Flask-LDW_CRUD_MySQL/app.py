# Importando o Flask
from flask import Flask
# Importando o controller (routes.py)
from controllers import routes
# Importando o model
from models.database import db
import pymysql

# Define o nome do banco de dados
DB_NAME = 'biblioteca'

# Criando uma instância do Flask
app = Flask(__name__, template_folder="views", static_folder="static")

# Configuração do banco de dados
app.config['DATABASE_NAME'] = DB_NAME
# Passando o endereço do banco ao SQLAlchemy
# ALTERE 'root' e 'admin' de acordo com seu usuário e senha do MySQL
# Passando o endereço do banco ao SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://root@localhost/{DB_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializando as rotas
routes.init_app(app)

# Se for executado diretamente pelo interpretador
if __name__ == "__main__":
    # Conecta ao MySQL para criar o banco de dados, se necessário
    connection = pymysql.connect(
        host='localhost',
        user='root',  # seu usuário MySQL
        password='',  
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    
    try:
        with connection.cursor() as cursor:
            # Cria o banco de dados se ele não existir
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
            print(f"✓ O banco de dados '{DB_NAME}' está criado!")
    except Exception as e:
        print(f"✗ Erro ao criar o banco de dados: {e}")
    finally:
        connection.close()
    
    # Inicializa a aplicação Flask
    db.init_app(app=app)
    
    with app.test_request_context():
        # Cria as tabelas
        db.create_all()
        print("✓ Tabelas criadas com sucesso!")
    
    # Inicia o aplicativo 
    app.run(host="localhost", port=5000, debug=True)