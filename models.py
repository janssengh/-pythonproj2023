from sqlalchemy import func
from config import db

#ORM -> Converte uma classe em uma tabela relacional, sem necessidade do uso de SQL
#representa uma entidade do banco de dados
class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(100), nullable=False)
    preco = db.Column(db.Float, nullable=False)
    quantidade = db.Column(db.Integer)
    cadastrado = db.Column(db.DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f'<Produto: {self.id} desc: {self.descricao} preço: {self.preco}' \
        f' quant: {self.quantidade} data: {self.cadastrado}>'



