from . import __version__
import json
import requests


class Connector:

    def __init__(self, url: str, login: str, password: str, db: str):
        print("Odoo Connector Version: {}".format(__version__))
        self._url = url
        self._login = login
        self._password = password
        self._db = db
        self._cookies: dict = {}
        self._HEADER = {'Content-type': 'application/json'}

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

    def post_value(self, url, dt):
        cnx = requests.post(
            url=self._url + url,
            headers=self._HEADER,
            data=json.dumps({'params': dt}),
            cookies=self._connect()
        ).text
        if json.loads(cnx).get('error', {'code': False})['code'] == 100:
            self._cookies = {}
            cnx = requests.post(
                url=self._url + url,
                headers=self._HEADER,
                data=json.dumps({'params': dt}),
                cookies=self._connect()
            ).text
        return cnx
