import hashlib

import requests


class payment:
    def __init__(self, Terminalkey, TerminalPass):
        self.TerminalKey = Terminalkey
        self.TerminalPass = TerminalPass
        self.UrlPay = "https://rest-api-test.tinkoff.ru/v2/"

        self.InitConfig = {
    "TerminalKey": Terminalkey,
    "Amount": "",  # сумма в копейках
    "OrderId": "",  # в нашей системе
    "Description": "букеты",
    "DATA": {
        "Phone": "+78005553535",
        "Email": "a@test.com"
        },
    "Receipt": {
        "Email": "allflowersbot@yandex.ru",
        "Phone": "", #телефон клиента
        # "EmailCompany": "b@test.ru",
        "Taxation": "osn",
        "Items": []
    }
}


    def init_pay(self, Items, order_id):
        url = self.UrlPay + 'Init/'
        Amount = 0
        for i in Items:
            Amount += i["Price"] * i["Quantity"]

        self.InitConfig["Amount"] = Amount
        self.InitConfig["OrderId"] = order_id
        self.InitConfig["Receipt"]["Items"] = Items

        resp = requests.post(url, json=self.InitConfig)
        return resp.json()

    def get_state(self, payment_id):
        url = self.UrlPay + "GetState/"
        hash_param = {
            "Password": self.TerminalPass,
            "PaymentId": str(payment_id),
            "TerminalKey": self.TerminalKey
        }
        hash_str = hash_param['Password'] + hash_param['PaymentId'] + hash_param['TerminalKey']
        print(hash_str)
        token = hashlib.sha256(hash_str.encode())
        print(token.hexdigest())
        req_param = {
            "TerminalKey": self.TerminalKey,
            "PaymentId": payment_id,
            "Token": token.hexdigest()
        }
        resp = requests.post(url, json=req_param)
        return resp.json()

    def cancel(self, payment_id):
        url = self.UrlPay + "Cancel/"
        hash_param = {
            "Password": self.TerminalPass,
            "PaymentId": str(payment_id),
            "TerminalKey": self.TerminalKey
        }
        hash_str = hash_param['Password'] + hash_param['PaymentId'] + hash_param['TerminalKey']
        print(hash_str)
        token = hashlib.sha256(hash_str.encode())
        print(token.hexdigest())
        req_param = {
            "TerminalKey": self.TerminalKey,
            "PaymentId": payment_id,
            "Token": token.hexdigest()
        }
        resp = requests.post(url, json=req_param)
        return resp.json()






data = {"TerminalKey":"TinkoffBankTest",
        "Amount":"140000",
        "OrderId":"21050",
        "Description":"Подарочная карта на 1000 рублей",
        "Token":"871199b37f207f0c4f721a37cdcc71dfcea880b4a4b85e3cf852c5dc1e99a8d6",
        "DATA":{
            "Phone":"+71234567890",
            "Email":"a@test.com"
                },
        "Receipt": {
                "Email":"a@test.ru",
                "Phone":"+79031234567",
                "Taxation":"osn",
                "Items": [
                            {
                                "Name":"Наименование товара 1",
                                "Price":10000,
                                "Quantity":1.00,
                                "Amount":10000,
                                "Tax":"vat10",
                                "Ean13":"0123456789",
                                "ShopCode":"12345"
                            },
                            {
                                "Name":"Наименование товара 2",
                                "Price":20000,
                                "Quantity":2.00,
                                "Amount":40000,
                                "Tax":"vat18"
                            },
                            {
                                "Name":"Наименование товара 3",
                                "Price":30000,
                                "Quantity":3.00,
                                "Amount":90000,
                                "Tax":"vat10"
                            }
                    ]
            }
        }