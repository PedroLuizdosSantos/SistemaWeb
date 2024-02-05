from flask import render_template, redirect, url_for, flash, request, send_file
from ProjetoVece import app, database, bcrypt
from ProjetoVece.formulario import FormLogin, FormCriarConta, FormSolicita, FormEditarPerfil,FormAprovado
from ProjetoVece.models import Usuario, Solicita, Upload, Aprovado
from flask_login import login_user, logout_user, current_user, login_required
import secrets
import os
from PIL import Image
from io import BytesIO




@app.route("/", methods=["GET","POST"])
def home():
    form_login = FormLogin()

    if form_login.validate_on_submit():
        usuario = Usuario.query.filter_by(username=form_login.username.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, form_login.senha.data) and usuario.setor == "Solicitante":
            login_user(usuario, remember=form_login.lembrar.data)
            flash("Login Bem Sucedido", 'alert-success')
            return redirect(url_for('Solicitante'))
        elif usuario and bcrypt.check_password_hash(usuario.senha, form_login.senha.data) and usuario.setor == "MKT":
            login_user(usuario, remember=form_login.lembrar.data)
            flash("Login Bem Sucedido", 'alert-success')
            return redirect(url_for('MKT'))
        elif usuario and bcrypt.check_password_hash(usuario.senha, form_login.senha.data) and usuario.setor == "OBRA":
            login_user(usuario, remember=form_login.lembrar.data)
            flash("Login Bem Sucedido", 'alert-success')
            return redirect(url_for('OBRA'))
        elif usuario and bcrypt.check_password_hash(usuario.senha, form_login.senha.data) and usuario.setor == "Pagamentos":
            login_user(usuario, remember=form_login.lembrar.data)
            flash("Login Bem Sucedido", 'alert-success')
            return redirect(url_for('PAGAMENTOS'))
        elif usuario and bcrypt.check_password_hash(usuario.senha, form_login.senha.data) and usuario.setor == "ADM":
            login_user(usuario, remember=form_login.lembrar.data)
            flash("Login Bem Sucedido", 'alert-success')
            return redirect(url_for('ADM'))
        elif usuario and bcrypt.check_password_hash(usuario.senha, form_login.senha.data) and usuario.setor == "Novos":
            login_user(usuario, remember=form_login.lembrar.data)
            flash("Login Bem Sucedido", 'alert-success')
            return redirect(url_for('ADM'))
        else:
            flash("Falha no Login, E-mail ou Senha Incorretos", 'alert-danger')

    return render_template("Home.html", form_login=form_login)


def salvar_anexo(anexo):
    codigo = secrets.token_hex(8)
    nome, extensao = os.path.splitext(anexo.filename)
    nome_arquivo = nome + codigo + extensao
    caminho_completo = os.path.join(app.root_path, 'static/Anexos', nome_arquivo)
    anexo_reduzida = Image.open(anexo)
    anexo_reduzida.save(caminho_completo)
    return nome_arquivo


@app.route("/solicita",methods=["GET","POST"])
@login_required
def solicita():
    form_solicita = FormSolicita()
    if form_solicita.validate_on_submit():
        solicita = Solicita(centrodecusto=form_solicita.centrodecusto.data, empreendimento=form_solicita.empreendimento.data, datavencimento=form_solicita.datavencimento.data, valorliquido=form_solicita.valorliquido.data, valorbruto=form_solicita.valorbruto.data, prazo=form_solicita.prazo.data, favorecido=form_solicita.favorecido.data, cnpj=form_solicita.cnpj.data, razaosocial=form_solicita.razaosocial.data, orcamento=form_solicita.orcamento.data, pendencia=form_solicita.pendencia.data, servico=form_solicita.servico.data, mei=form_solicita.mei.data, descricao=form_solicita.descricao.data, pagamento=form_solicita.pagamento.data, nf=form_solicita.nf.data, linhaplanejamento=form_solicita.linhaplanejamento.data, observacoes=form_solicita.observacoes.data, autor=current_user, aprovado='Nao')
        if form_solicita.anexo.data:
            nome_imagem = salvar_anexo(form_solicita.anexo.data)
            solicita.anexo = nome_imagem
        database.session.add(solicita)
        database.session.commit()
        files = request.files.getlist("file")
        for file in files:
            upload = Upload(filename=file.filename, data=file.read(), id_post=solicita.id)
            database.session.add(upload)
            database.session.commit()
        flash(' Solicitacão Enviada Com Sucesso', 'alert-success')

    return render_template("solicita.html", form_solicita=form_solicita)

