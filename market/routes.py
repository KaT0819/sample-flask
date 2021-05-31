from flask import (flash, redirect, render_template,
                   url_for)
from flask_login import login_user, logout_user

from market import app, db
from market.forms import LoginForm, RegisterForm
from market.models import Item, User


@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')


@app.route('/market')
def market_page():
    items = Item.query.all()
    # items = [
    #     {'id': 1, 'name': '電話', 'barcode': '893212299897', 'price': 50000},
    #     {'id': 2, 'name': 'ラップトップ', 'barcode': '123456789012', 'price': 90000},
    #     {'id': 3, 'name': 'キーボード', 'barcode': '987654321012', 'price': 1500},
    # ]
    return render_template('market.html', item_name='Phone', items=items)


@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()

    if form.validate_on_submit():
        user_to_create = User(
            username=form.username.data,
            email=form.email.data,
            password_hash=form.password1.data,
        )
        db.session.add(user_to_create)
        db.session.commit()
        return redirect(url_for('market_page'))

    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'エラー：{err_msg}', category='danger')

    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()

    if form.validate_on_submit():
        app.logger.debug(form.username.data)
        app.logger.debug(User.query.filter_by(username=form.username.data))
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_collection(
            attempted_password=form.password.data
        ):
            login_user(attempted_user)
            flash('ログインできました。', category='info')
            return redirect(url_for('market_page'))
        else:
            flash('ユーザ名とパスワードが一致しませんでした。再度入力してください。', category='danger')

    return render_template('login.html', form=form)


@app.route('/logout')
def logout_page():
    logout_user()
    flash('ログアウトしました。', category='info')

    return redirect(url_for('home_page'))
