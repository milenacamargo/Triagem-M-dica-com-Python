from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from datetime import datetime

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150),unique=True)
    senha = db.Column(db.String(150))
    nome = db.Column(db.String(150))
    
class Paciente(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    cpf = db.Column(db.String(10000))
    nome = db.Column(db.String(10000))
    idade = db.Column(db.Integer)

    atendimentos = db.relationship('Atendimento', backref='paciente', lazy=True)
    
class Atendimento(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    data_atendimento = db.Column(db.Date, nullable=False, default=datetime.now)
    temperatura = db.Column(db.Integer)
    pressao  = db.Column(db.Integer)
    dores = db.Column(db.Integer)
    perda_consciencia = db.Column(db.Integer)
    dificuldade_respiratoria = db.Column(db.Integer)       
    urgencia = db.Column(db.Integer)
    atendido = db.Column(db.Boolean)

    paciente_id = db.Column(db.Integer, db.ForeignKey('paciente.id'))
    