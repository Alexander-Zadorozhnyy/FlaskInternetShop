import os

from flask import Flask, render_template, redirect, flash, make_response, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_restful import Api

from data import db_session
from data.api import items_recources
from data.basket import Basket
from data.category import Category, category_to_items
from data.commands import create_item, create_basket, edit_item, delete_item, write_to_file
from data.support_question import Questions
from data.theme_questions import Themes
from data.users import User
from data.shop_items import Items
from forms.user import RegisterForm, SupportForm, LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)
api = Api(app)
db_sess = None

ALL_TYPES = ['bg-dark me-md-3 pt-3 px-3 pt-md-5 px-md-5 text-center text-white overflow-hidden',
             'bg-light me-md-3 pt-3 px-3 pt-md-5 px-md-5 text-center overflow-hidden',
             'bg-light me-md-3 pt-3 px-3 pt-md-5 px-md-5 text-center overflow-hidden',
             'bg-primary me-md-3 pt-3 px-3 pt-md-5 px-md-5 text-center text-white overflow-hidden',
             'bg-light me-md-3 pt-3 px-3 pt-md-5 px-md-5 text-center overflow-hidden',
             'bg-light me-md-3 pt-3 px-3 pt-md-5 px-md-5 text-center overflow-hidden'
             ]


@app.route('/')
@app.route('/index')
def index():
    items = [str(item).split('-') for item in db_sess.query(Items).all()]

    return render_template("index.html", count=len(items), all_types=ALL_TYPES, items=items)  # , items=items


@app.route('/support', methods=['GET', 'POST'])
def support():
    global db_sess
    form = SupportForm()
    form.theme.choices = [(theme.id, theme.theme) for theme in db_sess.query(Themes).all()]
    if form.validate_on_submit():
        if db_sess.query(User).filter(User.email == form.email.data).first():
            question = Questions(question=form.question.data,
                                 user_id=db_sess.query(User.id).filter(User.email == form.email.data).first()[0],
                                 theme_id=form.theme.data)
            db_sess.add(question)
            db_sess.commit()
            flash("Ваш запрос успешно отправлен в тех.поддержку", "success")
        else:
            return render_template('support.html', title='Поддержка',
                                   form=form,
                                   message="Обращаться с вопросами в тех.поддержку могут только зарегистрированные пользователи."
                                           " Попробуйте ввести корректный email, если у вас уже усть аккаунт. Иначе же создайте новый")
        return redirect('/index')
    return render_template('support.html', title='Поддержка', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    global db_sess
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            about=form.about.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@login_manager.user_loader
def load_user(user_id):
    return db_sess.query(User).get(user_id)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found !!!'}), 404)


@app.route('/login', methods=['GET', 'POST'])
def login():
    global user
    form = LoginForm()
    if form.validate_on_submit():
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/filtred_items/<string:type_item>')
def filtred_items(type_item):
    category, type_search = None, None
    filter_types = ['bg-dark me-md-3 pt-3 px-3 pt-md-5 px-md-5 text-center text-white overflow-hidden',
                    'bg-light me-md-3 pt-3 px-3 pt-md-5 px-md-5 text-center overflow-hidden',
                    'bg-light me-md-3 pt-3 px-3 pt-md-5 px-md-5 text-center overflow-hidden',
                    'bg-dark me-md-3 pt-3 px-3 pt-md-5 px-md-5 text-center text-white overflow-hidden',
                    ]
    if type_item == 'phones':
        type_search = 2
        category = 'телефоны'
    elif type_item == 'watch':
        type_search = 4
        category = 'часы'
    elif type_item == 'tv':
        type_search = 3
        category = 'телевизоры'
    elif type_item == 'tablets':
        type_search = 1
        category = 'планшеты'
    id_items = [item[0] for item in
                db_sess.query(category_to_items.c.item).filter(category_to_items.c.category == type_search).all()]

    items = [str(item).split('-') for item in db_sess.query(Items).filter(Items.id.in_(id_items)).all()]
    return render_template("filtred_items.html", count=len(items), all_types=filter_types, items=items,
                           category=category)


@app.route('/more/<int:id>', methods=['GET', 'POST'])
def more(id):
    item = db_sess.query(Items).filter(Items.id == id).first()
    characteristics = item.characteristics.split('%')
    img = item.content
    return render_template('info_more.html', characteristics=characteristics, count=len(characteristics), image=img,
                           id=id)


# для корзины
"""
<div class="card mb-3" style="max-width: 540px;">
  <div class="row no-gutters">
    <div class="col-md-4">
      <img src="..." class="card-img" alt="...">
    </div>
    <div class="col-md-8">
      <div class="card-body">
        <h5 class="card-title">Название карточки</h5>
        <p class="card-text">This is a wider card with supporting text below as a natural lead-in to additional content. This content is a little bit longer.</p>
        <p class="card-text"><small class="text-muted">Last updated 3 mins ago</small></p>
      </div>
    </div>
  </div>
</div>"""


@app.route('/basket', methods=['GET', 'POST'])
def basket_show():
    if current_user.is_authenticated:
        id_items = [item[0] for item in
                    db_sess.query(Basket.item_id).filter(Basket.user_id == current_user.id).all()]
        items = [str(item).split('-') for item in db_sess.query(Items).filter(Items.id.in_(id_items)).all()]
        return render_template("basket.html", items=items, count=len(items))


@app.route('/add_to_basket/<int:id_item>', methods=['GET', 'POST'])
def add_to_basket(id_item):
    global db_sess
    if current_user.is_authenticated:
        if not db_sess.query(Basket.item_id).filter(Basket.user_id == current_user.id).filter(
                Basket.item_id == id_item).first():
            bas = Basket(item_id=id_item, user_id=current_user.id)
            db_sess.add(bas)
            db_sess.commit()
            flash("Товар успешно добавлен в вашу карзину.")
        else:
            flash('Товар уже у вас в корзине')
    else:
        flash("Для начала войдите в вашу учётную запись для добавления товара в карзину.")
    return redirect("/")


@app.route('/buy_item/<int:id_item>', methods=['GET', 'POST'])
def buy_item(id_item):
    return redirect("/")


if __name__ == '__main__':
    db_session.global_init("db/shop_info.db")
    db_sess = db_session.create_session()
    api.add_resource(items_recources.ItemsListResource, '/api/v2/items')
    api.add_resource(items_recources.ItemsResource, '/api/v2/items/<int:items_id>')
    api.add_resource(items_recources.CategoryListResource, '/api/v2/categories')
    api.add_resource(items_recources.QuestionsListResource, '/api/v2/questions')
    api.add_resource(items_recources.BasketsListResource, '/api/v2/baskets')
    api.add_resource(items_recources.UsersListResource, '/api/v2/users')
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)