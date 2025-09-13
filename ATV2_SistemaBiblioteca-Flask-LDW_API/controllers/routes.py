from flask import Flask, render_template, request, url_for
import urllib.request
import json

# Cria a instância da aplicação Flask
app = Flask(__name__)

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

@app.route('/catalogo_online')
@app.route('/catalogo_online/<string:isbn>')
def catalogo_online(isbn=None):
    
    # Consome API pública de livros - Open Library API
    # Exibe catálogo ou informações detalhadas de um livro
        
        
        if isbn:
            # Buscar informações detalhadas de um livro específico
            url = f'https://openlibrary.org/api/books?bibkeys=ISBN:{isbn}&format=json&jscmd=data'
            
            try:
                res = urllib.request.urlopen(url)
                data = res.read()
                book_data = json.loads(data)
                
                if book_data:
                    # Pega o primeiro (e único) livro retornado
                    book_key = list(book_data.keys())[0]
                    book_info = book_data[book_key]
                    
                    return render_template('livro_detalhes.html', livro=book_info, isbn=isbn)
                else:
                    return f'Livro com ISBN {isbn} não encontrado na API.'
            
            except Exception as e:
                return f'Erro ao consultar API: {str(e)}'
        
        else:
            # Exibir catálogo com livros populares (simulação com ISBNs conhecidos)
            livros_populares = [
                {
                    'isbn': '9780134685991',
                    'titulo': 'Effective Java',
                    'autor': 'Joshua Bloch',
                    'categoria': 'Programação'
                },
                {
                    'isbn': '9780596009205',
                    'titulo': 'Head First Design Patterns',
                    'autor': 'Eric Freeman',
                    'categoria': 'Programação'
                },
                {
                    'isbn': '9780134494166',
                    'titulo': 'Clean Code',
                    'autor': 'Robert Martin',
                    'categoria': 'Programação'
                },
                {
                    'isbn': '9781617294945',
                    'titulo': 'Spring in Action',
                    'autor': 'Craig Walls',
                    'categoria': 'Programação'
                },
                {
                    'isbn': '9780321356680',
                    'titulo': 'Effective Java',
                    'autor': 'Joshua Bloch',
                    'categoria': 'Programação'
                },
                {
                    'isbn': '9781449355739',
                    'titulo': 'Learning Python',
                    'autor': 'Mark Lutz',
                    'categoria': 'Programação'
                }
            ]
            
            return render_template('catalogo_online.html', livros=livros_populares)

@app.route('/buscar-livro', methods=['GET', 'POST'])
def buscar_livro():
    """
    Permite buscar livros na API por título
    """
    resultado = None
    termo_busca = ''
    
    if request.method == 'POST':
        termo_busca = request.form.get('termo_busca')
        
        if termo_busca:
            # URL da API Open Library para busca por título
            url = f'https://openlibrary.org/search.json?title={termo_busca}&limit=10'
            
            try:
                res = urllib.request.urlopen(url)
                data = res.read()
                search_results = json.loads(data)
                
                # Formatar resultados para exibição
                livros_encontrados = []
                for book in search_results.get('docs', []):
                    livro = {
                        'titulo': book.get('title', 'Título não disponível'),
                        'autor': book.get('author_name', ['Autor desconhecido'])[0] if book.get('author_name') else 'Autor desconhecido',
                        'ano': book.get('first_publish_year', 'Ano desconhecido'),
                        'isbn': book.get('isbn', [''])[0] if book.get('isbn') else '',
                        'editora': book.get('publisher', [''])[0] if book.get('publisher') else ''
                    }
                    livros_encontrados.append(livro)
                
                resultado = livros_encontrados[:8]  # Limita a 8 resultados
                
            except Exception as e:
                resultado = f'Erro na busca: {str(e)}'
    
    return render_template('buscar_livro.html', resultado=resultado, termo_busca=termo_busca)

# Bloco para executar a aplicação
if __name__ == '__main__':
    app.run(debug=True)