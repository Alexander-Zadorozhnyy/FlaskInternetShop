import flask
from flask import jsonify

from Flask_2.data import db_session
from Flask_2.data.category import Category
from Flask_2.data.shop_items import Items

blueprint = flask.Blueprint(
    'items_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/items')
def get_news():
    db_sess = db_session.create_session()
    news = db_sess.query(Items).all()
    print(news)
    return jsonify(
        {
            'items':
                [item.to_dict(only=('name', 'about', 'characteristics', 'price'))
                 for item in news]
        }
    )


@blueprint.route('/api/items/<int:item_id>', methods=['GET'])
def get_one_news(item_id):
    db_sess = db_session.create_session()
    items = db_sess.query(Items).get(item_id)
    if not items:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'items': items.to_dict(only=(
                'name', 'about', 'characteristics', 'price'))
        }
    )


@blueprint.route('/api/items', methods=['POST'])
def create_news():
    from flask import request
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['name', 'content', 'category', 'about', 'characteristics', 'price']):
        return jsonify({'error': 'Bad request'})
    db_sess = db_session.create_session()
    item = Items(
        name=request.json['name'],
        content=request.json['content'],
        about=request.json['about'],
        characteristics=request.json['characteristics'],
        price = request.json['price']
    )
    item.categories.append(db_sess.query(Category).filter(Category.name == request.json['category']).first())
    db_sess.add(item)
    db_sess.commit()
    return jsonify({'success': 'OK'})



@blueprint.route('/api/items/<int:news_id>', methods=['DELETE'])
def delete_news(news_id):
    db_sess = db_session.create_session()
    news = db_sess.query(Items).get(news_id)
    if not news:
        return jsonify({'error': 'Not found'})
    db_sess.delete(news)
    db_sess.commit()
    return jsonify({'success': 'OK'})
