from flask import render_template
from app.models.gift import Gift
from app.view_models.book import BookViewModel
from . import web


@web.route('/')
def index():
    resent_gifts = Gift.resent()
    books = [BookViewModel(gift.book) for gift in resent_gifts]
    return render_template('index.html', recent=books)


@web.route('/personal')
def personal_center():
    pass
