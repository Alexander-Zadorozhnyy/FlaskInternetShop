from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, BooleanField, SelectField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, InputRequired


class RegisterForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    name = StringField('Имя пользователя', validators=[DataRequired()])
    about = TextAreaField("Немного о себе")
    submit = SubmitField('Войти')


class SupportForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    theme = SelectField(coerce=int, choices=[])
    question = TextAreaField("Напишите наиболее полное содержание вашего вопроса", validators=[DataRequired()])
    submit = SubmitField('Отправить')


class LoginForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class BuyItem(FlaskForm):
    pick_up_service = BooleanField("Самовывоз", default=False)
    delivery = BooleanField("Доставка", default=False)
    place_take = SelectField(coerce=int, choices=[])
    submit = SubmitField('Перейти на страницу оплаты')

