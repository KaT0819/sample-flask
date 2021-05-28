from flask import render_template, redirect, url_for

from market import app, db
from market.forms import RegisterForm
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
            password=form.password1.data,
        )
        db.session.add(user_to_create)
        db.session.commit()
        return redirect(url_for('market_page'))

    if form.errors != {}:
        for err_msg in form.errors.values():
            print(f'エラー：{err_msg}')

    return render_template('register.html', form=form)

