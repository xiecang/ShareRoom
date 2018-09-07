from flask import current_app, flash, redirect, url_for, render_template

from app import db
from app.libs.enums import PendingStatus
from app.models.drift import Drift
from app.models.gift import Gift
# from app.view_models.gift import MyGifts
from app.view_models.trade import MyTrades
from . import web
from flask_login import login_required, current_user


@web.route('/my/gifts')
@login_required
def my_gifts():
    uid = current_user.id
    gift_of_mine = Gift.get_user_gifts(uid)
    isbn_list = [gift.isbn for gift in gift_of_mine]
    wish_count_list = Gift.get_wish_counts(isbn_list)
    view_model = MyTrades(gift_of_mine, wish_count_list)
    return render_template('my_gifts.html', gifts=view_model.trades)


@web.route('/gifts/book/<isbn>')
@login_required
def save_to_gifts(isbn):
    if current_user.can_save_to_list(isbn):
        # 事物
        gift = Gift()
        with db.auto_commit():
            gift.uid = current_user.id
            current_user.beans += current_app.config['BEANS_UPLOAD_ONE_BOOK']
            gift.isbn = isbn
            db.session.add(gift)
    else:
        flash("这本书已经添加至您的心愿清单或存在您的赠送清单，请不要重复添加")
    # ajax
    return redirect(url_for('web.book_detail', isbn=isbn))


@web.route('/gifts/<gid>/redraw')
@login_required
def redraw_from_gifts(gid):
    gift = Gift.query.filter_by(id=gid, launched=False).first_or_404()
    drift = Drift.query.filter_by(
        gift_id=gid, pending=PendingStatus.Waiting
    ).first()
    if drift:
        flash("这个礼物正处于交易状态，请前往鱼漂完成该交易")
    else:
        with db.auto_commit():
            current_user.beans -= current_app.config['BEANS_UPLOAD_ONE_BOOK']
            gift.delete()
    return redirect(url_for('web.my_gifts'))



