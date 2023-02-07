from flask import render_template, request, redirect, session, flash, url_for, send_from_directory
from biblioteca import app, db
from models import Usuarios, Fotos
import os
import time

@app.route('/')
def index():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for("login", proxima=url_for("index")))

    user = session["usuario_logado"]
    print(type(user))
    lista = Fotos.query.filter_by(autor=user)
    return render_template('lista.html', titulo='Fotos', fotos=lista)

@app.route('/cadastro')
def cadastro():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('cadastro')))
    return render_template('cadastro.html', titulo='Novo Foto')

@app.route("/accounts", methods=["GET", "POST"])
def accounts_create():
    if request.method == "POST":
        nome = request.form["nome"]
        username = request.form["usuario"]
        senha = request.form["senha"]

        user = Usuarios.query.filter_by(username=username).first()

        if user:
            flash("Usuário já existente!")
            return redirect(url_for("accounts_create"))

        user = Usuarios(nome=nome, username=username, senha=senha)

        db.session.add(user)
        db.session.commit()

        return redirect(url_for("login"))


    return render_template("form-user.html")

@app.route('/criar', methods=['POST',])
def criar():
    nome = request.form['nome']
    ano = request.form['ano']
    autor = session['usuario_logado']

    foto = Fotos\
        .query.filter_by(nome=nome).first()

    if foto:
        flash('Foto já existente!')
        return redirect(url_for('index'))




    flash('Foto criado com sucesso!')
    nova_foto = Fotos(nome=nome, autor=autor, ano=ano)
    db.session.add(nova_foto)
    db.session.commit()

    img = request.files['imagem']
    upload_path = app.config['UPLOAD_PATH']
    timestamp = time.time()

    foto = Fotos.query.filter_by(nome=nome).first()

    img.save(f'{upload_path}/foto{foto.id}.jpg')

    nova_foto.url = f'{upload_path}/foto{foto.id}.jpg'


    return redirect(url_for('index'))

@app.route('/editar/<int:id>')
def editar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('editar')))
    foto = Fotos.query.filter_by(id=id).first()
    return render_template('editar.html', titulo='Editar Foto', foto=foto)

@app.route('/atualizar', methods=['POST',])
def atualizar():
    foto = Fotos.query.filter_by(id=request.form['id']).first()
    foto.nome = request.form['nome']
    foto.ano = request.form['ano']

    db.session.add(foto)
    db.session.commit()

    capa = request.files['imagem']
    upload_path = app.config['UPLOAD_PATH']
    timestamp = time.time()
    deleta_arquivo(foto.id)
    capa.save(f'{upload_path}/foto{foto.id}.jpg')

    flash('Foto atualizada com sucesso!')
    return redirect(url_for('index'))

@app.route('/deletar/<int:id>')
def deletar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login'))

    Fotos.query.filter_by(id=id).delete()
    db.session.commit()
    flash('Livro deletado com sucesso!')

    return redirect(url_for('index'))

@app.route('/visualizar/<int:id>')
def visualizar(id):
    foto = Fotos.query.filter_by(id=id).first()
    imagem = recupera_imagem(id)
    return render_template('foto.html', foto=foto, imagem=imagem)

@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima=proxima, titulo='Login')

@app.route('/autenticar', methods=['POST',])
def autenticar():
    usuario = Usuarios.query.filter_by(username=request.form['usuario']).first()
    if usuario:
        if request.form['senha'] == usuario.senha:
            session['usuario_logado'] = usuario.username
            flash(usuario.username + ' logado com sucesso!')
            proxima_pagina = request.form['proxima']
            return redirect(proxima_pagina)
        else:
            flash('Usuário não logado com sucesso!')
            return redirect(url_for('login'))
    else:
        flash('Usuário não logado com sucesso!')
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Logout efetuado com sucesso!')
    return redirect(url_for('index'))

@app.route('/uploads/<nome_arquivo>')
def imagem(nome_arquivo):
    return send_from_directory('uploads', nome_arquivo)

def recupera_imagem(id):
    for nome_arquivo in os.listdir(app.config['UPLOAD_PATH']):
        if f'capa{id}' in nome_arquivo:
            return nome_arquivo

    return 'livro.png'

def deleta_arquivo(id):
    arquivo = recupera_imagem(id)
    print(arquivo)
    if arquivo != 'livro.png':
        os.remove(os.path.join(app.config['UPLOAD_PATH'], arquivo))