from flask import Blueprint, render_template

web = Blueprint('web', __name__, template_folder='templates')


@web.app_errorhandler(404)
def not_found(e):
    # AOP 思想
    return render_template('404.html'), 404


from . import book, auth, drift, gift, main, wish
