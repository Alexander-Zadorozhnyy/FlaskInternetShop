from flask import jsonify, request
from flask_restful import reqparse, abort, Api, Resource

from Flask_2.data.category import Category, category_to_items
from Flask_2.data.commands import write_to_file
from Flask_2.data.shop_items import Items

from Flask_2.data import db_session
from Flask_2.data.api.regparse import parser


def abort_if_news_not_found(items_id):
    session = db_session.create_session()
    news = session.query(Items).get(items_id)
    if not news:
        abort(404, message=f"Items {items_id} not found")


class ItemsResource(Resource):
    def get(self, items_id):
        abort_if_news_not_found(items_id)
        session = db_session.create_session()
        items = session.query(Items).get(items_id)
        return jsonify({
            'items': items.to_dict(only=(
                'id', 'name', 'content', 'characteristics', 'price'))
        })

    def delete(self, items_id):
        abort_if_news_not_found(items_id)
        session = db_session.create_session()
        news = session.query(Items).get(items_id)
        session.delete(news)
        session.commit()
        return jsonify({'success': 'OK'})


class ItemsListResource(Resource):
    def get(self):
        session = db_session.create_session()
        news = session.query(Items).all()
        return jsonify(
            {
                'items':
                    [(item.to_dict(only=('id', 'name', 'content', 'characteristics', 'price')), session.query(Category.name).filter(Category.id == session.query(category_to_items.c.category).filter(category_to_items.c.item == str(item).split('-')[1]).first()[0]).first()[0])
                     for item in news],
            }
        )

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        item = Items(
            name=args['name'],
            content=args['content'],
            about=args['about'],
            characteristics=args['characteristics'],
            price=args['price']
        )
        item.categories.append(session.query(Category).filter(Category.name == request.json['category']).first())
        session.add(item)
        session.commit()
        return jsonify({'success': 'OK'})


class CategoryListResource(Resource):
    def get(self):
        session = db_session.create_session()
        news = session.query(Category).all()
        return jsonify(
            {
                'categories':
                    [item.to_dict(only=('id', 'name'))
                     for item in news]
            }
        )

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        item = Category(
            name=args['name']
        )
        session.add(item)
        session.commit()
        return jsonify({'success': 'OK'})


class ImageRecource(Resource):
    def get(self, items_id):
        session = db_session.create_session()
        news = session.query(Items.image).filter(Items.id == items_id).first()[0]
        write_to_file(news, 'game.jpg')
        print(str(news))
        bt = bytes(str(news), encoding='utf-8')
        write_to_file(bt, 'game_1.jpg')
        return jsonify({'image': str(news)})
