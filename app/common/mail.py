import logging, re , os
from smtplib import SMTPException
from threading import Thread
from flask import current_app,render_template, Flask , request
from flask_mail import Message,Mail
from app import mail
import app as current
logger = logging.getLogger(__name__)

def _send_async_email(app, msg):
    with app.app_context():
        try:
            mail.send(msg)
        except SMTPException:
            logger.exception("Ocurrió un error al enviar el email")


def send_email(subject, sender, recipients, text_body,cc=None, bcc=None, html_body=None):
    msg = Message(subject, sender=sender, recipients=recipients, cc=cc, bcc=bcc)
    msg.body = text_body
    if html_body:
        msg.html = html_body
    

    Thread(target=_send_async_email, args=(current_app._get_current_object(), msg)).start()


# def send_notificacion(path_img,objetos,camara):
#     with current_app._get_current_object().app_context():
#         msg = Message(f'Notificacion de Alerta del {camara}',['emanuel060120@gmail.com',],"Notificacion de alerta")
#         msg.body = "Notificacion de alerta"
#         #html_body = render_template('template_mail/mail_notificacion.html',objetos=objetos)
#         msg.attach('header.gif','image/gif',open(path_img, 'rb').read(), 'inline', headers={'Content-ID': '<reconocimiento>'})
#         #msg.html = html_body
#         #mail.send(msg)
#         mail.send(msg)

        

