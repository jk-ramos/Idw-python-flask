from flask import render_template, request, redirect, url_for
from models.database import db, Leitor, Livro, Emprestimo
from datetime import datetime

def init_app(app):
    
    @app.route('/')
    def home():
        # Estatísticas para a home
        total_livros = Livro.query.count()
        total_leitores = Leitor.query.count()
        total_emprestimos = Emprestimo.query.filter_by(status='Emprestado').count()
        
        return render_template('index.html', 
                             total_livros=total_livros,
                             total_leitores=total_leitores,
                             total_emprestimos=total_emprestimos)

    # ==================== CRUD DE LEITORES ====================
    
    @app.route('/leitores', methods=['GET', 'POST'])
    @app.route('/leitores/delete/<int:id>')
    def gerenciar_leitores(id=None):
        # EXCLUSÃO
        if id:
            leitor = Leitor.query.get(id)
            if leitor:
                db.session.delete(leitor)
                db.session.commit()
            return redirect(url_for('gerenciar_leitores'))
        
        # CADASTRO
        if request.method == 'POST':
            novo_leitor = Leitor(
                request.form['nome'],
                request.form['email'],
                request.form['telefone'],
                datetime.now().strftime('%d/%m/%Y')
            )
            db.session.add(novo_leitor)
            db.session.commit()
            return redirect(url_for('gerenciar_leitores'))
        
        # LISTAGEM COM PAGINAÇÃO
        page = request.args.get('page', 1, type=int)
        per_page = 5
        leitores_page = Leitor.query.paginate(page=page, per_page=per_page, error_out=False)
        
        return render_template('leitores.html', leitores=leitores_page)
    
    
    @app.route('/leitor/edit/<int:id>', methods=['GET', 'POST'])
    def editar_leitor(id):
        leitor = Leitor.query.get(id)
        
        # EDIÇÃO
        if request.method == 'POST':
            leitor.nome = request.form['nome']
            leitor.email = request.form['email']
            leitor.telefone = request.form['telefone']
            db.session.commit()
            return redirect(url_for('gerenciar_leitores'))
        
        return render_template('editar_leitor.html', leitor=leitor)


    # ==================== CRUD DE LIVROS ====================
    
    @app.route('/livros', methods=['GET', 'POST'])
    @app.route('/livros/delete/<int:id>')
    def gerenciar_livros(id=None):
        # EXCLUSÃO
        if id:
            livro = Livro.query.get(id)
            if livro:
                db.session.delete(livro)
                db.session.commit()
            return redirect(url_for('gerenciar_livros'))
        
        # CADASTRO
        if request.method == 'POST':
            novo_livro = Livro(
                request.form['titulo'],
                request.form['autor'],
                request.form['ano'],
                request.form['categoria'],
                request.form.get('isbn', ''),
                int(request.form['quantidade'])
            )
            db.session.add(novo_livro)
            db.session.commit()
            return redirect(url_for('gerenciar_livros'))
        
        # LISTAGEM COM PAGINAÇÃO
        page = request.args.get('page', 1, type=int)
        per_page = 6
        livros_page = Livro.query.paginate(page=page, per_page=per_page, error_out=False)
        
        return render_template('livros.html', livros=livros_page)
    
    
    @app.route('/livro/edit/<int:id>', methods=['GET', 'POST'])
    def editar_livro(id):
        livro = Livro.query.get(id)
        
        # EDIÇÃO
        if request.method == 'POST':
            livro.titulo = request.form['titulo']
            livro.autor = request.form['autor']
            livro.ano = request.form['ano']
            livro.categoria = request.form['categoria']
            livro.isbn = request.form.get('isbn', '')
            livro.quantidade = int(request.form['quantidade'])
            livro.disponivel = 'Sim' if livro.quantidade > 0 else 'Não'
            db.session.commit()
            return redirect(url_for('gerenciar_livros'))
        
        return render_template('editar_livro.html', livro=livro)


    # ==================== CRUD DE EMPRÉSTIMOS ====================
    
    @app.route('/emprestimos', methods=['GET', 'POST'])
    @app.route('/emprestimos/delete/<int:id>')
    def gerenciar_emprestimos(id=None):
        # EXCLUSÃO
        if id:
            emprestimo = Emprestimo.query.get(id)
            if emprestimo:
                # Atualiza disponibilidade do livro
                livro = Livro.query.get(emprestimo.livro_id)
                livro.quantidade += 1
                livro.disponivel = 'Sim' if livro.quantidade > 0 else 'Não'
                
                db.session.delete(emprestimo)
                db.session.commit()
            return redirect(url_for('gerenciar_emprestimos'))
        
        # CADASTRO
        if request.method == 'POST':
            livro_id = int(request.form['livro_id'])
            livro = Livro.query.get(livro_id)
            
            # Verifica disponibilidade
            if livro and livro.quantidade > 0:
                novo_emprestimo = Emprestimo(
                    int(request.form['leitor_id']),
                    livro_id,
                    datetime.now().strftime('%d/%m/%Y'),
                    request.form['data_devolucao']
                )
                
                # Atualiza quantidade do livro
                livro.quantidade -= 1
                livro.disponivel = 'Sim' if livro.quantidade > 0 else 'Não'
                
                db.session.add(novo_emprestimo)
                db.session.commit()
            
            return redirect(url_for('gerenciar_emprestimos'))
        
        # LISTAGEM COM PAGINAÇÃO
        page = request.args.get('page', 1, type=int)
        per_page = 8
        emprestimos_page = Emprestimo.query.paginate(page=page, per_page=per_page, error_out=False)
        
        # Lista de leitores e livros para o formulário
        leitores = Leitor.query.all()
        livros = Livro.query.filter(Livro.quantidade > 0).all()
        
        return render_template('emprestimos.html', 
                             emprestimos=emprestimos_page,
                             leitores=leitores,
                             livros=livros)
    
    
    @app.route('/emprestimo/devolver/<int:id>')
    def devolver_emprestimo(id):
        emprestimo = Emprestimo.query.get(id)
        
        if emprestimo:
            emprestimo.status = 'Devolvido'
            
            # Atualiza quantidade do livro
            livro = Livro.query.get(emprestimo.livro_id)
            livro.quantidade += 1
            livro.disponivel = 'Sim'
            
            db.session.commit()
        
        return redirect(url_for('gerenciar_emprestimos'))