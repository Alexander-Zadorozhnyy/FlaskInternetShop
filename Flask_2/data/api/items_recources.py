import json

from flask import jsonify, request
from flask_restful import reqparse, abort, Api, Resource

from Flask_2.data.category import Category, category_to_items
from Flask_2.data.commands import write_to_file
from Flask_2.data.shop_items import Items

from Flask_2.data import db_session
from Flask_2.data.api.regparse import parser
from Flask_2.data.support_question import Questions
from Flask_2.data.theme_questions import Themes
from Flask_2.data.users import User


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
                    [(item.to_dict(only=('id', 'name', 'content', 'characteristics', 'price')),
                      session.query(Category.name).filter(Category.id ==
                                                          session.query(category_to_items.c.category).filter(
                                                              category_to_items.c.item == str(item).split('-')[
                                                                  1]).first()[0]).first()[0])
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
        with open(f"static/img/{args['content']}", 'wb') as f:
            f.write(args['img'].encode('latin1'))
        '''write_to_file(args['img'], args['img_name'])'''
        print(session.query(Category.id).first()[0])
        item.categories.append(session.query(Category).filter(Category.name == args['category']).first())
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


class QuestionsListResource(Resource):
    def get(self):
        session = db_session.create_session()
        news = session.query(User.name, User.email, Questions.question, Themes.theme).filter(
            User.id == Questions.user_id).filter(Questions.theme_id == Themes.id).all()
        print(news)
        data = {}
        for item in news:
            new_data = {'name': item[0],
                        'email': item[1],
                        'question': item[2],
                        'theme': item[3]}
        return jsonify(
            {
                'questions':
                    [{'name': item[0],
                      'email': item[1],
                      'question': item[2],
                      'theme': item[3]} for item in news]
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