@app.route("/host", methods=["GET","POST"])
def host():
    form_criarconta= FormCriarConta()

    if form_criarconta.validate_on_submit():
        senha_cript = bcrypt.generate_password_hash(form_criarconta.senha.data)
        usuario = Usuario(username=form_criarconta.username.data,senha=senha_cript,setor=form_criarconta.setor.data,email=form_criarconta.email.data)
        database.session.add(usuario)
        database.session.commit()

        flash("Cadastro Realizado com Sucesso", 'alert-success')
    return render_template("host.html", form_criarconta=form_criarconta)

@app.route('/MKT', methods=["GET","POST"])
@login_required
def MKT():
    posts = Solicita.query.order_by(Solicita.id.desc())
    arquivo = Upload.query.first()
    form_aprovado = FormAprovado()
    if form_aprovado.validate_on_submit():
        aprovado = Aprovado(aprovado="SIM")
        database.session.add(aprovado)
        database.session.commit()

        flash("Solicitação Aprovada", 'alert-success')

    return render_template("MKT.html", posts=posts, arquivo=arquivo,form_aprovado=form_aprovado)


@app.route("/ADM", methods=["GET", "POST"])
@login_required
def ADM():
    posts = Solicita.query.order_by(Solicita.id.desc())


    return render_template("ADM.html", posts=posts)

@app.route("/PAGAMENTOS")
@login_required
def PAGAMENTOS():

    return render_template("PAGAMENTOS.html")

@app.route("/OBRA")
@login_required
def OBRA():
    posts = Solicita.query.order_by(Solicita.id.desc())

    return render_template("OBRA.html", posts=posts)

@app.route("/sair")
@login_required
def sair():
    logout_user()
    flash("Logout feito com sucesso", 'alert-success')
    return redirect(url_for("home"))

@app.route("/Perfil")
@login_required
def Perfil():
    foto = url_for('static', filename='fotos_perfil/{}'.format(current_user.foto))
    return render_template("Perfil.html", foto_perfil=foto)


def salvar_imagem(imagem):
    codigo = secrets.token_hex(8)
    nome, extensao = os.path.splitext(imagem.filename)
    nome_arquivo = nome + codigo + extensao
    caminho_completo = os.path.join(app.root_path, 'static/fotos_perfil', nome_arquivo)
    tamanho = (200, 200)
    imagem_reduzida = Image.open(imagem)
    imagem_reduzida.thumbnail(tamanho)
    imagem_reduzida.save(caminho_completo)
    return nome_arquivo

def salvar_anexo(anexo):
    codigo = secrets.token_hex(8)
    nome, extensao = os.path.splitext(anexo.filename)
    nome_arquivo = nome + codigo + extensao
    caminho_completo = os.path.join(app.root_path, 'static/Anexos', nome_arquivo)
    anexo.save(caminho_completo)
    return nome_arquivo



@app.route("/editarperfil",methods=["GET","POST"])
@login_required
def editarperfil():
    foto = url_for('static', filename='fotos_perfil/default.jpg')
    form = FormEditarPerfil()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        if form.foto.data:
            nome_imagem = salvar_imagem(form.foto.data)
            current_user.foto = nome_imagem
        database.session.commit()
        flash("Alteração Feita com Sucesso", 'alert-success')
        return redirect(url_for('Perfil'))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email

    return render_template("editarperfil.html", foto=foto, form=form)

@app.route("/Solicitante")
@login_required
def Solicitante():
    posts = Solicita.query.order_by(Solicita.id.desc())
    return render_template("Solicitante.html", posts=posts)

@app.route("/novos")
@login_required
def Novos():
    posts = Solicita.query.order_by(Solicita.id.desc())
    return render_template("Novos.html", posts=posts)

@app.route('/download/<upload_id>')
def download(upload_id):
    upload = Upload.query.filter_by(id=upload_id).first()
    return send_file(BytesIO(upload.data), download_name=upload.filename, as_attachment=True)


@app.route('/gestor', methods=["GET","POST"])
def gestor():
    posts = Solicita.query.order_by(Solicita.id.desc())
    aprovado = Aprovado.query.posts


    return render_template("gestor.html", posts=posts, aprovado=aprovado)















