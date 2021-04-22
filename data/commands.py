from data import db_session
from data.category import Category
from data.shop_items import Items
from data.users import User


def create_basket(title, content, user_id):
    basket = Basket(title=title, content=content,
                    user_id=user_id)
    db_sess = db_session.create_session()
    db_sess.add(basket)
    db_sess.commit()


def create_item(name, content, about, characteristics, price, category, image):
    db_sess = db_session.create_session()
    item = Items(name=name, content=content,
                 about=about, characteristics=characteristics, price=price, image=image)
    item.categories.append(db_sess.query(Category).filter(Category.name == category).first())
    db_sess.add(item)
    db_sess.commit()


def edit_item(id_item, content=None, name=None, about=None):
    db_sess = db_session.create_session()
    item = db_sess.query(Items).filter(Items.id == id_item).first()
    if content:
        item.content = content
    if name:
        item.name = name
    if about:
        item.about = about
    db_sess.commit()


def delete_item(item_id):
    db_sess = db_session.create_session()
    item = db_sess.query(Items).filter(Items.id == item_id).first()
    db_sess.delete(item)
    db_sess.commit()


def write_to_file(data, filename):
    # возможная проблема дата
    print(type(data))
    file_path = f"static/img/{filename}"

    import os.path
    if not os.path.exists(file_path):
        # Преобразование двоичных данных в нужный формат
        with open(file_path, 'wb') as file:
            file.write(data)
        print("Данный из blob сохранены в: ", file_path, "\n")


'''write_to_file(img, 'photo.jpg')'''


def convert_to_binary_data(filename):

    # Преобразование данных в двоичный формат
    with open(filename, 'rb') as file:
        blob_data = file.read()
    return blob_data