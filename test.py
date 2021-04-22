from requests import get, post, delete

from Flask_2.data import db_session
from Flask_2.data.commands import create_item, write_to_file
from Flask_2.data.shop_items import Items

from yandex_money.api import Wallet, ExternalPayment

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

'''with open('photo.jpg', 'rb') as f:
    a = f.read()
a = a.decode('latin1')
a = a.encode('latin1')

with open('good.jpg', 'wb') as file:
    file.write(a)'''

scope = ['account-info', 'operation-history'] # etc..
client_id = 'A76ACB24B8300F9585A065ECEBF272C746AC909DE178E8D696D17B6E1D0BA0C6'
redirect_uri = 'http://localhost/redirect'
url = Wallet.build_obtain_token_url(
            client_id,
            "http://localhost/redirect",
            ["account-info", "operation_history"]
        )
print(url)
access_token = Wallet.get_access_token(client_id, code, redirect_uri,
    client_secret=None)
api = Wallet(access_token)
account_info = api.account_info()
balance = account_info['balance'] # and so on

request_options = { "pattern_id": "p2p", "to": "410011161616877", "amount_due": "0.02", "comment": "test payment comment from yandex-money-python", "message": "test payment message from yandex-money-python", "label": "testPayment", "test_payment": True, "test_result": "success" }
request_result = api.request(request_options) # check status

process_payment = api.process({ "request_id": request_result['request_id'], }) # check result
if process_payment['status'] == "success": # show success page
    print('Ok')
else: # something went wrong
    print('Oops')