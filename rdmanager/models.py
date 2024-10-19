from datetime import datetime
from rdmanager import db, loginMgr, bcrypt
from flask_login import UserMixin

@loginMgr.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(60), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False , default=datetime.now)
    @property
    def password(self):
        return ''
    @password.setter
    def password(self,password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
    def __repr__(self):
        return f"{self.name} {self.lastname}({self.email})"

class UserLogins(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), )
    login_date = db.Column(db.DateTime, nullable=False, default=datetime.now)
    login_ip = db.Column(db.String(45))
    
    def _repr__(self):
        return f"UserLogins({self.id}, {self.user_id}, {self.login_date}, {self.login_ip})"

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True)
    phone = db.Column(db.String(11))
    address = db.Column(db.String(100))
    number = db.Column(db.Integer)
    complement = db.Column(db.String(25))
    city = db.Column(db.String(100))
    state = db.Column(db.String(2))
    postal_code = db.Column(db.String(10))
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.now)
    terminais = db.relationship('Terminal', back_populates='Customer', lazy=True)

    def __repr__(self):
        return f"{self.nome}({self.razao_social})"
   
class Terminal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    description = db.Column(db.String(50),)
    rustdesk_id = db.Column(db.String(12),unique=True, nullable=False)
    rustdesk_password = db.Column(db.String(12), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.now)
    customer = db.relationship('Customer',back_populates='terminals')

    def __repr__(self):
        return f"{self.description}-{self.rustdesk_id}/{self.rustdesk_password}"