from flask import Flask
from flask_login import LoginManager
from app.models import db
from flask_mail import Mail


login_manager = LoginManager()
mail = Mail()


def create_app():
    app = Flask(__name__)
    app.config.from_object('app.secure')
    app.config.from_object('app.setting')

    register_blueprint(app)

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'web.login'
    # login_manager.login_message = "请先登录或注册"

    mail.init_app(app)

    db.create_all(app=app)
    # 其它传入参数的写法 flask 上下文
    # with app.app_context():
    #     db.create_all()
    # 下面一行 告诉 flask_login 登录视图函数的位置 如果在需要登录的界面， 未登录会自动跳转登录
    return app


def register_blueprint(app):
    from app.web import web
    app.register_blueprint(web)


"""
Flask-Login 为 Flask 提供了会话管理。它处理日常的登入、登出并长期保留用户会话。

它会：

存储会话中活动用户的 ID，并允许你随意登入登出。
让你限制已登入（或已登出）用户访问视图。
实现棘手的“记住我”功能。
保护用户会话免遭 Cookie 盗用。
随后可能会与 Flask-Principal 或其它认证扩展集成。
无论如何，它不会：

限制你使用特定的数据库或其它存储方法。如何加载用户完全由你决定。
限制用户名和密码、OpenID 或其它认证方法的使用。
处理“登入或未登入”之外的权限。
处理用户注册信息或账号恢复。
"""