from config import db
from werkzeug.security import generate_password_hash, check_password_hash

class Login(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(60), nullable=False, unique=True)
    senha = db.Column(db.String(200), nullable=False)

    def __init__(self, nome, idade, email, senha):
        self.nome = nome
        self.idade = idade
        self.email = email
        self.senha = generate_password_hash(senha, method='sha256')

    def verificarSenha(self, senha): #senha sem criptografia
        return check_password_hash(self.senha, senha)
