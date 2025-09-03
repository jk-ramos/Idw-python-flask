from flask import render_template, request, redirect, url_for
import urllib #envia requisições pra uma URL
import json #conversão de dados de json pra dicionário 


def init_app(app):
    # lista 
    # a lista veio pra cá pq dentro da função ela era reiniciada a cada requisição
    players = ['Giovana', 'Amanda', 'Igor', 'Diego']
    gamelist = [{'Título': 'CS 1.6', 'Ano': 1996, 'Categoria': 'FPS Online'}]
    
    
    # definindo a rota principal da aplicação '/'
    @app.route('/')
    # toda rota precisa de um função para executar 
    def home():
        return render_template('index.html')


    # definindo a rota principal da aplicação '/'
    @app.route('/games', methods=['GET', 'POST'])
    # toda rota precisa de um função para executar 
    def games():
        # essas variáveis estariam vindo de fora 
        title = 'Tarisland'
        year = 2022
        category = 'MMORPG'
        # dicionário 
        console = {'Nome' : 'PS5', 'Fabricante': 'Sony', 'Ano': 2020}
        
        # tratando uma requisição POST com request
        if request.method == 'POST':
            # coletando o texto da input 
            # player é o nome da caixinha que eu criei no form
            if request.form.get('player'):
                players.append(request.form.get('player'))
                return redirect(url_for('games'))
        
        # o primeiro title é a var que vai ser criada na página 
        return render_template('games.html', title=title, year=year, category=category, players=players, console=console)
    
    
    @app.route('/newGame', methods=['GET', 'POST'])
    def newGame():
        if request.method == 'POST':
            if request.form.get('title') and request.form.get('year') and request.form.get('category'):
                gamelist.append({'Título': request.form.get('title'), 'Ano': request.form.get('year'), 'Categoria' : request.form.get('category')})
                return redirect(url_for('newGame'))
                
        return render_template('newGame.html', gamelist=gamelist)
    
    @app.route("/apigames", methods=['GET', 'POST'])
    # criando parâmetros para a rota
    @app.route('/apigames/<int:id>', methods=['GET', 'POST'])
    def apigames(id=None):
        # para deixar o parâmetro opcional, devo colocar dentro da função: id=None
        url = 'https://www.freetogame.com/api/games'
        response = urllib.request.urlopen(url) # pega a resposta da api
        data = response.read() # lê os dados da resposta
        gamesList = json.loads(data) # pega o json e transforma em um dicionário 
        # verificando se o parâmetro foi enviado
        if id:
            gameInfo = [] # o game que eu passei na url
            for game in gamesList:
                if game['id'] == id: #comparando o id do jogo com o id passado como parâmetro na url 
                    gameInfo = game
                    break
            if gameInfo:
                return render_template('gameInfo.html', gameInfo=gameInfo)
            else:
                return f'Game com a ID {id} não encontrado.'
        else:
            return render_template('apigames.html', gamesList=gamesList)

