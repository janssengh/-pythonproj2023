from flask import render_template, session, request, redirect, url_for, flash
from loja.produtos.models import Product, Brand, Category
from loja import app, db, bcrypt
from .forms import RegistrationForm, LoginFormulario
#import os
#from werkzeug.security import generate_password_hash, check_password_hash

from .models import User


@app.route('/admin')
def admin():
    if 'email' not in session:
        flash(f'Favor fazer o seu login no sistema primeiro!', 'danger')
        return redirect(url_for('login'))
    produtos = Product.query.all()
    return render_template('admin/index.html', titulo='Administrador', produtos=produtos)

@app.route('/marcas')
def marcas():
    if 'email' not in session:
        flash(f'Favor fazer o seu login no sistema primeiro!', 'danger')
        return redirect(url_for('login'))
    marcas = Brand.query.order_by(Brand.id.desc()).all()
    return render_template('admin/marca.html', titulo='Pagina Fabricantes', marcas=marcas)

@app.route('/categoria')
def categoria():
    if 'email' not in session:
        flash(f'Favor fazer o seu login no sistema primeiro!', 'danger')
        return redirect(url_for('login'))
    categorias = Category.query.order_by(Category.id.desc()).all()

    return render_template('admin/marca.html', titulo='Pagina Categorias', categorias=categorias)

@app.route('/registrar', methods=['GET', 'POST'])
def registrar():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        hash_password = bcrypt.generate_password_hash(form.password.data)
        user = User(name=form.name.data, user=form.user.data, email=form.email.data, password=hash_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Obrigado {form.name.data} por cadastrar !','success')
        return redirect(url_for('login'))
    return render_template('admin/registrar.html', form=form, titulo='Login')

@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginFormulario(request.form)
    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            session['email'] = form.email.data
            flash(f'{form.email.data} logado com sucesso!', 'success')
            return redirect(request.args.get('next')or url_for('admin'))
        else:
            flash('E-mail/Senha inválidos ou não cadastrados!', 'danger')
    return render_template('admin/login.html', form=form, titulo='Login')
