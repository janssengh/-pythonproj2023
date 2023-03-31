from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'chave_secreta'

#usando o prompt do mysql command line, vamos criar uma base de dados
#create database bancodados

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:softgraf@localhost:3306/bancodados'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['RECAPTCHA_PRIVATE_KEY'] = '6Lc2_0YlAAAAAB5JMKSTh9e843n2NI1YgUZzjAFP'
app.config['RECAPTCHA_PUBLIC_KEY'] = '6Lc2_0YlAAAAABAiIufL9fiAcQptQIF3LnddKwJo'
app.config['RECAPTCHA_USE_SSL'] = False
app.config['RECAPTCHA_OPTIONS'] = {'theme': 'white'}

db = SQLAlchemy(app)
lista = []


