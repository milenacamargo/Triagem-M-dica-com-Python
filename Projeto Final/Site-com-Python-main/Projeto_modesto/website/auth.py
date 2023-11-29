from flask import Blueprint, render_template, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from website.models import User
from .models import Paciente
from .models import Atendimento
from . import db
from flask_login import login_user, login_required,logout_user, current_user


auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET','POST'])#permitir que o sistema receba as informações
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.senha, senha):
                flash('Logado com sucesso!', category='sucedida')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Senha incorreta, tente novamente!', category='erro')
        else:
            flash('Email inexistente.', category='erro')
                                     

    return render_template("login.html", user= current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET','POST'])#permitir que o sistema receba as informações
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        nome = request.form.get('nome')
        sobrenome = request.form.get('sobrenome')
        crm = request.form.get('crm')
        data = request.form.get('data')
        senha = request.form.get('senha')
        senha2 = request.form.get('senha2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Este email já existe.', category = 'erro')
        elif len(email)< 11:
            flash('O email deve ser maior que 10 caracteres', category='erro')
        elif len(nome)< 3:
            flash('O nome deve ser maior que 2 caracteres', category='erro')
        elif len(sobrenome)< 2:
            flash('O sobrenome deve ser maior que 1 caracter', category='erro')
        elif senha != senha2:
            flash('As senhas não são iguais', category='erro')
        elif len(senha)< 7:
            flash('A senha deve ser maior que 6 caracteres', category='erro')
        else:
            #adicionar o usuário no banco de dados
            new_user = User(email=email, nome=nome, senha=generate_password_hash(senha, method='pbkdf2:sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Conta criada com sucesso!', category='sucedida')
            return redirect(url_for('views.home'))
        
    return render_template("sign_up.html", user = current_user)

@auth.route('/paciente', methods=['GET','POST'])#permitir que o sistema receba as informações
@login_required
def paciente():
    if request.method == 'POST':
        nome = request.form.get('nome')
        CPF = request.form.get('CPF')
        temcpf = Paciente.query.filter_by(cpf=CPF).first()
        if temcpf:
            flash('CPF já cadastrado.', category='erro')
        else:
            idade = request.form.get('idade')
            
            novo_paciente = Paciente(cpf=CPF, nome=nome, idade=idade)
            db.session.add(novo_paciente)
            db.session.commit()

            flash("Cadastro de paciente criado com sucesso!", category = 'sucedida')
        
      

    return render_template("paciente.html", user=current_user)

@auth.route('/atendimento', methods=['GET', 'POST'])
@login_required
def atendimento():

    paciente = None 
    if request.method == 'POST':
        cpf = request.form.get('CPF')

        paciente = Paciente.query.filter_by(cpf=cpf).first()

        if paciente:
            temperatura = float(request.form.get('temperatura'))
            pressao = float(request.form.get('pressao'))
            dores = request.form.get('dores')
            perda_consciencia = request.form.get('perda_consciencia')
            dificuldade_respiratoria = request.form.get('dificuldade_respiratoria')

            urgencia = 0

            if temperatura > 38.0 or temperatura < 35.0:
                urgencia += 1

            if pressao > 140 or pressao < 90:
                urgencia += 1

            if perda_consciencia == '2':
                urgencia += 2

            elif perda_consciencia == '1':
                urgencia += 1

            if dificuldade_respiratoria == '2':
                urgencia += 2
            
            elif dificuldade_respiratoria == '1':
                urgencia += 1

            if dores == '1':
                urgencia += 2

            elif dores == '2':
                urgencia += 1

            novo_atendimento = Atendimento(temperatura=temperatura,  pressao =pressao, dores=dores, perda_consciencia=perda_consciencia, dificuldade_respiratoria=dificuldade_respiratoria,urgencia=urgencia, paciente_id=paciente.id)
            db.session.add(novo_atendimento)
            db.session.commit()

            flash("Adicionado!", category = 'sucedida')
            return render_template("atendimento.html", user=current_user, paciente=paciente)
        else:
            flash("Paciente não encontrado. Por favor, cadastre o paciente", category = 'erro')
    
    return render_template('atendimento.html', user=current_user, paciente=paciente)

@auth.route('/detalhes_paciente/<int:paciente_id>')
@login_required
def detalhes_paciente(paciente_id):
    paciente = Paciente.query.get(paciente_id)
    atendimentos = Atendimento.query.filter_by(paciente_id=paciente_id).all()
    return render_template('detalhes_paciente.html', user=current_user, paciente=paciente, atendimentos=atendimentos)
