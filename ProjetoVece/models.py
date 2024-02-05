from ProjetoVece import database, login_manager
from flask_login import UserMixin
from datetime import datetime

@login_manager.user_loader
def load_usuario(id_usuario):
    return Usuario.query.get(int(id_usuario))



class Usuario(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String, nullable=False, unique=True)
    senha = database.Column(database.String, nullable=False)
    setor = database.Column(database.String, nullable=False)
    foto = database.Column(database.String, default='salvararquivo.png')
    email = database.Column(database.String,unique=True,)
    pedidos = database.relationship('Solicita', backref='autor', lazy=True)

class Solicita(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    centrodecusto = database.Column(database.String, nullable=False)
    empreendimento = database.Column(database.String, nullable=False)
    datavencimento = database.Column(database.String, nullable=False)
    valorliquido = database.Column(database.String, nullable=False)
    favorecido = database.Column(database.String, nullable=False)
    cnpj = database.Column(database.String, nullable=False)
    razaosocial = database.Column(database.String, nullable=False)
    orcamento = database.Column(database.String, nullable=False)
    pendencia = database.Column(database.String, nullable=False)
    servico = database.Column(database.String, nullable=False)
    mei = database.Column(database.String, nullable=False)
    descricao = database.Column(database.String, nullable=False)
    pagamento = database.Column(database.String, nullable=False)
    nf = database.Column(database.String, nullable=False)
    linhaplanejamento = database.Column(database.String, nullable=False)
    anexo = database.Column(database.String, default='default.jpg')
    observacoes = database.Column(database.Text, nullable=False)
    datacriacao = database.Column(database.DateTime, nullable=False, default=datetime.utcnow)
    prazo = database.Column(database.String, nullable=False)
    valorbruto = database.Column(database.String, nullable=False)
    id_usuario = database.Column(database.Integer, database.ForeignKey('usuario.id'), nullable=False )
    aprovado = database.Column(database.String)
    post = database.relationship('Upload', backref='arquivo', lazy=True)

class Upload(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    filename = database.Column(database.String(50))
    data = database.Column(database.LargeBinary)
    id_post = database.Column(database.Integer, database.ForeignKey('solicita.id'), nullable=False )


class Aprovado(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    aprovado = database.Column(database.String, nullable=False)








