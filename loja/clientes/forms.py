from flask_wtf.file import FileAllowed
from wtforms import StringField, validators, PasswordField, FileField, SubmitField, ValidationError
from flask_wtf import FlaskForm
from wtforms.validators import Length, Email, DataRequired

from .model import Client

class CadastroClienteForm(FlaskForm):
    name = StringField('Nome: ')
    username = StringField('Usuário: ', [validators.DataRequired()])
    email = StringField('E-mail: ', validators=[Length(min=6, max=60),
                                             Email(message='Entre com um e-mail válido'),
                                             DataRequired()])
    password = PasswordField('Senha: ', [validators.DataRequired(),
                                         validators.equal_to('confirm',message='As suas senhas devem ser iguais!')])
    confirm = PasswordField('Redigite Senha: ', [validators.DataRequired()])
    country = StringField('País: ', [validators.DataRequired()])
    city = StringField('Cidade: ', [validators.DataRequired()])
    contact = StringField('Contato: ', [validators.DataRequired()])
    address = StringField('Endereço: ', [validators.DataRequired()])
    zipcode = StringField('Caixa-Postal: ', [validators.DataRequired()])
    profile = FileField('Perfil ', validators=[FileAllowed(['jpg', 'png', 'gif', 'jpeg'])])

    submit = SubmitField('Cadastrar')

    def validate_username(self, username):
        if Client.query.filter_by(username=username.data).first():
            raise ValidationError("Este usuário já existe no Banco de Dados!")

    def validate_email(self, email):
        if Client.query.filter_by(email=email.data).first():
            raise ValidationError("Este e-mail já existe no Banco de Dados!")

class ClienteLoginForm(FlaskForm):
    email = StringField('E-mail: ', [validators.DataRequired()])
    password = PasswordField('Senha: ', [validators.DataRequired()])
