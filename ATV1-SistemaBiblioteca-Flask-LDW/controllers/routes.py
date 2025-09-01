from flask import render_template, request, redirect, url_for

leitores = [     # Lista para nome dos leitores
    'Jaquelaine Ramos',
    'Ruan Henck',
    'Ana Clara Mendes'
]  
livros = [     # Dicionário para dados dos livros
    {
        'titulo': 'Dom Casmurro',
        'autor': 'Machado de Assis', 
        'ano': 1899,
        'categoria': 'Literatura Brasileira',
        'disponivel': 'Sim'
    },
    
    {
        'titulo': 'Orgulho e Preconceito',
        'autor': 'Jane Austen', 
        'ano': 1813,
        'categoria': 'Romance',
        'disponivel': 'Sim'
    },
    
    {
        'titulo': 'Quincas Borba',
        'autor': 'Machado de Assis', 
        'ano': 1891,
        'categoria': 'Literatura Brasileira',
        'disponivel': 'Sim'
    },
    
    {
        'titulo': 'Neuromancer',
        'autor': 'William Gibson', 
        'ano': 1984,
        'categoria': 'Ficção Científica',
        'disponivel': 'Sim'
    }
    
]

def init_app(app):
    
    @app.route('/')
    def home():
        return render_template('index.html')
    
    @app.route('/leitores', methods=['GET', 'POST'])
    def gerenciar_leitores():
        # Processa formulário (adiciona à lista)
        if request.method == 'POST':
            if request.form.get('nome_leitor'):
                leitores.append(request.form.get('nome_leitor'))
        
        return render_template('leitores.html', leitores=leitores)
    
    @app.route('/livros', methods=['GET', 'POST'])
    def gerenciar_livros():
        # Processa formulário (adiciona ao dicionário)
        if request.method == 'POST':
            titulo = request.form.get('titulo')
            autor = request.form.get('autor')
            ano = request.form.get('ano')
            categoria = request.form.get('categoria')
            
            if titulo and autor and ano and categoria:
                livros.append({
                    'titulo': titulo,
                    'autor': autor,
                    'ano': ano,
                    'categoria': categoria,
                    'disponivel': 'Sim'
                })
        
        return render_template('livros.html', livros=livros)

