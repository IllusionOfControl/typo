from typo import mail
from flask import url_for, current_app
from flask_mail import Message


def sendmail(addr, subject, text):
    sender = current_app.config.get('APP_EMAIL')
    msg = Message(subject, sender=sender, recipients=addr)
    msg.body = text
    mail.send(msg)


def forgot_password(addr, username):
    pass