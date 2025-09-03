# do pacote importo o Flask 
# render_template renderiza páginas HTML 
from flask import Flask, render_template
from controllers import routes

# Criando uma instância do Flask 
app = Flask(__name__, template_folder='views') # esse parâmetro representa o nome da aplicação

routes.init_app(app)

# se for executado diretamente peloo interpretador 
# camada de segurança; se eu importar o app em outro arquivo, não vai rodar o servidor;
if __name__ == '__main__':
    # iniciando o servidor
    app.run(host="localhost", port=5000, debug=True) 

 
