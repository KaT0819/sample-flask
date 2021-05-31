from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from market.models import User


class RegisterForm(FlaskForm):

    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('そのユーザ名はすでに使われています。他の名まえを設定してください。')

    def validate_email(self, email_to_check):
        user = User.query.filter_by(email=email_to_check.data).first()
        if user:
            raise ValidationError('そのメールアドレスはすでに使われています。他のメールアドレスを設定してください。')

    username = StringField(label='ユーザ名:', validators=[Length(min=2, max=30), DataRequired()])
    email = StringField(label='メールアドレス:', validators=[Email(), DataRequired()])
    password1 = PasswordField(label='パスワード:', validators=[Length(min=6), DataRequired()])
    password2 = PasswordField(label='パスワード確認:', validators=[EqualTo('password1'), DataRequired()])

    submit = SubmitField(label='アカウント登録')


class LoginForm(FlaskForm):
    username = StringField(label='ユーザ名:', validators=[DataRequired()])
    password = PasswordField(label='パスワード:', validators=[DataRequired()])

    submit = SubmitField(label='ログイン')
