from requests import get, post, delete

from Flask_2.data import db_session
from Flask_2.data.commands import create_item, write_to_file
from Flask_2.data.shop_items import Items

'''print(post('http://localhost:5000/api/news').json())

print(post('http://localhost:5000/api/news',
           json={'title': 'Заголовок'}).json())

print(post('http://localhost:5000/api/news',
           json={'title': 'Заголовок',
                 'content': 'Текст новости',
                 'user_id': 1,
                 'is_private': False}).json())

print(delete('http://localhost:5000/api/news/999').json())
# новости с id = 999 нет в базе

print(delete('http://localhost:5000/api/news/1').json())'''
'''s = get('http://localhost:5000//api/v2/image/1').json()['image']
print(s)'''

with open('photo.jpg', 'rb') as f:
    a = f.read()
a = a.decode('latin1')
a = a.encode('latin1')

with open('good.jpg', 'wb') as file:
    file.write(a)