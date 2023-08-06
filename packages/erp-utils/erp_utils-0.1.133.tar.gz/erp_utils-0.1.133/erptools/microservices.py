import json
import os
from datetime import datetime

import boto3
import requests
from cryptography.fernet import Fernet


class ApiCalls:
    fernet = Fernet(bytes(os.environ.get('API_TOKEN_KEY'), encoding='utf-8'))

    def __init__(self, url):
        self.url = url.strip('/')
        self.endpoints = {}

    def encrypt(self, message):
        b_message = json.dumps(message).encode()
        return self.fernet.encrypt(b_message)

    def decrypt(self, enc):
        d = self.fernet.decrypt(enc)
        data = json.loads(d)
        data['creation_time'] = datetime.fromtimestamp(self.fernet.extract_timestamp(enc)).strftime(
            "%m/%d/%Y, %H:%M:%S")
        return data

    def format_query(self, queries=None):
        if queries is None:
            queries = []
        query = ''
        # make sure that all tuple pairs are strings
        queries = map(lambda x: (str(x[0]), str(x[1])), queries)
        # combine pairs in 'x=y' format
        pairs = map(lambda x: '='.join(x), queries)
        if queries:
            query = f"?{'&'.join(pairs)}"
        return query

    def endpoint(self, suffix, query=None):
        if query is None:
            query = []
        return '/'.join((self.url, suffix)).strip('/') + '/'

    def put_request(self, basename, url_suffix, data):
        message = {'views': {basename: 'PUT'}}
        r = requests.put(self.endpoint(url_suffix), data=data, headers={
            'token': self.encrypt(message)})
        return r.content, r.status_code

    def post_request(self, basename, url_suffix, data):
        message = {'views': {basename: 'POST'}}
        r = requests.post(self.endpoint(url_suffix), json=data, headers={
            'token': self.encrypt(message)})
        if str(r.status_code)[0] == '2':
            return json.loads(r.content), r.status_code
        else:
            return {"failed": r.content}, r.status_code

    def get_request(self, basename, url_suffix, query=None):
        if query is None:
            query = []
        message = {'views': {basename: 'GET'}}
        r = requests.get(self.endpoint(url_suffix, query), params=dict(query), headers={'token': self.encrypt(message)})
        try:
            return json.loads(r.content), r.status_code
        except:
            return r.content, r.status_code

    def delete_request(self, basename, url_suffix):
        message = {'views': {basename: 'DELETE'}}
        r = requests.delete(self.endpoint(url_suffix), headers={'token': self.encrypt(message)})
        try:
            return json.loads(r.content), r.status_code
        except:
            return r.content, r.status_code

    def list(self, route, query=None):
        if query is None:
            query = []
        url_info = self.endpoints[route]
        return self.get_request(url_info['basename'], url_info['route'], query)

    def destroy(self, route, pk):
        url_info = self.endpoints[route]
        return self.delete_request(url_info['basename'], f"{url_info['route']}/{pk}/")

    def read(self, route, pk):
        url_info = self.endpoints[route]
        return self.get_request(url_info['basename'], f"{url_info['route']}/{pk}/")

    def create(self, route, data):
        url_info = self.endpoints[route]
        return self.post_request(url_info['basename'], url_info['route'], data)

    def update(self, route, pk, data):
        url_info = self.endpoints[route]
        return self.put_request(url_info['basename'], f"{url_info['route']}/{pk}/", data)


