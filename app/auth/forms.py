# coding=utf-8
# app/auth/forms.py

from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Email, EqualTo

from ..models import Usuario


class RegistroForm(FlaskForm):
    """
    Form for users to create new account
    """
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    username = StringField('Nombre de Usuario', validators=[DataRequired()])
    nombre = StringField('Nombre', validators=[DataRequired()])
    apellido = StringField('Apellido', validators=[DataRequired()])
    password = PasswordField('Contraseña', validators=[DataRequired(),EqualTo('password_confirm',message='La contraseñas no son iguales!!!')])
    password_confirm = PasswordField("Confirma Contraseña",validators=[DataRequired()])
    submit = SubmitField('Registrarse')

    def validate_email(self, field):
        if Usuario.query.filter_by(email=field.data).first():
            raise ValidationError('El correo ingresado ya Existe')

    def validate_username(self, field):
        if Usuario.query.filter_by(username=field.data).first():
            raise ValidationError('Nombre de Usuario ya existente')


class LoginForm(FlaskForm):
    """
    Form for users to login
    """
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Iniciar Sesion')