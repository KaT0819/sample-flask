from flask import (flash, redirect, render_template,
                   url_for, request)
from flask_login import login_user, logout_user, login_required, current_user

from market import app, db
from market.forms import LoginForm, RegisterForm, PurchaseItemForm, SellItemForm
from market.models import Item, User


@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')


@app.route('/market', methods=['GET', 'POST'])
@login_required
def market_page():
    purchase_form = PurchaseItemForm()
    selling_form = SellItemForm()

    items = Item.query.filter_by(owner=None)
    owned_items = Item.query.filter_by(owner=current_user.id)
    # items = [
    #     {'id': 1, 'name': '電話', 'barcode': '893212299897', 'price': 50000},
    #     {'id': 2, 'name': 'ラップトップ', 'barcode': '123456789012', 'price': 90000},
    #     {'id': 3, 'name': 'キーボード', 'barcode': '987654321012', 'price': 1500},
    # ]

    return render_template('market.html', item_name='Phone', items=items, purchase_form=purchase_form, owned_items=owned_items, selling_form=selling_form)

@app.route('/market/buy', methods=['POST'])
@login_required
def market_buy_page():
    form = PurchaseItemForm()

    if form.validate_on_submit():
        purchased_item = request.form.get('purchased_item')
        p_item_object = Item.query.filter_by(name=purchased_item).first()
        if p_item_object:
            # 購入可能かチェック
            if current_user.can_purchase(p_item_object):
                p_item_object.buy(current_user)
                flash(f'おめでとうございます！ {p_item_object.name} を¥{p_item_object.price} で購入しました。', category='success')
            else:
                flash(f'残念ですが残高不足のため {p_item_object.name} を購入できません。', category='danger')

    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'エラー：{err_msg}', category='danger')

    # 購入後は一覧表示のため下記処理を継続
    return redirect(url_for('market_page'))


@app.route('/market/sell', methods=['POST'])
@login_required
def market_sell_page():
    form = SellItemForm()

    if form.validate_on_submit():
        sold_item = request.form.get('sold_item')
        s_item_object = Item.query.filter_by(name=sold_item).first()
        if s_item_object:
            if current_user.can_sell(s_item_object):
                s_item_object.sell(current_user)
                flash(f'おめでとうございます！ {s_item_object.name} を¥{s_item_object.price} で販売しました。', category='success')
            else:
                flash(f'販売する際にエラーが発生しました。 {s_item_object.name} を販売できません。', category='danger')

    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'エラー：{err_msg}', category='danger')

    # 購入後は一覧表示のため下記処理を継続
    return redirect(url_for('market_page'))


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

        login_user(user_to_create)
        flash('アカウントが登録できました。', category='info')

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
@login_required
def logout_page():
    logout_user()
    flash('ログアウトしました。', category='info')

    return redirect(url_for('home_page'))
