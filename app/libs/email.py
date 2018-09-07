from threading import Thread

from flask import current_app, render_template

from app import mail
from flask_mail import Message


def send_async_mail(app, msg):
    with app.app_context():
        try:
            mail.send(msg)
        except Exception as e:
            pass


def send_mail(to, subject, template, **kwargs):
    # msg = Message('测试邮件', sender='aaa@qq.com', body='Test',
    #               recipients=['user@qq.com'])
    msg = Message('[codes_room]' + '' + subject,
                  sender=current_app.config['MAIL_USERNAME'],
                  recipients=[to]
                  )
    msg.html = render_template(template, **kwargs)

    # 异步发送邮件
    # 获取传递真实的 app 而不是代理 app(current_app)
    app = current_app._get_current_object()
    thr = Thread(target=send_async_mail, args=[app, msg])
    thr.start()
