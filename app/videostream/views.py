from flask import render_template, abort, Response, Flask, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from . import videostream
from ..models import Funciones, Eventos, Configuraciones, Usuario, UsuarioNotificacion
from .forms import FuncionForm
from .. import db, mail 
import time, json
import requests
from requests.auth import HTTPBasicAuth 

def chequeo_admin():
    if not current_user.is_admin:
        abort(403)


@videostream.route('/videostream/stream/<string:id_cam>', methods=['GET'])
@login_required
def stream(id_cam):
    
    link_ngrok = Configuraciones.query.filter_by(nombre='ngrok').first().config + '/videostream/get_video/' + id_cam


    return render_template('videostream/stream.html', link=link_ngrok, title=id_cam.upper())


@videostream.route('/videostream/funciones')
@login_required
def funciones():
    chequeo_admin()
    funcion = Funciones.query.get_or_404(1)
    form = FuncionForm()
    form.inicio = funcion.inicio
    form.fin = funcion.fin
    return render_template("videostream/funcion.html", funcion=funcion, form=form, title="Administrar Tarea")


@videostream.route('/iniciarfin/<string:inicia>')
@login_required
def iniciar_fin(inicia):
    hecho = True

    while hecho:
        try:
            chequeo_admin()
            funcion = Funciones.query.get_or_404(1)
            link_ngrok = Configuraciones.query.filter_by(nombre='ngrok').first().config + '/videostream/iniciar_fin'
            usu=Configuraciones.query.filter_by(nombre='user-ngrok').first().config
            contra=Configuraciones.query.filter_by(nombre='pass-ngrok').first().config

            if inicia == "True":
                funcion.corriendo = 1
                data={
                    'inicia': True,
                    #'usu_telegram':[]
                }
                # Usuario_Telegram = UsuarioNotificacion.query.filter_by(medionotificacion_id=2)
                # for i in Usuario_Telegram:
                #     usu = Usuario.query.get_or_404(i.usuario_id)
                #     if usu.id_telegram is not None and usu.id_telegram != '':

                #         i=data['usu_telegram'].append(dict(id_telegram=usu.id_telegram))


                msg = 'Se Inicio el Reconocimiento de Objetos!!!'

            else:
                funcion.corriendo = 0
                data={
                    'inicia': False,
                }

                msg = 'Se Detuvo el Reconocimiento de Objetos!!!'

            result = requests.get(link_ngrok, json=data)#,auth=HTTPBasicAuth(usu,contra))
            if result.status_code != 200:
                abort(result.status_code)

            db.session.commit()
            hecho=False
            flash(msg)
            return redirect(url_for('videostream.funciones'))
            
        except Exception as e:
            abort(500)

    


@videostream.route('/periodo', methods=['POST'])
@login_required
def periodo():
    hecho = True

    while hecho:
        try:
            chequeo_admin()
            form = request.form
            funcion = Funciones.query.get_or_404(1)
            funcion.inicio = form['inicio']
            funcion.fin = form['fin']
            db.session.commit()
            hecho=False
            msg = 'Se modifico exitosamente los periodos de Monitoreo!!!'
            flash(msg)
            return redirect(url_for('videostream.funciones'))

        except Exception as e:
            abort(500)


@videostream.route('/listaeventos')
def lista_eventos():

    chequeo_admin()
    #cargo la lista de eventos
    eventos= Eventos.query.all()

    return render_template('videostream/eventos.html',eventos=eventos, title='Listado de Eventos')

@videostream.route('/videostream/get_imagen', methods=['POST'])
def get_imagen():
    paths = json.loads(request.data)["path"]

    linkngrok= Configuraciones.query.filter_by(nombre='ngrok').first().config
    response = requests.post(linkngrok + "/videostream/jpg_get", data=json.dumps(paths),headers = {'content-type': 'application/json'})
   
    return Response(response)

    
