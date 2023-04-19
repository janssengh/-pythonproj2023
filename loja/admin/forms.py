from flask_wtf import RecaptchaField
from wtforms import Form, BooleanField, StringField, validators, PasswordField
from wtforms.validators import Email, DataRequired, Length, EqualTo


class RegistrationForm(Form):
    name = StringField('Nome Completo :', [validators.Length(min=6, max=40),
                                           validators.DataRequired('Faltou digitar o nome')])
    user = StringField('Username', [validators.Length(min=6, max=10),
                                    validators.DataRequired('Faltou digitar o usuário')])
    email = StringField('E-mail', [validators.Length(min=6, max=60),
                                   Email(message='Entre com um e-mail válido'),
                                   DataRequired()])
    password = PasswordField('Informe a sua Senha', [
        validators.DataRequired(),
        Length(min=6, message='Selecione uma senha forte')])
    confirm = PasswordField('Confirme sua senha', validators=[DataRequired(),
                                                      EqualTo('password',
                                                      message='Senhas devem corresponder')])
    recaptcha = RecaptchaField()

class LoginFormulario(Form):
    email = StringField('E-mail', [validators.Length(min=6, max=60)])
    password = PasswordField('Informe a sua Senha', [validators.DataRequired()])

