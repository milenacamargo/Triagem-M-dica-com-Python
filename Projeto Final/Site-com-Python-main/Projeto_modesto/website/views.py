from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from .models import Paciente, Atendimento
from . import db
from sqlalchemy import desc

views = Blueprint('views', __name__)
#colocando urls nas nossas pages

@views.route('/')
@login_required
def home():
    pacientes = (
        db.session.query(Paciente, Atendimento)
        .join(Atendimento, Paciente.id == Atendimento.paciente_id)
        .order_by(desc(Atendimento.urgencia))
        .all()
    )
    
    return render_template("home.html", user=current_user, pacientes=pacientes)

@views.route('/marcar_atendido/<int:atendimento_id>', methods=['GET', 'POST'])
@login_required
def marcar_atendido(atendimento_id):
    atendimento = Atendimento.query.get(atendimento_id)
    if atendimento:
       atendimento.atendido = True
       db.session.commit()
    return redirect(url_for('views.home'))