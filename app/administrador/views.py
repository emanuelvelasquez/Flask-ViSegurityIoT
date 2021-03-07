# app/admin/views.py

from flask import abort, flash, redirect, render_template, url_for,current_app,request
from flask_login import current_user, login_required
from flask_mail import  Message
from . import administrador
from ..models import Role, Usuario, MedioNotificacion,UsuarioNotificacion
from .. import db
from app import mail
from app.common.mail import send_email
from .forms import RoleForm, UsuarioAsignaForm, UsuarioForm, UsuarioEditaForm, MedioNotificacionForm,UsuarioMedioForm

def chequeo_admin():
    if not current_user.is_admin:
        abort(403) 

@administrador.route('/roles')
@login_required
def lista_roles():
    chequeo_admin()
   
    roles = Role.query.all()
    return render_template('administrador/roles/roles.html',roles=roles, title='Roles')


@administrador.route('/roles/crear', methods=['GET', 'POST'])
@login_required
def crear_role():
    
    chequeo_admin()

    crear_rol = True

    form = RoleForm()
    if form.validate_on_submit():
        rol = Role(name=form.name.data,
                    description=form.description.data)

        try:
            # add role to the database
            db.session.add(rol)
            db.session.commit()
            flash('Se creo el rolo exitosamente!!!')
        except:
            # in case role name already exists
            flash('Error: El Rol ya existe')

        # redirect to the roles page
        return redirect(url_for('administrador.lista_roles'))

    # load role template
    return render_template('administrador/roles/role.html', crear_rol=crear_rol,form=form, title='Crear Role')


