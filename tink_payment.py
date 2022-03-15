import hashlib

import requests


class payment:
    def __init__(self, Terminalkey, TerminalPass):
        self.TerminalKey = Terminalkey
        self.TerminalPass = TerminalPass
        self.UrlPay = "https://securepay.tinkoff.ru/v2/"

        self.InitConfig = {
    "TerminalKey": Terminalkey,
    "Amount": 0,  # сумма в копейках
    "OrderId": "",  # в нашей системе
    "Shops": [],
    "Description": "букеты",
    "Receipt": {
        "Email": "allflowersbot@yandex.ru",
        "Phone": "", #телефон клиента
        # "EmailCompany": "b@test.ru",
        "Taxation": "osn",
        "Items": []
    }
}

    def init_pay(self, shops, Items, order_id):
        url = self.UrlPay + 'Init'
        Amount = 0
        for i in Items:
            Amount += int(i["Price"]) * int(i["Quantity"])
        print("Items_from_pay={}".format(Items))
        print("Amount_from_pay={}".format(Amount))
        self.InitConfig["Amount"] = Amount
        self.InitConfig["OrderId"] = order_id

        self.InitConfig["Shops"] = shops
        self.InitConfig["Receipt"]["Items"] = Items
        resp = requests.post(url, json=self.InitConfig)
        print("INIT_CONF={}".format(self.InitConfig))
        return resp.json(), Amount/100

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
        url = self.UrlPay + "Cancel"
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




    #
config = {
    "TerminalKey": "1615725763495DEMO",
    "Amount": "140000",  # сумма в копейках
    "OrderId": "1",  # в нашей системе
    "Shops": [
        {
        "ShopCode": "700017436",
        "Amount": "140000",
        "Name": "варежки"
        },
    ],
    "Description": "акции",
    "DATA": {
        "Email": "allflowersbot@yandex.ru"
    },
    "Receipt": {
        "Email": "allflowersbot@yandex.ru",
        "Phone": "+79031234567", #телефон клиента
        "EmailCompany": "allflowersbot@yandex.ru",
        "Taxation": "osn",
        "Items": [{"Name":"Наименование товара 1",
                   "Price":10000,
                   "Quantity":1.00,
                   "Amount":10000,
                   "Tax":"vat10",
                   "Ean13":"0123456789",
                   "ShopCode":"12345"},]
    }
}


# Items = [
#                   {
#                       "Name":"Наименование товара 1",
#                    "Price":10000,
#                    "Quantity":1.00,
#                    "Amount":10000,
#                    "Tax":"vat10",
#                    "Ean13":"0123456789",
#                    "ShopCode":"12345"
#                   },
#
#                   {"Name":"Наименование товара 2",
#                    "Price":20000,
#                    "Quantity":2.00,
#                    "Amount":40000,
#                    "Tax":"vat18"},
#
#                   {"Name":"Наименование товара 3",
#                    "Price":30000,"Quantity":3.00,
#                    "Amount":90000,
#                    "Tax":"vat10"}
# ]
#
# prod = {
#     "Name": "Наименование товара 1",
#     "Price": 10000,
#     "Quantity": 1.00,
#     "Amount": 10000,  # price * quantity
#     "Tax": "vat10",
#     "ShopCode": "12345"
# }
#
# prod2 = {
#     "Name": "Наименование товара 1",
#     "Price": 10000,
#     "Quantity": 1.00,
#     "Amount": 10000,  # price * quantity
#     "Tax": "vat10",
#     "ShopCode": "12345"
# }