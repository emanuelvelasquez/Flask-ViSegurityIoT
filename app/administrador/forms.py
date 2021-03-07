# app/admin/forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, ValidationError,PasswordField, HiddenField, IntegerField ,BooleanField
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms.ext.sqlalchemy.fields import QuerySelectField

from ..models import Role, Usuario

class RoleForm(FlaskForm):
    name  =  StringField("Nombre", validators=[DataRequired()])
    description = StringField("Descripcion", validators=[DataRequired()])
    submit = SubmitField("Guardar")

class UsuarioAsignaForm(FlaskForm):
    role = QuerySelectField(query_factory=lambda: Role.query.all(),
                            get_label="name")

    submit = SubmitField("Guardar")

class UsuarioForm(FlaskForm):
    """
    Formulario de Usuario
    """
    
    username = StringField('Nombre de Usuario', validators=[DataRequired()])
    nombre = StringField('Nombre', validators=[DataRequired()])
    apellido = StringField('Apellido', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Contraseña', validators=[DataRequired(),EqualTo('password_confirm',message='La contraseñas no son iguales!!!')])
    password_confirm = PasswordField("Confirma Contraseña",validators=[DataRequired()])
    submit = SubmitField('Guardar')

    def validate_email(self, field):
        if Usuario.query.filter_by(email=field.data).first():
            raise ValidationError('El correo ingresado ya Existe')

    def validate_username(self, field):
        if Usuario.query.filter_by(username=field.data).first():
            raise ValidationError('Nombre de Usuario ya existente')

class UsuarioEditaForm(FlaskForm):
    """
    Formulario de Usuario
    """
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    username = StringField('Nombre de Usuario', validators=[DataRequired()])
    nombre = StringField('Nombre', validators=[DataRequired()])
    apellido = StringField('Apellido', validators=[DataRequired()])
    # is_admin = BooleanField('Administrador')
    # id_telegram = StringField('Cuenta Telegram')

    submit = SubmitField('Guardar')

class MedioNotificacionForm(FlaskForm):
    name  =  StringField("Nombre", validators=[DataRequired()])
    description = StringField("Descripcion", validators=[DataRequired()])
    submit = SubmitField("Guardar")

class UsuarioMedioForm(FlaskForm):
    idmedio = StringField("idmedio",validators=[DataRequired()])
    iduser = StringField("Usuario", validators=[DataRequired()])
    submit= SubmitField('Agregar')


