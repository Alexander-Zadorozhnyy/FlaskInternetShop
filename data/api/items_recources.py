import json

from flask import jsonify, request
from flask_restful import reqparse, abort, Api, Resource

from data.basket import Basket
from data.category import Category, category_to_items
from data.commands import write_to_file
from data.shop_items import Items

from data import db_session
from data.api.regparse import parser, parser_for_basket, parser_for_question
from data.support_question import Questions
from data.theme_questions import Themes
from data.users import User


def abort_if_news_not_found(items_id):
    session = db_session.create_session()
    news = session.query(Items).get(items_id)
    if not news:
        abort(404, message=f"Items {items_id} not found")


def abort_if_question_not_found(items_id):
    session = db_session.create_session()
    news = session.query(Questions).get(items_id)
    if not news:
        abort(404, message=f"Question {items_id} not found")


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
        with open(f"static/img/{args['content']}", 'wb') as f:
            f.write(args['img'].encode('latin1'))
        item = Items(
            name=args['name'],
            content=args['content'],
            about=args['about'],
            characteristics=args['characteristics'],
            price=args['price']
        )
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
        args = parser_for_question.parse_args()
        session = db_session.create_session()
        item = Questions(
            question=args['question'],
            theme_id=session.query(Themes.id).filter(Themes.theme == args['theme']).first()[0],
            user_id=session.query(User.id).filter(User.email == args['email']).first()[0]
        )
        session.add(item)
        session.commit()
        return jsonify({'success': 'OK'})


class QuestionResource(Resource):
    def delete(self, question_id):
        abort_if_question_not_found(question_id)
        session = db_session.create_session()
        quest = session.query(Questions).get(question_id)
        session.delete(quest)
        session.commit()
        return jsonify({'success': 'OK'})


class BasketsListResource(Resource):
    def get(self):
        session = db_session.create_session()
        news = session.query(User.id, Items.id, Items.name).filter(
            User.id == Basket.user_id).filter(Items.id == Basket.item_id).all()
        return jsonify(
            {
                'baskets':
                    [{'id_user': item[0],
                      'id_item': item[1],
                      'name_item': item[2]} for item in news]
            }
        )

    def post(self):
        args = parser_for_basket.parse_args()
        session = db_session.create_session()
        item = Basket(
            user_id=args['id_user'],
            item_id=args['id_item']
        )
        session.add(item)
        session.commit()
        return jsonify({'success': 'OK'})


class UsersListResource(Resource):
    def get(self):
        session = db_session.create_session()
        news = session.query(User.id, User.name, User.email, User.created_date).all()
        return jsonify(
            {
                'users':
                    [{'id_user': item[0],
                      'name_user': item[1],
                      'email_user': item[2],
                      'created_date': item[3]} for item in news]
            }
        )
