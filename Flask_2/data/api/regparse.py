from flask_restful import reqparse

parser = reqparse.RequestParser()
parser.add_argument('name', required=True)
parser.add_argument('content', required=True)
parser.add_argument('category', required=True)
parser.add_argument('about', required=True)
parser.add_argument('characteristics', required=True)
parser.add_argument('img', required=True)
parser.add_argument('price', required=True)
