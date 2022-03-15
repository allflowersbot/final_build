from loader import dp, bot, auctions, ADMIN_CHAT_ID, current_products
from config import *
import re
from keyboards import MAIL, INIT_KEYBOARD, manager_mode_keys1, manager_mode_keys2, manager_mode_keys, FLOWER_KEYS
from video_instruction import mailing
from utils import States
from aiogram import types
from dbcm import connect, commit_query, get_query

# upload_here

@dp.message_handler(content_types=types.ContentTypes.PHOTO, state=States.UPLOAD1)
async def products(msg: types.Message):
    print("products")
    state = dp.current_state()
    if msg.text == "назад":
        iter = 0
        for cur_prod in current_products:
            if cur_prod['manager_chat'] == msg.chat.id:
                current_products.pop(iter)
            iter+=1
        kb = types.InlineKeyboardMarkup()
        bn1 = types.InlineKeyboardButton("добавить товар", callback_data='add_product')
        bn2 = types.InlineKeyboardButton("посмотреть список товаров", callback_data='show_product')
        bn3 = types.InlineKeyboardButton("редактировать товар", callback_data='edit_product')
        kb.add(bn1, bn3)
        kb.add(bn2)
        await bot.send_message(msg.chat.id, "что вы хотите сделать?", reply_markup=kb)
        kb1 = types.ReplyKeyboardMarkup(True, True)
        kb1.row("★ ⬆️ В начало ⬆️ ★")
        kb.row("назад")
        await bot.send_message(msg.chat.id, "для выхода нажмите на кнопку на клавиатуре ниже",
                               reply_markup=kb1)
        await state.set_state(States.manager_mode)
        return -1
    elif msg.text == "★ ⬆️ В начало ⬆️ ★":
        iter = 0
        for cur_prod in current_products:
            if cur_prod['manager_chat'] == msg.chat.id:
                current_products.pop(iter)
            iter += 1
        await bot.send_message(msg.chat.id, "начнем заново", reply_markup=INIT_KEYBOARD)
        await state.set_state(States.AFT_INIT_STATE)
        return -1
    for i in msg.photo:
        print(i)

    print(msg.photo[0].file_id)
    print(msg.text)
    print(msg.date, msg.caption)
    await bot.send_message(msg.chat.id, "photo")

    value = (msg.photo[-1].file_id, msg.caption)

    for cur_prod in current_products:
        if cur_prod['manager_chat'] == msg.chat.id:
            cur_prod['file_id'] = msg.photo[-1].file_id

    await state.set_state(States.UPLOAD5)
    print("!!")
    await bot.send_message(msg.chat.id,
                           "какое у него описание? не более 15-20 слов(255 символов)не забудьте добавить цену и время сборки букета")

@dp.message_handler(content_types=types.ContentTypes.TEXT, state=States.UPLOAD5)
async def products(msg: types.Message):
    state = dp.current_state()
    print("&&")
    if msg.text == "назад":
        kb = types.InlineKeyboardMarkup()
        bn1 = types.InlineKeyboardButton("добавить товар", callback_data='add_product')
        bn2 = types.InlineKeyboardButton("посмотреть список товаров", callback_data='show_product')
        bn3 = types.InlineKeyboardButton("редактировать товар", callback_data='edit_product')
        kb.add(bn1, bn3)
        kb.add(bn2)
        await bot.send_message(msg.chat.id, "что вы хотите сделать?", reply_markup=kb)
        kb1 = types.ReplyKeyboardMarkup(True, True)
        kb1.row("★ ⬆️ В начало ⬆️ ★")
        kb.row("назад")
        await bot.send_message(msg.chat.id, "для выхода нажмите на кнопку на клавиатуре ниже",
                               reply_markup=kb1)
        await state.set_state(States.manager_mode)
    elif msg.text == "★ ⬆️ В начало ⬆️ ★":
        await bot.send_message(msg.chat.id, "начнем заново", reply_markup=INIT_KEYBOARD)
        await state.set_state(States.AFT_INIT_STATE)
        return -1

    for cur_prod in current_products:
        if cur_prod['manager_chat'] == msg.chat.id:
            cur_prod['caption'] = (msg.text)

    await state.set_state(States.UPLOAD3)
    await bot.send_message(msg.chat.id,
                           "перечислите цветы в составе букета через запятую пример:\n\"пионы, розы \"\n не более 15-20 слов", reply_markup=FLOWER_KEYS)

