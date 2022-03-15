from dbcm import *
import tink_registration
from aiogram import Bot, types
import tink_registration
from dbcm import commit_query, connect, get_query
from keyboards import tink_reg_keys, INIT_KEYBOARD
from config import BOT_TOKEN

# bot = Bot(token=BOT_TOKEN)

new_shop_codes = {
    '7': "528733",
    '34': "528740",
    '35': "528742",
    '37': "528744",
    '40': "528745",
    '43': "528746",
    '44': "528747",
    '46': "528752",
    '47': "528753",
    '48': "528754",
    '51': "528755",
    '52': "528757",
    '53': "528759",
    '56': "528760",
    '61': "528761",
    '71': "528762"
}


def func(shop_id):
        print("start")
        reg = tink_registration.RegInBank("AllFlowRu1", "n2YLD8x0hd")

        cnx = connect()
        cursor = cnx.cursor()
        sql = (" select * from flobot.registration_info "
               " where shop_id = {};".format(shop_id))
        cursor.execute(sql)
        curs = cursor.fetchone()
        reg.auth()
        if curs is None:
            print("{} :no data".format(shop_id))
            return -1
        try:
            str_qwe = {
            "billingDescriptor": curs[1][:14],
            "fullName": curs[2],
            "name": curs[3],
            "inn": curs[4],
            "kpp": "000000000000",  # `nenado
            "okved": curs[5],
            "ogrn": curs[6],
            "addresses": [{
                "type": "legal",
                "zip": curs[8],
                "country": "RUS",
                "city": curs[10],
                "street": curs[11],
                "description": ""
            },
                {
                    "type": "post",
                    "zip": curs[8],
                    "country": "RUS",
                    "city": curs[10],
                    "street": curs[11],
                }],
            "email": curs[12],
            "founders": {
                "individuals": [{
                    "address": curs[13],
                    "citizenship": "Россия",
                    "firstName": curs[15],
                    "lastName": curs[16],
                }]
            },
            "ceo": {
                "phone": curs[17],
                "firstName": curs[18],
                "lastName": curs[19],
                "middleName": curs[20],
                "birthDate": curs[21],  #
            },
            "siteUrl": "http://T.me/flo_test1221bot",  # nenado
            "bankAccount": {
                "account": curs[22],
                "bankName": curs[23],
                "bik": curs[24],
                "details": "оплата услуг предпринимателя",  # !!!!!!!!TODO уточнить
                "tax": 10  # !!
            },
        }
        except:
            print("smth gonna wrong")
            return -1

        data = reg.partner_reg(str_qwe)
        print("= = = = = = = = = = ")
        print(data)
        print("= = = = = = = = = = ")
        try:
            if data['message']:
                print(data["message"])
                # TODO delete * from reg_info
                return -1
        except:
            print("data without message")

        try:
            if data['errors']:
                for errors in data['errors']:
                    error_str = "введен неверно: " + errors['field']
                    print("введен неверно: " + errors['field'])
                    print("'{}': {}".format(shop_id, errors['field']))

                    return -1
        except:
            print('data without errors')

        # sql = (" update flobot.shops "
        #        " set tink_shop_code= %s "
        #        " where shop_id = %s;")

        try:
            # values = (data['shopCode'], shop_id,)
            print("'shop_id': tink_shop_code")
            print("'{}': \"{}\",".format(shop_id, data['shopCode']))
            # commit_query(sql, values)
        except:
            print('shop_code error')


def easy():
    for key in new_shop_codes:
        print(key, ' :', new_shop_codes[key])
        sql = (" update flobot.shops "
               " set tink_shop_code= %s "
               " where shop_id = %s;")
        values = (new_shop_codes[key], key,)
        commit_query(sql, values)


def main_foo():
    cnx = connect()
    cursor = cnx.cursor()
    cursor.execute("select count(*), shop_id from products where cost is null group by shop_id;")
    shops = cursor.fetchall()
    for curr in shops:
        cnx = connect()
        cursor = cnx.cursor()
        cursor.execute("select shop_name from shops where shop_id = {};".format(curr[1]))
        shops = cursor.fetchone()
        print(shops)

def analog():
    shop_id = 80
    func(shop_id)
    # easy()

analog()

