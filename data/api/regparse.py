from flask_restful import reqparse

parser = reqparse.RequestParser()
parser.add_argument('name', required=True)
parser.add_argument('content', required=True)
parser.add_argument('category', required=True)
parser.add_argument('about', required=True)
parser.add_argument('characteristics', required=True)
parser.add_argument('img', required=True)
parser.add_argument('price', required=True)


parser_for_basket = reqparse.RequestParser()
parser_for_basket.add_argument('id_user', required=True)
parser_for_basket.add_argument('id_item', required=True)