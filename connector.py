from . import __version__
import json
import requests


def cookies(func):
    def inner(*args, **kwargs):
        r = func(*args, **kwargs)
        if json.loads(r).get('error', {'code': False})['code'] == 100:
            args[0]._cookies = {}
            return func(*args, **kwargs)
        return r
    return inner


class Connector:

    def __init__(self, url: str, login: str, password: str, db: str):
        print("Odoo Connector Version: {}".format(__version__))
        self._url = url
        self._login = login
        self._password = password
        self._db = db
        self._cookies: dict = {'session_id': '28befa61980463f9d51acb9e22c5ab6c87fbeda0d'}
        self._HEADER = {'Content-type': 'application/json'}
        print("Model Odoo Version: {}".format(self.get('/odoo-connector-v')))

    def _auth(self):
        req = requests.post(
            self._url + '/auth/',
            data=json.dumps({
                'params': {
                    'login': self._login,
                    'password': self._password,
                    'db': self._db
                }
            }),
            headers=self._HEADER
        )
        if not json.loads(req.text).get('result', False):
            return False
        return dict(req.cookies)

    def _connect(self):
        if not self._cookies.get('session_id', False):
            self._cookies = self._auth()
            if not self._cookies:
                raise Exception('Error cnx')
        return self._cookies

    @cookies
    def post(self, url, dt):
        cnx = requests.post(
            url=self._url + url,
            headers=self._HEADER,
            data=json.dumps({'params': dt}),
            cookies=self._connect()
        ).text
        return cnx

    def get(self, url):
        cnx = requests.get(self._url + url)
        if cnx.status_code == 200:
            return cnx.text
        else:
            print(cnx.status_code)
            return False
