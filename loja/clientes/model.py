from loja import db, app, login_manager
from datetime import datetime
from flask_login import UserMixin
import json

class JsonEcodeDirect(db.TypeDecorator):
    impl = db.Text

    def process_bind_param(self, value, dialect):
        if value is None:
            # retorna o dicionário
            return '{}'
        else:
            return json.dumps(value)

    def process_result_value(self, value, dialect):
        if value is None:
           # retorna vazio
           return {}
        else:
           return json.loads(value)

@login_manager.user_loader
def user_carregar(user_id):
    print(user_id)
    return Client.query.get(user_id)

class Client(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50), unique = False)
    username = db.Column(db.String(50), unique = False)
    email = db.Column(db.String(50), unique = False)
    password = db.Column(db.String(50), unique = False)
    country = db.Column(db.String(50), unique = False)
    city = db.Column(db.String(50), unique = False)
    contact = db.Column(db.String(50), unique = False)
    address = db.Column(db.String(50), unique = False)
    zipcode = db.Column(db.String(50), unique = False)
    profile = db.Column(db.String(50), unique = False, default='profile.jpg')
    created_date = db.Column(db.DateTime, nullable = False, default=datetime.utcnow())

    def __repr__(self):
        return '<Cadastrar %r>' % self.name

class ClientOrder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    invoice = db.Column(db.String(20), unique=False, nullable=False)
    status = db.Column(db.String(20), default='pendente', nullable=False)
    client_id = db.Column(db.Integer, unique=False, nullable=False)
    created_date = db.Column(db.DateTime(50), default=datetime.utcnow, nullable=False)
    # De: pedido = db.Column(db.Text) para:
    order = db.Column(JsonEcodeDirect)

    def __repr__(self):
        return '<ClientOrder %r>' % self.invoice


with app.app_context():
    db.create_all()
