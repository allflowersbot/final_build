from aiogram.dispatcher.filters import state
from aiogram import Bot, types
import tink_registration
from dbcm import commit_query, connect, get_query
from keyboards import tink_reg_keys, INIT_KEYBOARD
# from main import dp
from utils import States
from config import APP_ID, APP_SECRET, REDIRECT_URL, DADATA_TOKEN, BOT_TOKEN, TEST_BOT_TOKEN
bot = Bot(token=BOT_TOKEN)

async def reg_tink(shop_id: int, chat_id: int):
    print("start tink reg")
    # state = dp.current_state(user=chat_id)
    cnx = connect()
    reg = tink_registration.RegInBank("AllFlowRu1", "n2YLD8x0hd")

    cursor = cnx.cursor()
    sql = (" select * from flobot.registration_info "
           " where shop_id = {};".format(shop_id))
    cursor.execute(sql)
    curs = cursor.fetchone()

    # str_qwe = {'billingDescriptor': 'IP BORISOVA S',
    #          'fullName': 'ИП Борисова С.А.',
    #          'name': 'ИП Борисова С.А.',
    #          'inn': '371102846608',
    #          'okved': '47.76',
    #          'kpp': '000000000000',
    #          'ogrn': '320508100157982',
    #          'addresses': [{'type': 'legal',
    #                         'zip': '140005',
    #                         'country': 'RUS',
    #                         'city': 'Люберцы',
    #                         'street': 'Ул красноармейская, дом 5, квартира 6',
    #                         'description': ''},
    #                        {'type': 'post',
    #                         'zip': '140005',
    #                         'country': 'RUS',
    #                         'city': 'Москва',
    #                         'street': 'красноармейская ул, дом 5, квартира 6'}],
    #          'email': 'Flip.ag@yandex.ru',
    #          'founders':
    #              {'individuals':
    #                   [{'address':
    #                         'Московская обл, Люберцы г, красноармейская ул, дом 5, квартира 6',
    #                     'citizenship': 'Россия',
    #                     'firstName': 'Софья',
    #                     'lastName': 'Борисова'}]
    #               },
    #          'ceo':
    #              {'phone': '8-952-410-28-91',
    #               'firstName': 'Софья',
    #               'lastName': 'Борисова',
    #               'middleName': 'Андреевна',
    #               'birthDate': '2002-04-11'},
    #          'siteUrl': 'http://T.me/flo_test1221bot',
    #          'bankAccount': {'account': '40802810800001502726',
    #                          'bankName': 'АО «Тинькофф Банк»',
    #                          'bik': '044525974',
    #                          'details': 'оплата услуг предпринимателя',
    #                          'tax': 95}
    #          }
    #
    #
    # # print(сurs)
    reg.auth()

    str_qwe = {
        "billingDescriptor": curs[1][:14],
        "fullName": curs[2],
        "name": curs[3],
        "inn": curs[4],
        "kpp": "000000000000",  # nenado
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
            "birthDate": curs[21],
        },
        "siteUrl": "http://T.me/flo_test1221bot",  # nenado
        "bankAccount": {
            "account": curs[22],
            "bankName": curs[23],
            "bik": curs[24],
            "details": "оплата услуг предпринимателя",  # !!!!!!!!TODO уточнить
            "tax": 95  # !!
        },
    }
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    print(str_qwe)
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    print("\n\n")
    data = reg.partner_reg(str_qwe)
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    print(data)
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    try:
        if data['message']:
            print(data["message"])
            await bot.send_message(chat_id, data['message'] + " проверьте корректность данных и введите всё заново")

            # import dbcm
            #
            # cnx = dbcm.connect()
            # cursor = cnx.cursor()
            # cursor.execute("delete from registration_info where shop_id = {};".format(shop_id))
            # cnx.commit()
            # TODO delete * from reg_info
            return -1
    except:
        print("data without message")

    try:
        if data['errors']:
            for errors in data['errors']:
                await bot.send_message(chat_id, "введен неверно" + errors['field'])
                print("введен неверно: " + errors['field'])
                # cnx = connect()
                # cursor = cnx.cursor()
                # cursor.execute(
                #     """update registration_info set bik = NULL, bankName = NULL, banc_account = NULL where shop_id = {};""".format(
                #         shop_id))
                # cnx.commit()

                return -1
    except:
        print('data without errors')

    sql = (" update flobot.shops "
           " set tink_shop_code= %s "
           " where shop_id = %s;")

    try:
        values = (data['shopCode'], shop_id,)
        commit_query(sql, values)
        await bot.send_message(chat_id, "благодарим вас за сотрудничество", reply_markup=INIT_KEYBOARD)
        # await state.set_state(States.AFT_INIT_STATE)
    except:
        print('shop_code error')
        await bot.send_message(chat_id, "непридвиденная ошибка регистрации, обратитесь в техподдержку",
                               reply_markup=INIT_KEYBOARD)


async def fill_reg_info(i: int, text: str, shop_id: int, chat_id: int):
    print('i =', i)
    cnx = connect()
    cursor = cnx.cursor()
    cursor.execute("select * from flobot.registration_info where shop_id = {};".format(shop_id))

    desriptions = cursor.description

    if i == 7 or i == 9 or i == 14:
        print()

    query = """update flobot.registration_info 
           set {} = '{}' 
           where shop_id = {};""".format(desriptions[i][0], text, shop_id)

    print(query)
    cnx = connect()
    cursor = cnx.cursor()
    cursor.execute(query)
    cnx.commit()
    cnx.close()
    if i == 24:
        await reg_tink(shop_id, chat_id)


