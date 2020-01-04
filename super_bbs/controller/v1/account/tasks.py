import datetime
from flask import current_app
from flask_mail import Message
from super_bbs.model.users import CeleryTaskLogs
from super_bbs.core.extensions import mail, celery
from super_bbs.constants import web_title


@celery.task()
def send_register_mail(mail_addr, code):
    msg = Message(
        f'{web_title}注册码请查收',
        recipients=[mail_addr]
    )
    current_date = str(datetime.datetime.now())
    msg.html = f'''<h3>欢迎注册 {web_title}!</h3>
    <br>
    <div>您的注册码是: <span style="color: black;font-size:200%;font-weight:bold;">{code}</span></div>
    <br>
    <hr>
    <div>from: {web_title} at: {current_date}</div>
    '''
    mail.send(msg)
    current_app.logger.info(f'mail send to {mail_addr}, code {code}')


@celery.task()
def clean_celery_log():
    CeleryTaskLogs.query.filter(
        CeleryTaskLogs.done == 1,
        CeleryTaskLogs.task_status == 1,
        CeleryTaskLogs.time_modify < datetime.datetime.now() - datetime.timedelta(days=10)
    ).delete()
    return '清理成功'