@administrador.route('/roles/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def edita_role(id):
    chequeo_admin()
 
    crear_rol = False

    rol = Role.query.get_or_404(id)
    form = RoleForm(objet=rol)

    if form.validate_on_submit():
        rol.name = form.name.data
        rol.description = form.description.data
        db.session.commit()
        flash("Se edito Correctamente el ROl!!!")

        return redirect(url_for('administrador.lista_roles'))

    form.description.data = rol.description
    form.name.data = rol.name

    return render_template('administrador/roles/role.html',crear_rol=crear_rol,form=form,title="Editar Rol" )

@administrador.route('/eliminar/<int:id>', methods=['GET', 'POST'])
@login_required
def elimina_role(id):
    chequeo_admin()

    rol = Role.query.get_or_404(id)

    db.session.delete(rol)
    db.session.commit()

    flash("Se elimino correctmante el ROl!!!")

    return redirect(url_for("administrador.lista_roles"))


@administrador.route('/usuariosroles')
@login_required
def lista_usuariorol():
    chequeo_admin()

    usuarios=Usuario.query.all()

    return render_template('administrador/usuariosroles/usuariorol.html',usuarios=usuarios,title='Usuarios')


@administrador.route('/usuariosroles/usuariorolasigna/<int:id>', methods=['GET', 'POST'])
@login_required
def asigna_usuariorol(id):

    chequeo_admin()

    usuario = Usuario.query.get_or_404(id)

 
    
    form= UsuarioAsignaForm(obj=usuario)
    if form.validate_on_submit():
        usuario.role=form.role.data
        if form.role.data==1:
            usuario.is_admin=1
        else:
            usuario.is_admin=0
        db.session.add(usuario)
        db.session.commit()
        flash("Se asisgno el rol correctamente!!!")

        return redirect(url_for("administrador.lista_usuariorol"))
    
    return render_template('administrador/usuariosroles/usuariorolasigna.html',usuario=usuario,form=form,title="Asignar Rol")



#Usuarios Funciones Eliminar, Editar , Crear, Lista
@administrador.route('/usuarios')
def lista_usuarios():
    #filtro los usuarios que son administradores
    usuarios = Usuario.query.all()
    return render_template('administrador/usuarios/usuarios.html',usuarios=usuarios, title=' Lista Usuarios')

@administrador.route('/usuarios/edita/<int:id>', methods=['GET', 'POST'])
def edita_usuario(id):
    chequeo_admin()

    crear_usuario = False

    usuario = Usuario.query.get_or_404(id)
    form = UsuarioEditaForm(objet=usuario)

    if form.validate_on_submit():
        usuario.username = form.username.data
        usuario.nombre = form.nombre.data
        usuario.apellido = form.apellido.data
        usuario.email = form.email.data
        usuario.is_admin =form.is_admin.data
        usuario.id_telegram = form.id_telegram.data
        db.session.commit()
        flash("Se edito Correctamente el Usuario!!!")

        return redirect(url_for('administrador.lista_usuarios'))

    form.username.data = usuario.username
    form.nombre.data = usuario.nombre
    form.apellido.data = usuario.apellido
    form.email.data = usuario.email
    form.is_admin.data = usuario.is_admin
    form.id_telegram.data = usuario.id_telegram
    return render_template('administrador/usuarios/usuario.html',crear_usuario=crear_usuario,form=form,title="Editar Usuario" )
    

@administrador.route('/usuarios/crear', methods=['GET', 'POST'])
@login_required
def crear_usuario():
    chequeo_admin()
    crear_usuario = True
    form = UsuarioForm()

    if form.validate_on_submit():
        usuario = Usuario(email=form.email.data,
                            username=form.username.data,
                            nombre=form.nombre.data,
                            apellido=form.apellido.data,
                            password=form.password.data)

        # agrego un nuevo usuario al base de datos
        db.session.add(usuario)
        db.session.commit()
        #NOtifico al usuario creado
        html = render_template('template_mail/mail_crea_usu.html',nombre=form.nombre.data,contraseña=form.password.data)
        send_email(subject='Creacion de Usuario',
                        sender=current_app.config['DONT_REPLY_FROM_EMAIL'],
                        recipients=[form.email.data,],
                        text_body=f'Hola {form.nombre.data}, bienvenid@ al miniblog de Flask',
                        html_body=html)

        flash("Se creo un Usuario correctamente!!!")
        return redirect(url_for('administrador.lista_usuarios'))
    
    if len(form.errors)>0:
        errores=""
        for error in form.errors:
            errores= form.errors[error][0]
        flash(errores)


    return render_template('administrador/usuarios/usuario.html', crear_usuario=crear_usuario,form=form, title='Crear Usuario')

@administrador.route('/usuarios/elimina/<int:id>')
@login_required
def elimina_usuario(id):
    chequeo_admin()
    usuario=Usuario.query.get_or_404(id)

    db.session.delete(usuario)
    db.session.commit()

    flash("Se elimino correctmante el Usuario!!!")

    return redirect(url_for("administrador.lista_usuarios"))

@administrador.route('/listamedionotificaciones')
@login_required
def lista_medio_notificaciones():
    chequeo_admin()
    medionotificacion= MedioNotificacion.query.all()

    return render_template('administrador/medionotificaciones/listamedionotificaciones.html',medionotificacion=medionotificacion,title="Medio de Notificacion")

@administrador.route('/medionotificaciones/medionotificacion/<int:id>')
@login_required
def medio_notificacion(id):
    chequeo_admin()
    
    listausuarios= Usuario.query.all()
    usuarios=[]
    
    for usu in listausuarios:

        result= UsuarioNotificacion.query.filter_by(medionotificacion_id=id).filter_by(usuario_id=usu.id).first()
        if not result:
            usuarios.append(usu)
        

    usuariomedio=UsuarioNotificacion.query.filter_by(medionotificacion_id=id).all()   
    #usuarios que estan relacionados con el medio seleccionado
    mediousuario=[]
    
    for user in usuariomedio:
        usu=Usuario.query.filter_by(id=user.usuario_id).first()
        mediousuario.append([usu.username,usu.email,user.id,id])
        #mediousuario.append(Usuario.query.filter_by(id=user.usuario_id).first())
        

    form=UsuarioMedioForm(idmedio=id)
    title=MedioNotificacion.query.filter_by(id=id).first().name 
    return render_template('administrador/medionotificaciones/medionotificacion.html',form=form,usuarios=usuarios,mediousuario=mediousuario,title=title)

@administrador.route('/medionotificaciones/asignausuariomedio', methods=['POST'])
@login_required
def usuario_medio_notificacion():
    chequeo_admin()
    
    form=UsuarioMedioForm(request.form)
    if form.validate_on_submit():
        usuariomedio = UsuarioNotificacion(usuario_id=form.iduser.data, medionotificacion_id =form.idmedio.data)
        db.session.add(usuariomedio)
        db.session.commit()
    
    usu=Usuario.query.filter_by(id=form.iduser.data).first()
    medio=MedioNotificacion.query.filter_by(id=form.idmedio.data).first().name
    if (medio=="Telegram"):
        html = render_template('template_mail/mail_usuario_telegram.html',nombre=usu.nombre)
        send_email(subject='Aviso',
                        sender=current_app.config['DONT_REPLY_FROM_EMAIL'],
                        recipients=[usu.email,],
                        text_body=f'Hola {usu}, se te agrego al grupo que recibira notificaciones mediante Telegram',
                        html_body=html)
    else:
        html = render_template('template_mail/mail_usuario_correo.html',nombre=usu.nombre)
        send_email(subject='Aviso',
                        sender=current_app.config['DONT_REPLY_FROM_EMAIL'],
                        recipients=[usu.email,],
                        text_body=f'Hola {usu}, se te agrego al grupo que recibira notificaciones mediante Correo',
                        html_body=html)

    
    flash('Se agrego correctamente el Usuario!!!')
    return redirect(url_for('administrador.medio_notificacion',id=form.idmedio.data))

@administrador.route('/eliminarusuariomedio/<int:id>/<int:idmedio>')
@login_required
def elimina_usuario_medio(id,idmedio):
    chequeo_admin()

    usuariomedio= UsuarioNotificacion.query.get_or_404(id)
    db.session.delete(usuariomedio)
    
    if idmedio==2:

        usu= Usuario.query.get_or_404(usuariomedio.usuario_id)
        usu.id_telegram = None
    
    db.session.commit()

    flash('Se quito correctamente el Usuario de este Medio')
    return redirect(url_for('administrador.medio_notificacion',id=idmedio))