async def print_reg_info(i: int, chat_id: int):
    if i == 1:
        print(1)
        await bot.send_message(chat_id,
                               "Пришлите Полное наименование организации пример: \"ОБЩЕСТВО С ОГРАНИЧЕННОЙ ОТВЕТСТВЕННОСТЬЮ «НЬЮСВИК»\"",
                               reply_markup=tink_reg_keys)
    elif i == 2:
        print(2)
        await bot.send_message(chat_id, "Пришлите Сокращенное наименование организации пример: \"ООО «НЬЮСВИК»\"",
                               reply_markup=tink_reg_keys)
    elif i == 3:
        print(3)
        await bot.send_message(chat_id, "Пришлите ИНН пример: \"095109397801\"", reply_markup=tink_reg_keys)
    elif i == 4:
        print(4)
        await bot.send_message(chat_id, "Пришлите ОКВЭД пример: \"46.22\"", reply_markup=tink_reg_keys)
    elif i == 5:
        print(5)
        await bot.send_message(chat_id, "Пришлите ОГРН пример: \"314574633902111\"", reply_markup=tink_reg_keys)
    elif i == 6:
        print(6)
        await bot.send_message(chat_id, "Пришлите почтовый индекс пример: \"414045\"", reply_markup=tink_reg_keys)
    elif i == 7:
        print(7)
    elif i == 8:
        print(8)
        await bot.send_message(chat_id, "адрес регистрации организации, город: \"Москва\"", reply_markup=tink_reg_keys)
    elif i == 9:
        print(9)
    elif i == 10:
        print(10)
        await bot.send_message(chat_id, "адрес регистрации организации, улица: \"Южный мкр., дом 11, квартира 24\"",
                               reply_markup=tink_reg_keys)
    elif i == 11:
        print(11)
        await bot.send_message(chat_id, "email организации пример: \"vaster18@gmail.ru\"", reply_markup=tink_reg_keys)

    elif i == 12:
        print(12)
        await bot.send_message(chat_id,
                               "Сведения об учредителе организации, адрес прописки : \"Московская обл, Котельники г, Южный мкр., дом 22, квартира 54\"",
                               reply_markup=tink_reg_keys)
    elif i == 13:
        print(13)
        await bot.send_message(chat_id, "Сведения об учредителе организации, Имя: \"Василий\"",
                               reply_markup=tink_reg_keys)
    elif i == 14:
        print(14)
        await bot.send_message(chat_id, "Пришлите тоже строну: \"Россия\"", reply_markup=tink_reg_keys)
    elif i == 15:
        print(15)
        await bot.send_message(chat_id, "Сведения об учредителе организации, фамилия : \"Тёркин\"",
                               reply_markup=tink_reg_keys)

    elif i == 16:
        print(16)
        await bot.send_message(chat_id, "Сведения об учредителе организации, телефон : \"8-926-662-88-88\"",
                               reply_markup=tink_reg_keys)

    elif i == 17:
        print(17)
        await bot.send_message(chat_id, "Сведения об учредителе организации, имя : \"Иван\"",
                               reply_markup=tink_reg_keys)
    elif i == 18:
        print(18)
        await bot.send_message(chat_id, "Сведения об учредителе организации, фамилия : \"Иванов\"",
                               reply_markup=tink_reg_keys)

    elif i == 19:
        print(19)
        await bot.send_message(chat_id, "Сведения об учредителе организации, отчество : \"Иванович\"",
                               reply_markup=tink_reg_keys)

    elif i == 20:
        print(20)
        await bot.send_message(chat_id, "Сведения об учредителе организации, дата рождения : \"1981-11-05\"",
                               reply_markup=tink_reg_keys)

    elif i == 21:
        print(21)
        await bot.send_message(chat_id, "Расчетный счет : \"40702810302800002189\"", reply_markup=tink_reg_keys)

    elif i == 22:
        print(22)
        await bot.send_message(chat_id, "наименование банка : \"ОАО «АЛЬФА-БАНК»\"", reply_markup=tink_reg_keys)

    elif i == 23:
        print(23)
        await bot.send_message(chat_id, "БИК : \"044525593\"", reply_markup=tink_reg_keys)


async def on_back_press(id: int):
    sql = (" select shop_id from flobot.shops where manager_chat_id = '%s';")
    values = (id,)
    shop_id = get_query(sql, values)

    cnx = connect()
    cursor = cnx.cursor()
    cursor.execute("select * from flobot.registration_info where shop_id = {};".format(shop_id))

    describe = cursor.description
    reg_info = cursor.fetchone()

    print(reg_info)
    if reg_info is not None:
        for i in range(1, 25):
            print(i)
            if i == 1:
                # state = dp.current_state(user=id)
                await bot.send_message(id, "начнем заново", reply_markup=INIT_KEYBOARD)
                # await state.set_state(States.AFT_INIT_STATE)
            elif i == 7 or i == 9 or i == 14:
                print()
            elif reg_info[i] is None:
                sql = """update flobot.registration_info set {} = NULL where shop_id = {}""".format(describe[i - 1][0],
                                                                                                    shop_id)
                print(sql)
                cursor = cnx.cursor()
                cursor.execute(sql)
                cnx.commit()
                await print_reg_info(i - 2, chat_id=id)
                break
    cnx.close()
