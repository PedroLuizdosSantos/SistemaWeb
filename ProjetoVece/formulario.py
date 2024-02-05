from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from ProjetoVece.models import Usuario
from flask_login import current_user



class FormCriarConta(FlaskForm):
    username = StringField("Nome de Usuário:",validators= [DataRequired()])
    senha = PasswordField("Senha:", validators=[DataRequired(),Length(6)])
    confirmasenha = PasswordField("Confirme a senha", validators=[DataRequired(),EqualTo("senha")])
    email = StringField("e-mail:", validators=[Email()])
    btcadastrar = SubmitField("Cadastrar")
    setor = SelectField("Setor:", choices=[('MKT', 'MARKETING'), ('OBRA', 'OBRAS'), ('ADM', 'ADM/FINANÇAS'),('Pagamentos','PAGAMENTOS'),('Solicitante','SOLICITANTE'), ('Novos','NOVOS NEGÓCIOS'),('gestor','GESTOR')],validators=[DataRequired()])

    def validate_username(self, username):
        usuario = Usuario.query.filter_by(username=username.data).first()
        if usuario:
            raise ValidationError("Nome de Usuario já cadastrado")

    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario:
            raise ValidationError("E-mail Já Cadastrado")






class FormLogin(FlaskForm):
    username = StringField("Nome de Usuário:",validators=[DataRequired()])
    senha = PasswordField("Senha:",validators=[DataRequired(), Length(6)])
    btlogin = SubmitField("Entrar")
    lembrar = BooleanField("Lembrar Login:")

class FormSolicita(FlaskForm):
    centrodecusto = SelectField("Setor:", choices=[('MKT', 'MARKETING'), ('OBRA', 'OBRAS'), ('ADM', 'ADM/FINANÇEIRO'), ('Novos', 'NOVOS NEGÓCIOS')],validators=[DataRequired()])
    empreendimento = StringField("Empreendimento:", validators=[DataRequired()])
    datavencimento = StringField("Data de Vencimento:", validators=[DataRequired()])
    valorbruto = StringField("Valor Bruto:")
    valorliquido = StringField("Valor Liquido:", validators=[DataRequired()])
    favorecido = StringField("Favorecido:", validators=[DataRequired()])
    cnpj = StringField("CNPJ:", validators=[DataRequired()])
    razaosocial = StringField("Razão Social:", validators=[DataRequired()])
    orcamento = StringField("Está no Orçamento?:")
    pendencia = StringField("Tem pendencia? qual:")
    prazo = StringField("Prazo para saldar pendencia:")
    servico = StringField("O serviço/material, já foi entregue/prestado?")
    mei = StringField("O fornecedor é MEI?")
    descricao = StringField("Descrição do que foi Contratado :", validators=[DataRequired()])
    pagamento = StringField("Forma de Pagamento:", validators=[DataRequired()])
    nf = StringField("Número NF:")
    linhaplanejamento = StringField("Linha do Planejamento", validators=[DataRequired()])
    anexo = FileField("Adicionar Anexo", validators=[FileAllowed(['jpg', 'png', 'jpeg','pdf','zip'])])
    observacoes = TextAreaField("Observações:")
    btenviar = SubmitField("Enviar Solicitação")



class FormEditarPerfil(FlaskForm):
    username = StringField("Nome de Usuário:", validators=[DataRequired()])
    email = StringField("e-mail:", validators=[Email()])
    foto = FileField("Atualizar foto de perfil", validators=[FileAllowed(['jpg', 'png'])])
    btenviarr = SubmitField("Confirmar edição")



    def validate_username(self, username):
        if current_user.username != username.data:
            usuario = Usuario.query.filter_by(username=username.data).first()
            if usuario:
                raise ValidationError("Nome de Usuario já cadastrado")
            
    def validate_email(self, email):
        if current_user.email != email.data:
            usuario = Usuario.query.filter_by(email=email.data).first()
            if usuario:
                raise ValidationError("E-mail já cadastrado")



class FormAprovado(FlaskForm):
    aprovado = StringField("Aprovado")
    btaprovado = SubmitField("Aprovar")











