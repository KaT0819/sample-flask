from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, EqualTo, Email, DataRequired


class RegisterForm(FlaskForm):
    username = StringField(label='ユーザ名:', validators=[Length(min=2, max=30), DataRequired()])
    email = StringField(label='メールアドレス:', validators=[Email(), DataRequired()])
    password1 = PasswordField(label='パスワード:', validators=[Length(min=6), DataRequired()])
    password2 = PasswordField(label='パスワード確認:', validators=[EqualTo('password1'), DataRequired()])

    submit = SubmitField(label='アカウント登録')