class ShippingApi(ApiCalls):
    url = os.environ.get('SHIPMENT_API').strip('/')

    def __init__(self):
        ApiCalls.__init__(self, ShippingApi.url)
        self.endpoints = {
            'countries': {'basename': 'countries', 'route': 'countries'},
            'provinces': {'basename': 'provinces', 'route': 'provinces'},
            'shippingaddress': {'basename': 'shippingaddress', 'route': 'shippingaddress'},
            'shippingzones': {'basename': 'shippingzones', 'route': 'shippingzones'},
            'accessmethod': {'basename': 'accessmethod', 'route': 'accessmethod'},
            'shippingquestionnaire': {'basename': 'shippingquestionnaire', 'route': 'shippingquestionnaire'},
            'shipment': {'basename': 'shipment', 'route': 'shipment'},
            'flatrate': {'basename': 'flatrate', 'route': 'flatrate'},
            'shipmentcontact': {'basename': 'shipmentcontact', 'route': 'shipmentcontact'},
            'changeonconvert': {'basename': 'changeonconvert', 'route': 'changeonconvert'},
            'delivery_questionnaire': {'basename': 'shipment', 'route': 'shipment/project_email_questionnaire'},
            'shipment_info': {'basename': 'shipment', 'route': 'shipment/project_price'},
            'shipping_bulk_price': {'basename': 'shipment', 'route': 'shipment/bulk_price'},
            'installer-booking': {'basename': 'installerbooking', 'route': 'installer-booking'},
            'installer-booking-projects': {'basename': 'installerbooking', 'route': 'installer-booking/byproject'},
            'context': {'basename': 'context', 'route': 'context'},
        }


class AccountingApi(ApiCalls):
    url = os.environ.get('ACCOUNTING_API').strip('/')

    def __init__(self):
        ApiCalls.__init__(self, AccountingApi.url)
        self.endpoints = {
            'items': {'basename': 'item', 'route': 'items'},
            'sync-map': {'basename': 'syncmap', 'route': 'sync-map'}
        }


class ProductsApi(ApiCalls):
    url = os.environ.get('PRODUCTS_API').strip('/')

    def __init__(self):
        ApiCalls.__init__(self, ProductsApi.url)
        self.endpoints = {
            'products': {'basename': 'products', 'route': 'products'},
            'category': {'basename': 'category', 'route': 'category'},
            'manufacturer': {'basename': 'manufacturer', 'route': 'manufacturer'},
            'option': {'basename': 'option', 'route': 'option'},
            'option_group': {'basename': 'option_group', 'route': 'option_group'},
            'property_setting': {'basename': 'property_setting', 'route': 'property_setting'},
            'validate_order': {'basename': 'products', 'route': 'validate_order'},
            'category_options': {'basename': 'category', 'route': 'category/options'},
            'context': {'basename': 'context', 'route': 'context'},
            'parts': {'basename': 'parts', 'route': 'parts'},
        }


class TransactionsApi(ApiCalls):
    url = os.environ.get('TRANSACTIONS_API').strip('/')

    def __init__(self):
        ApiCalls.__init__(self, TransactionsApi.url)
        self.endpoints = {
            'invoice': {'basename': 'invoice', 'route': 'invoice'},
            'context': {'basename': 'context', 'route': 'context'},
            'extra_charges': {'basename': 'extra_charges', 'route': 'extra-charges/sync'},
        }


class CncApi(ApiCalls):
    url = os.environ.get('MATERIALS_API').strip('/')

    def __init__(self):
        ApiCalls.__init__(self, CncApi.url)
        self.endpoints = {
            'source-list': {'basename': 'cutlist', 'route': 'cutlist/source-list'},

        }


class OrdersApi(ApiCalls):
    url = os.environ.get('ORDERS_API').strip('/')

    def __init__(self):
        ApiCalls.__init__(self, OrdersApi.url)
        self.endpoints = {
            'projects': {'basename': 'projects', 'route': 'projects'},
            'project_orders': {'basename': 'projects_orders', 'route': 'projects/order_num'},
            'cnc-order': {'basename': 'cnc-order', 'route': 'cnc-order'},
            'context': {'basename': 'context', 'route': 'context'},
        }


def authenticate_and_get_token(username: str, password: str) -> str:
    client = boto3.client('cognito-idp')
    user_pool_id = os.environ.get('COGNITO_USER_POOL', '')
    app_client_id = os.environ.get('COGNITO_AUDIENCE', '')
    resp = client.admin_initiate_auth(
        UserPoolId=user_pool_id,
        ClientId=app_client_id,
        AuthFlow='ADMIN_NO_SRP_AUTH',
        AuthParameters={
            "USERNAME": username,
            "PASSWORD": password
        }
    )
    return f"Bearer {resp['AuthenticationResult']['IdToken']}"