@dp.message_handler(content_types=types.ContentTypes.TEXT, state=States.UPLOAD3)
async def products(msg: types.Message):
    state = dp.current_state()
    print("**")
    if msg.text == "назад":
        kb = types.InlineKeyboardMarkup()
        bn1 = types.InlineKeyboardButton("добавить товар", callback_data='add_product')
        bn2 = types.InlineKeyboardButton("посмотреть список товаров", callback_data='show_product')
        bn3 = types.InlineKeyboardButton("редактировать товар", callback_data='edit_product')
        kb.add(bn1, bn3)
        kb.add(bn2)
        await bot.send_message(msg.chat.id, "что вы хотите сделать?", reply_markup=kb)
        kb1 = types.ReplyKeyboardMarkup(True, True)
        kb1.row("★ ⬆️ В начало ⬆️ ★")
        kb.row("назад")
        await bot.send_message(msg.chat.id, "для выхода нажмите на кнопку на клавиатуре ниже",
                               reply_markup=kb1)
        await state.set_state(States.manager_mode)
    elif msg.text == "★ ⬆️ В начало ⬆️ ★":
        await bot.send_message(msg.chat.id, "начнем заново", reply_markup=INIT_KEYBOARD)
        await state.set_state(States.AFT_INIT_STATE)
        return -1

    for cur_prod in current_products:
        if cur_prod['manager_chat'] == msg.chat.id:
            cur_prod['categ'] = (msg.text)

    print("**")
    kb1 = types.ReplyKeyboardMarkup(True, True)
    kb1.row("★ ⬆️ В начало ⬆️ ★")
    await state.set_state(States.UPLOAD2)
    await bot.send_message(msg.chat.id, "цена? в рублях \"1000\"", reply_markup=kb1)

@dp.message_handler(content_types=types.ContentTypes.TEXT, state=States.UPLOAD2)
async def products(msg: types.Message):
    state = dp.current_state()
    if msg.text == "назад":
        kb = types.InlineKeyboardMarkup()
        bn1 = types.InlineKeyboardButton("добавить товар", callback_data='add_product')
        bn2 = types.InlineKeyboardButton("посмотреть список товаров", callback_data='show_product')
        bn3 = types.InlineKeyboardButton("редактировать товар", callback_data='edit_product')
        kb.add(bn1, bn3)
        kb.add(bn2)
        await bot.send_message(msg.chat.id, "что вы хотите сделать?", reply_markup=kb)
        kb1 = types.ReplyKeyboardMarkup(True, True)
        kb1.row("★ ⬆️ В начало ⬆️ ★")
        kb.row("назад")
        await bot.send_message(msg.chat.id, "для выхода нажмите на кнопку на клавиатуре ниже",
                               reply_markup=kb1)
        await state.set_state(States.manager_mode)
    elif msg.text == "★ ⬆️ В начало ⬆️ ★":
        await bot.send_message(msg.chat.id, "начнем заново", reply_markup=INIT_KEYBOARD)
        await state.set_state(States.AFT_INIT_STATE)
        return -1

    try:
        for cur_prod in current_products:
            if cur_prod['manager_chat'] == msg.chat.id:
                cur_prod['cost'] = int(msg.text)

    except:
        await bot.send_message(msg.chat.id, "цифрами, например '1000'")
        return -1
    await state.set_state(States.UPLOAD4)
    print("__")
    await bot.send_message(msg.chat.id, "название магазина?")

@dp.message_handler(content_types=types.ContentTypes.TEXT, state=States.UPLOAD4)
async def products(msg: types.Message):
    state = dp.current_state()
    print("@@")
    if msg.text == "назад":
        kb = types.InlineKeyboardMarkup()
        bn1 = types.InlineKeyboardButton("добавить товар", callback_data='add_product')
        bn2 = types.InlineKeyboardButton("посмотреть список товаров", callback_data='show_product')
        bn3 = types.InlineKeyboardButton("редактировать товар", callback_data='edit_product')
        kb.add(bn1, bn3)
        kb.add(bn2)
        await bot.send_message(msg.chat.id, "что вы хотите сделать?", reply_markup=kb)
        kb1 = types.ReplyKeyboardMarkup(True, True)
        kb1.row("★ ⬆️ В начало ⬆️ ★")
        kb.row("назад")
        await bot.send_message(msg.chat.id, "для выхода нажмите на кнопку на клавиатуре ниже",
                               reply_markup=kb1)
        await state.set_state(States.manager_mode)
    elif msg.text == "★ ⬆️ В начало ⬆️ ★":
        await bot.send_message(msg.chat.id, "начнем заново", reply_markup=INIT_KEYBOARD)
        await state.set_state(States.AFT_INIT_STATE)
        return -1
    #current_product ={}
    for cur_prod in current_products:
        if cur_prod['manager_chat'] == msg.chat.id:
            cur_prod['shop'] = msg.text
            #current_product = cur_prod

    await state.set_state(States.UPLOAD8)
    await bot.send_message(msg.chat.id,
                           "сколько по времени он будет собирраться? в минутах")

