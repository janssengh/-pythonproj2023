#pip install wtforms
#pip install flask_wtf
#pip install wtforms[email]

from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, IntegerField, EmailField, PasswordField, SubmitField, validators
from wtforms.validators import NumberRange, DataRequired, Length, EqualTo, Email


#FormCadastro é um FlaskForm
class FormCadastro(FlaskForm):

    nome = StringField('Nome', validators=[validators.Length(min=6, max=60),
                                           validators.DataRequired('Faltou digitar o nome')])

    idade = IntegerField('Idade', validators=[NumberRange(min=18, max=65),
                                              DataRequired('Faltou a idade')])

    email = EmailField('E-mail', validators=[Length(min=6, max=60),
                                             Email(message='Entre com um e-mail válido'),
                                             DataRequired()])

    senha = PasswordField('Senha', validators=[DataRequired(),
                                               Length(min=6, message='Selecione uma senha forte')])

    confirmacao = PasswordField('Confirme sua senha', validators=[DataRequired(),
                                                      EqualTo('senha',
                                                      message='Senhas devem corresponder')])

    recaptcha = RecaptchaField()


    submit = SubmitField('Enviar')