# coding=utf-8
# app/auth/views.py

from flask import flash, redirect, render_template, url_for, request
from flask_login import login_required, login_user, logout_user
from . import auth
from .forms import LoginForm, RegistroForm
from .. import db
from ..models import Usuario


@auth.route('/register', methods=['GET', 'POST'])
def register():
    """
    Handle requests to the /register route
    Add an employee to the database through the registration form
    """
    
    form = RegistroForm()
    if form.validate_on_submit():
        usuario = Usuario(email=form.email.data,
                            username=form.username.data,
                            nombre=form.nombre.data,
                            apellido=form.apellido.data,
                            password=form.password.data)

        # add employee to the database
        db.session.add(usuario)
        db.session.commit()
        flash('Regstro exitoso!!!, ahora debe Iniciar Sesion')

        # redirect to the login page
        return redirect(url_for('auth.login'))
    
    
    
    # load registration template
    return render_template('auth/registro.html', form=form, title='Registro')


@auth.route('/login', methods=['GET', 'POST'])
def login():

    form = LoginForm()
    if form.validate_on_submit():
        usuario = Usuario.query.filter_by(email=form.email.data).first()
        if usuario is not None and usuario.verify_password(form.password.data):
            login_user(usuario)
            
            if usuario.is_admin:
                return redirect(url_for('home.admin_dashboard'))
            else:
                return redirect(url_for('home.dashboard'))
        else:
            flash('Email o Contraseña Invalida')
    
    return render_template('auth/login.html',form=form,title='Inicio de Sesion')


@auth.route('/logout')
@login_required
def logout():
   
    logout_user()
    flash('Se cerro Sesion con exito!!!')

    return redirect(url_for('auth.login'))

