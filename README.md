**Odoo Connector**
```elm
from OdooConnector import Connector

ROOT = 'http://localhost:1014'
USERS_URL = '/user'
INVOICE_URL = '/invoice'
ORDER_URL = '/order'

odoo = Connector(ROOT, 'email@user.com', 'password', 'db')
res = odoo.post_value(ORDER_URL, {
                    'client': {'name': 'abdo', 'email': 'abougaa@weelite.co'},
                    'products': [{'infos': {'default_code': '124','name': 'article','type': 'product', 'standard_price': 10,},
                                'qty': 1,
                                'ht_price': 100,
                                # 'ttc_price': 120,
                                'taxes': [{'name': 'tva+5', 'amount_type': 'fixed', 'amount': 5},
                                {'name': 'tva+1p', 'amount_type': 'percent', 'amount': 1}]
                                }]
                      })
```
