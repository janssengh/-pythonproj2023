#Projeto baseado em ORM (object Relational-Mapping = Mapeamento Objeto-Relacional)
#FLASK-SQLALCHEMY
#Converte objetos em tabelas relcionais (SQL)

#site oficial:
#https://flask-sqlalchemy.palletsprojects.com

#No terminal do pycharm
#pip install Flask Flask-SQLAlchemy

#Caso ocorra err0 de segurança, mudar a política de seg.do powrshell
#a. Executar powershell como administrador
#b. PS C:\Windows\sytem32> Get-ExecutionPolicy
#  Restricted
#
#c. PS C:\Windows\sytem32> Set-ExecutionPolicy RemoteSigned
#d. PS C:\Windows\sytem32> Get-ExecutionPolicy
#  RemoteSigned

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

#Configurandp acesso ao banco de dados MySQL:
#mysql://username:password@host:port/database_name
#msql: //root:@softgraf@localhost:3306/nome_banco

#Configurandp acesso ao banco de dados PostgreSQL:
#postgresql: //username:password@host:port/database_name

#Configurando para sqllite
#D:\Curso Python Valdeci\projeto_alchemy
basedir = os.path.abspath(os.path.dirname(__file__))

#'sqlite:///D:\Curso Python Valdeci\projeto_alchemy\database.db'
uri = 'sqlite:///' + os.path.join(basedir, 'database.db')

#cria a aplicacao Flask
app = Flask(__name__)
#configure o SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#cria um objeto para acesso ao banco de dados
db = SQLAlchemy(app)