@dp.message_handler(content_types=types.ContentTypes.TEXT, state=States.UPLOAD8)
async def timeofbuild(msg: types.Message):
    state = dp.current_state()

    if msg.text == "назад":
        kb = types.InlineKeyboardMarkup()
        bn1 = types.InlineKeyboardButton("добавить товар", callback_data='add_product')
        bn2 = types.InlineKeyboardButton("посмотреть список товаров", callback_data='show_product')
        bn3 = types.InlineKeyboardButton("редактировать товар", callback_data='edit_product')
        kb.add(bn1, bn3)
        kb.add(bn2)
        await bot.send_message(msg.chat.id, "что вы хотите сделать?", reply_markup=kb)
        kb1 = types.ReplyKeyboardMarkup(True, True)
        kb1.row("★ ⬆️ В начало ⬆️ ★")
        kb.row("назад")
        await bot.send_message(msg.chat.id, "для выхода нажмите на кнопку на клавиатуре ниже",
                               reply_markup=kb1)
        await state.set_state(States.manager_mode)
    elif msg.text == "★ ⬆️ В начало ⬆️ ★":
        await bot.send_message(msg.chat.id, "начнем заново", reply_markup=INIT_KEYBOARD)
        await state.set_state(States.AFT_INIT_STATE)
        return -1
    try:

        for cur_prod in current_products:
            if cur_prod['manager_chat'] == msg.chat.id:
                cur_prod['time'] = int(msg.text)

    except:
        await bot.send_message(msg.chat.id, "цифрой, например 20")
        return -1
    #
    # sql = ("select shop_id from shops where manager_chat_id = %s;")
    # value = (msg.chat.id,)
    # shop_id = get_query(sql, value)
    #
    # sql = (" update flobot.products set "
    #        "timeofbuild = '%s' "
    #        " where file_id = %s")
    # value = (current_product['time'], current_product['file_id'])
    # commit_query(sql, value)
    await state.set_state(States.UPLOAD6)
    await bot.send_message(msg.chat.id,
                           "до какого числа? в формате YYYY-MM-DD\nв случае если букет выставлен "
                           "надолго - напишите \"Нет\", с большой буквы.")

