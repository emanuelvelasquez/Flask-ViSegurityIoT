from flask import render_template, abort, Response, Flask, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from . import videostream
from ..models import Funciones, Eventos
from .forms import FuncionForm
from .. import db, mail #, sched
#from ..common.telegram_send import Send_Telegram, Send_Mensaje
#import cv2
import time
#from ..camaras.getvideo import get_video
#from .. import camaras

def chequeo_admin():
    if not current_user.is_admin:
        abort(403)

camIpLink = {
             "Frente",#camara numero 1
             "Porton"#camara numero 2
    }


@videostream.route('/videostream/stream/<string=id_cam>', methods=['GET'])
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
    chequeo_admin()
    funcion = Funciones.query.get_or_404(1)
    if inicia == "True":
        funcion.corriendo = 1

        for id_cam in camIpLink:
            
            #sched.add_job(func=tensorflow, trigger='cron', args=[id_cam, funcion.fin], minute=funcion.inicio, id=id_cam)

            time.sleep(2)

        msg = 'Se Inicio el Reconocimiento de Objetos!!!'

    else:
        funcion.corriendo = 0
        # jobss=sched.get_jobs().count()
        #sched.remove_all_jobs()
        # sched.shutdown()
        msg = 'Se Detuvo el Reconocimiento de Objetos!!!'

    db.session.commit()

    flash(msg)
    return redirect(url_for('videostream.funciones'))


@videostream.route('/periodo', methods=['POST'])
@login_required
def periodo():
    chequeo_admin()
    form = request.form
    funcion = Funciones.query.get_or_404(1)
    funcion.inicio = form['inicio']
    funcion.fin = form['fin']
    db.session.commit()

    msg = 'Se modifico exitosamente los periodos de Monitoreo!!!'
    flash(msg)
    return redirect(url_for('videostream.funciones'))

@videostream.route('/listaeventos')
def lista_eventos():

    chequeo_admin()
    #cargo la lista de eventos
    eventos= Eventos.query.all()

    return render_template('videostream/eventos.html',eventos=eventos, title='Listado de Eventos')


    
