# Autor: Bruno Ribeiro dos Santos
# data de criação: 26/11/2022
# CURSO DE INTRODUÇÃO A PROGRAMAÇÃO COM PYTHON + WEB

# ------------------------------------------------------------------- Código da aplicação ---------------------------------------------------------------------------------------------------------#

import sqlite3
from flask import Flask, render_template, redirect, url_for, request, flash, session, g, abort
from contextlib import closing

# Configurações iniciais
USERNAME = 'test'
PASSWORD = 'pass'
DATABASE = 'DB_Cadastro.db'
SECRET_KEY = 'BrUnSnEcO kEy'


# Aplicação:
app = Flask(__name__)
app.config.from_object(__name__)

# conexão com nosso banco de dados
def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

# Iniciar banco de dados
def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql') as f:
            db.cursor().executescript(f.read())
        db.commit()

def get_post(post_id):
    conn = connect_db()
    post = conn.execute('select * FROM Cadastro where id = ?',(post_id,)).fetchone()
    if post is None:
        abort(404)
    return post

def get_user(post_user):
    conn = connect_db()
    user = conn.execute('select * FROM Cadastro where user = ?',(post_user,)).fetchone()
    if user is None:
        abort(404)
    return user 

# conectar o db antes da requisição
@app.before_request
def before_request():
    g.db = connect_db()

# Desconectar db após requisição
@app.teardown_request
def teardown_request(exception):
    g.db.close()
  
#  Página principal
@app.route('/home')
def home():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    else:
        return render_template('home.html')

# login de acesso a página:
@app.route("/", methods=['GET','POST'])
def login():
    error = None    

    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Usuário incorreto'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Senha incorreta!'
        else:
    
            session['logged_in'] = True
            flash('Login realizado!')
            return redirect(url_for('home'))
    return render_template("login.html", error=error)

# logout da página
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('Você esstá desconectado!')
    return redirect(url_for('login'))

# Cadastro de usuários
@app.route("/cadastro", methods=['GET','POST'])
def add_entry():
    falha = None
    if request.method == 'POST':
        if request.form['pass'] == request.form['passConfirm']:
            g.db.execute('insert into Cadastro (Nome, Email, Nascimento, Cidade, User, Senha, SenhaConfirm) values (?,?,?,?,?,?,?)', [request.form['nome'], request.form['email'], 
            request.form['nascimento'], request.form['cidade'],request.form['user'],request.form['pass'], request.form['passConfirm']])
            g.db.commit()
            flash('Cadatro realizado!')
            if not session.get('logged_in'):
                return redirect(url_for('login'))
            else:
                return redirect(url_for('home'))
        else:
            falha = 'Senhas não são iguais!'
    return render_template('cadastro.html', falha=falha)

# acesso aos Logins Cadastrados
@app.route('/database')
def show_entries():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    cur = g.db.execute('select id, Nome, Email, User from Cadastro order by id ')
    entries = [dict(id=row[0],nome=row[1], email=row[2], user=row[3]) for row in cur.fetchall()]
    return render_template('show_entries.html', entries=entries)

# acesso a um cadastro específico
@app.route('/<int:id>/edit', methods=('GET', 'POST'))
def edit(id):
    entries = get_post(id)
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        user = request.form['user']

        if not nome:
            flash('Nome é obrigatório!')
        elif not email:
            flash('E-mail é obrigatório!')
        elif not user:
            flash('Usuário é obrigatório')
        else:
            g.db.execute('UPDATE Cadastro SET Nome = ?, Email = ?, User = ?''WHERE id = ?', (nome, email, user,id))
            g.db.commit()
            return redirect(url_for('home'))
        
    return render_template('edit.html', cadastro=entries)

# excluir um cadastro
@app.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    g.db.execute('delete from cadastro where id =?', (id,))
    g.db.commit()
    print('Excluido!')
    return redirect(url_for('home'))

#  configuração da aplicação
if __name__ == "__main__":
    app.run(debug=True, port=80)