@dp.message_handler(content_types=types.ContentTypes.TEXT, state=States.UPLOAD6)
async def products(msg: types.Message):
    print("^^")
    state = dp.current_state()
    if msg.text == "назад":
        kb = types.InlineKeyboardMarkup()
        bn1 = types.InlineKeyboardButton("добавить товар", callback_data='add_product')
        bn2 = types.InlineKeyboardButton("посмотреть список товаров", callback_data='show_product')
        bn3 = types.InlineKeyboardButton("редактировать товар", callback_data='edit_product')
        kb.add(bn1, bn3)
        kb.add(bn2)
        await bot.send_message(msg.chat.id, "что вы хотите сделать?", reply_markup=kb)
        kb1 = types.ReplyKeyboardMarkup(True, True)
        kb1.row("★ ⬆️ В начало ⬆️ ★")
        kb.row("назад")
        await bot.send_message(msg.chat.id, "для выхода нажмите на кнопку на клавиатуре ниже",
                               reply_markup=kb1)
        await state.set_state(States.manager_mode)
        return -1
    elif msg.text == "★ ⬆️ В начало ⬆️ ★":
        await bot.send_message(msg.chat.id, "начнем заново", reply_markup=INIT_KEYBOARD)
        await state.set_state(States.AFT_INIT_STATE)
        return -1

    if msg.text.lower() != 'нет':
        # sql = (" update flobot.products set "
        #        "inspired_in = %s "
        #        " where file_id = %s")
        # value = (msg.text, current_product['file_id'],)
        try:
            for cur_prod in current_products:
                if cur_prod['manager_chat'] == msg.chat.id:
                    cur_prod['inspired_in'] = msg.text

            #commit_query(sql, value)
        except:
            await bot.send_message(msg.chat.id, "введите дату корректно в формате YYYY-MM-DD или 'Нет'")
            return -1
    current_product = {}
    i = 0
    for cur_prod in current_products:
        if cur_prod['manager_chat'] == msg.chat.id:
            current_product = cur_prod
            break
        i+=1

    print(current_product)
    if current_product['sale'] == 'sale':

        cnx = connect()

        curs = cnx.cursor()

        sql = ("SELECT id FROM successful_payment ORDER BY id DESC LIMIT 1")
        curs.execute(sql)
        id_ins = curs.fetchone()
        id_insert = id_ins[0]
        print(id_insert, "test id insert")


        config = {
            "TerminalKey": "1615725763495",
            "Amount": "5000",  # сумма в копейках
            "OrderId": id_insert+1,  # в нашей системе
            "Shops": [
                {
                    "ShopCode": "492585",
                    "Amount": "5000",
                    "Name": "варежки"
                },
            ],
            "Description": "акции",
            "DATA": {
                "Email": "allflowersbot@yandex.ru"
            },
            "Receipt": {
                "Email": "allflowersbot@yandex.ru",
                "Phone": "+79031234567",  # телефон клиента
                "EmailCompany": "allflowersbot@yandex.ru",
                "Taxation": "osn",
                "Items": [{"Name": "акции",
                           "Price": 5000,
                           "Quantity": 1.00,
                           "Amount": 5000,
                           "Tax": "vat10",
                           "Ean13": "0123456789",
                           "ShopCode": "492585"}, ]
            }
        }

        import requests

        resp = requests.post('https://rest-api-test.tinkoff.ru/v2/Init/', json=config)
        print(resp.json())
        confirmation_url = resp.json()['PaymentURL']

        sql = (" select shop_id from flobot.managers where manager_chat_id = '%s';")
        values = (msg.chat.id,)
        sh_id = get_query(sql, values)

        sql = ("insert into successful_payment(provider_payment_charge_id, caption, cost, client_id, shop_id) values(%s, %s, %s, %s, %s); ")
        val = (resp.json()['PaymentId'], "акционный товар", 50, msg.chat.id, sh_id,)
        cnx = connect()

        cur = cnx.cursor()

        cur.execute(sql, val)

        cnx.commit()

        cnx.close()

        kb = types.InlineKeyboardMarkup()
        bn = types.InlineKeyboardButton("pay", url=confirmation_url)

        kb.add(bn)
        await bot.send_message(msg.chat.id, "чтобы ваш продукт появился как акционный оплатите по кнопке ниже",
                               reply_markup=kb)
    sql = (" select shop_id from flobot.managers where manager_chat_id = '%s';")
    values = (msg.chat.id,)
    shop_id = get_query(sql, values)

    if current_product['inspired_in'] == "нет":
        sql = (
            "insert into products(file_id, caption, categories, cost, shop, shop_id, timeofbuild, sale) values(%s, %s, %s, %s, %s, %s, %s, %s); ")
        values = (current_product['file_id'], current_product['caption'], current_product['categ'], current_product['cost'],
              current_product['shop'], shop_id, current_product['time'], current_product["sale"],)
    else:
        sql = (
        "insert into products(file_id, caption, categories, cost, shop, shop_id, inspired_in, timeofbuild, sale) values(%s, %s, %s, %s, %s, %s, %s, %s, %s); ")
        values = (current_product['file_id'], current_product['caption'], current_product['categ'], current_product['cost'],
              current_product['shop'], shop_id, current_product['inspired_in'], current_product['time'], current_product["sale"],)

    cnx = connect()

    cur = cnx.cursor()

    cur.execute(sql, values)

    cnx.commit()

    cnx.close()
    print(current_products)
    current_products.pop(i)

    current_prod = {
        'manager_chat': msg.chat.id,
        'sale': "NULL",
        'file_id': "",
        'caption': "",
        'categ': "",
        'cost': 0,
        'shop': "",
        'time': 0,
        'inspired_in': "нет"
    }
    current_products.append(current_prod)

    await bot.send_message(msg.chat.id, "ваш продукт добавлен, чтобы добавить еще один - сначала пришлите фото")
    await state.set_state(States.UPLOAD1)