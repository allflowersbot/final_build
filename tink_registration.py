import requests


class RegInBank:
    def __init__(self, username, password):
        self.username = username  # 'username': 'AllFlowRu1'
        self.password = password  # 'password': 'AllFlowRu1'
        self.host = 'sm-register.tinkoff.ru'
        self.access_token = ""

    def auth(self):
        url = 'https://{}/oauth/token'.format(self.host)

        req = requests.post(url, auth=('partner', 'partner'),
                            data={'grant_type': 'password', 'username': self.username, 'password': self.password})
        print(req.json())
        self.access_token = req.json()['access_token']
        return req.json()

    def partner_reg(self, str_qwe):
        urlreg = 'https://{}/register'.format(self.host)

        req = requests.post(urlreg, json=str_qwe, headers={"Authorization": "Bearer " + self.access_token})
        # {'code': '700017436', 'shopCode': 700017436, 'terminals': []} correct answer
        return req.json()


str_qwe ={
    "billingDescriptor" : "IP_SHENKAO_V_M",
    "fullName" : "INDIVIDUAL_PREDPRINIMATEL_SHENKAO_VALERIY_MUHAMEDOVICH",
    "name" : "SHENKAO_VALERIY_MUHAMEDOVICH",
    "inn" : "090109397802",
    "kpp" : "000000000000", # nenado
    "okved" : "46.22",
    "ogrn" : 314774633902117,
    "addresses" : [ {
    "type" : "legal",
    "zip" : "140053",
    "country" : "RUS",
    "city" : "Moscow",
    "street" : " 1",
    "description" : ""
    },
        {
    "type" : "post",
    "zip" : "119620",
    "country" : "RUS",
    "city" : "котельники",
    "street" : "Южный мкр., дом 11, квартира 24",
    }],
    "email" : "valter81@mail.ru",
    "founders" : {
    "individuals" : [ {
    "address" : "Московская обл, Котельники г, Южный мкр., дом 11, квартира 24",
    "citizenship" : "RUSSIA",
    "firstName" : "Valeriy",
    "lastName" : "Shenkao",
    } ]
    },
    "ceo" : {
    "phone" : "8-926-642-87-77",
    "firstName" : "Valeriy",
    "lastName" : "Shenkao",
    "middleName" : "Muhamedovich",
    "birthDate" : "1981-11-05",
    },
    "siteUrl" : "http://T.me/flo_test1221bot", #nenado
    "bankAccount" : {
    "account" : "40802810700000010390",
    "bankName" : "ПАО «ПРОМСВЯЗЬБАНК» г. Москва",
    "bik" : "044525555",
    "details" : "oplata_po_dogovoru_komissii", #!!!!!!!!TODO уточнить
    "tax" : 10 #!!
    },
}

# rosana's{'code': '491801', 'shopCode': 491801, 'terminals': []}