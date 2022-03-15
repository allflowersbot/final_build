from math import *

from datetime import datetime
import config
import asyncio
import re
from handlers.reg_shop import regshop
from async_auction import auction
from utils import States
from messages import MESSAGES
from aiogram import types
from aiogram.utils import executor
from aiogram.dispatcher import FSMContext
from aiogram.types.message import ContentType
from keyboards import INIT_KEYBOARD, TO_ME, KEYBOARD3, COST, FLOWER_KEYS, button_phone, regex_dict, TMP, \
    REP_KEY_WHEN_INLINE, manager_mode_keys, manager_mode_edit_keys, manager_mode_keys2, manager_mode_keys1
from config import DADATA_TOKEN
from dbcm import commit_query, get_query, connect, get_query_all
from video_instruction import send_video_instruction, bot_videos
from loader import ADMIN_CHAT_ID, bot, instagram_basic_display, array, auctions, current_products
# init
from handlers import dp

def init(dp):
    print("nachalo")



@dp.callback_query_handler(lambda c: c.data == 'fast_search', state=States.GEO_PROVE)
async def fast_search(callback_query: types.CallbackQuery):
    state = dp.current_state(user=callback_query.from_user.id)
    user_id = callback_query.from_user.id
    await bot.send_message(user_id, "выберите категорию цветов")
    state.set_state(States.FAST_SEARCH)
    # searching shops
    current_addr = get_query("select order_shipping_adress from orders where client_order_id = '%s'", (user_id,))

    lon = 0.0
    lat = 0.0
    from dadata import DadataAsync
    token = DADATA_TOKEN
    secret = config.DADATA_SECRET
    dadata = DadataAsync(token)
    result = await dadata.suggest("address", current_addr)
    await dadata.close()
    if not result:
        await bot.send_message(user_id, "сервис поддерживает адреса только из России, введите адрес корректно")
        await  state.set_state(States.TO_ME_ST)
        return -1

    for row in result:
        value = row['value']
        current_value = value
        dadata = DadataAsync(token, secret)
        try:
            result = await dadata.clean("address", current_value)
        except:
            await bot.send_message(user_id,
                                   "наблюдаются проблемы с сервисом определения адресов, повторите попытку позже")
            print("наблюдаются проблемы с сервисом определения адресов, повторите попытку позже")
            await bot.send_message(ADMIN_CHAT_ID,
                                   "наблюдаются проблемы с сервисом определения адресов dadata адрес: " + current_value)
            return -1
        lon = result['geo_lon']
        lat = result['geo_lat']
        await dadata.close()
        break

    cnx = connect()
    cursor = cnx.cursor()
    sqlin = (
        "select flobot.shop_addr.*, flobot.shops.shop_name from flobot.shop_addr left join flobot.shops on "
        "flobot.shops.shop_id = flobot.shop_addr.shop_id where flobot.shops.is_open = 'yes' and flobot.shops.tink_shop_code is not null;")
    id_of_min = 10000
    d_min = 1000000.
    cursor.execute(sqlin)

    tmp_keys = types.ReplyKeyboardMarkup(True, True)

    iterator = 0

    dict_of_shops = {}

    for row in cursor:
        print(lon, lat)
        lon1 = float(lon) * pi / 180
        lat1 = float(lat) * pi / 180

        lon2 = float(row[3]) * pi / 180
        lat2 = float(row[4]) * pi / 180
        d = 2. * 6371 * asin(sqrt(
            sin((lat2 - lat1) / 2) * sin((lat2 - lat1) / 2) + cos(lat1) * cos(lat2) * sin((lon2 - lon1) / 2) * sin(
                (lon2 - lon1) / 2)))
        idstr = float(d)
        # dstr = str(idstr)

        dict_of_shops.update({row[0]: idstr})  # with addr_id
    cnx.close()
    sort_dict = {}
    sort_keys = sorted(dict_of_shops, key=dict_of_shops.get)
    print(sort_keys)

    for w in sort_keys:
        sort_dict[w] = dict_of_shops[w]
        print("!")
    print(sort_dict, "dict_of_shops")
    cnx.close()
    shop_list = []
    iter = 5
    for i, v in sort_dict.items():
        if iter == 0:
            break
        print(i, v)
        shop_list.append(i)
        iter -= 1
    print(shop_list)
    # =======
    id = user_id

    shop_id = id_of_min
    list_of_shop = []

    for addr_id in shop_list:
        rw = get_query_all("select shop_id, addr from shop_addr where addr_id = %s;", (addr_id,))
        shop_id = (rw[0]).__str__()
        list_of_shop.append(shop_id)
        print(shop_id, "вот они наши id")


    print(list_of_shop, "list of shop")

    key_dict = {}
    for shop_id in list_of_shop:
        regex_dict
        print(shop_id, "shop_id")
        cnx = connect()
        curs = cnx.cursor()
        cost = 4000
        curs.execute("select categories from products where shop_id = %s and cost < 4000;", (shop_id,))
        products = curs.fetchall()
        # print(products, "@")
        for row in products:
            srstr = row[0]
            # print(row[0], "!!")
            for key in regex_dict:
                # print(regex_dict[key], "regex_dict[key]")
                # print(key), "key"
                # # print(key, "key")
                try:
                    res = re.search(regex_dict[key], srstr)
                except:
                    continue

                if res is not None and len(res[0]) > 1:
                    # print(key_dict[key])
                    try:
                        key_dict[key] += 1
                    except:
                        print("key_dict.update({key")
                        key_dict.update({key: 1})
                        print(res[0], "@$#")
        print(key_dict)
        keys = types.ReplyKeyboardMarkup(True, True)
        max = 15
        iter = 1
        btns = []
        j = 0
        for key in key_dict:
            znach = key_dict[key]
            stroka1 = key + ' ' + znach.__str__()
            btn = stroka1
            btns.append(btn)
            keys.row(btn)
            j += 1

        print(btns)
        tuple(btns)
        # print("tut")
        if j == 0:
            await bot.send_message(user_id,
                                   "🔥💐похоже, у магазина нет букетов в этом ценовом диапозоне, выберите другой",
                                   reply_markup=COST)
            return -1
        keys.row("☆ ↩️ Назад ↩️ ☆")
        # keys.row("к магазинам")
    await state.set_state(States.FAST_SEARCH_CATALOG)
    await state.update_data(list_of_shop = list_of_shop)
    await bot.send_message(user_id,
                               "🔥💐Отлично,выберите нужный цветок",
                               reply_markup=keys)



@dp.message_handler(state='*', commands=['send_video'])  # @dp.message_handler(state=States.NS3) #todo bad
async def send_video(msg: types.Message):
    state = dp.current_state(user=msg.chat.id)
    print("rere")
    # cnx = connect()
    # cursor = cnx.cursor()
    # sql = ("select shop_name, access_token, shop_id, manager_chat_id from flobot.shops;")
    # cursor.execute(sql)  # todo требует проверки state!
    # curs = cursor.fetchall()
    start = open('videos/IMG_9722.MOV', 'rb')
    msg = await bot.send_video(msg.chat.id, start)
    print('start', msg.video.file_id)
    # addr = open('videos/IMG_9724.MOV', 'rb')
    # cost = open('videos/IMG_9726.MOV', 'rb')
    # flowers = open('videos/IMG_9728.MOV', 'rb')
    # correct_data = open('videos/IMG_9730.MOV', 'rb')
    # delivery = open('videos/IMG_9734.MOV', 'rb')
    # phone = open('videos/IMG_9739.MOV', 'rb')
    # main_menu = open('videos/IMG_9742.MOV', 'rb')
    # ordering = open('videos/IMG_9745.MOV', 'rb')
    # confirmed = open('videos/IMG_9753.MOV', 'rb')
    # add_flowers = open('videos/IMG_9754.MOV', 'rb')

    # msg = await bot.send_video(msg.chat.id, addr)
    # print('addr', msg.video.file_id)
    #
    # msg = await bot.send_video(msg.chat.id, cost)
    # print('cost', msg.video.file_id)
    #
    # msg = await bot.send_video(msg.chat.id, flowers)
    # print('flowers', msg.video.file_id)
    #
    # msg = await bot.send_video(msg.chat.id, correct_data)
    # print('correct_data', msg.video.file_id)
    #
    # msg = await bot.send_video(msg.chat.id, delivery)
    # print('delivery', msg.video.file_id)
    #
    # msg = await bot.send_video(msg.chat.id, phone)
    # print('phone', msg.video.file_id)
    #
    # msg = await bot.send_video(msg.chat.id, main_menu)
    # print('main_menu', msg.video.file_id)
    #
    # msg = await bot.send_video(msg.chat.id, ordering)
    # print('ordering', msg.video.file_id)
    #
    # msg = await bot.send_video(msg.chat.id, confirmed)
    # print('confirmed', msg.video.file_id)
    #
    # msg = await bot.send_video(msg.chat.id, add_flowers)
    # print('add_flowers', msg.video.file_id)


# current_product = {
#     'manager_chat': 0,
#     'sale': "",
#     'file_id': "",
#     'caption': "",
#     'categ': "",
#     'cost': 0,
#     'shop': "",
#     'time': 0
# }






@dp.callback_query_handler(lambda c: c.data == 'invoice', state='*')
async def process_callback_add(callback_query: types.CallbackQuery):
    print("invoice")
    await bot.answer_callback_query(callback_query.id, "invoice")
    flag = True
    str1 = callback_query["message"]["text"]

    i = str1.find("заказа")
    j = str1.find("!")
    id = str1[i + 7:j]
    print(id)
    cnx = connect()

    cursor = cnx.cursor()

    sql = ("select provider_payment_charge_id from flobot.successful_payment where id = '%s';")
    cursor.execute(sql, (int(id),))
    row = cursor.fetchone()

    payment_id = row[0]

    print(callback_query)
    from tink_payment import payment

    pay = payment("1615725763495", "2illo2v6pxz3brce")
    resp = pay.get_state(payment_id)

    print(resp, payment_id, "!!!!!")
    await bot.send_message(callback_query.from_user.id, "статус оплаты: " + resp["Status"])
    print(resp)
    r = "CONFIRMED"
    if resp["Status"] == "CONFIRMED":  # resp["Status"] == "CONFIRMED":

        sql = "select confirmed from orders where client_order_id = {}".format(callback_query.from_user.id)
        cnx = connect()
        curs = cnx.cursor()
        curs.execute(sql)
        info = curs.fetchone()
        print(info)
        if info[0] is None:
            print('vid')
            # vid = test_bot_videos[state]
            vid = bot_videos['confirmed']
            await bot.send_video(callback_query.from_user.id, vid)

        commit_query("update orders set ordering = 'yes' where client_order_id = %s", (callback_query.from_user.id,))

        sql = (" update flobot.successful_payment "
               "set status = %s where successful_payment.id =%s;")
        value = ("CONFIRMED", int(id))
        commit_query(sql, value)

        sql = ("delete from flobot.cart where client_id = '%s'")
        value = (callback_query.from_user.id,)
        commit_query(sql, value)

        st = types.InlineKeyboardMarkup()
        bn = types.InlineKeyboardButton("проблемы при пользовании", callback_data="helper")
        bn1 = types.InlineKeyboardButton("статус оплаты", callback_data="payment_status")
        st.add(bn, bn1)
        await bot.send_message(callback_query.from_user.id,
                               "поздравляю, вы сделали все правильно, менеджер уже начал делать букет", reply_markup=st)
        msg = ""
        cnx = connect()

        cursor = cnx.cursor()

        sql = ("select flobot.orders.order_shipping_adress,flobot.orders.shop_order_id, flobot.orders.shop_addr, "
               "clients.first_name, clients.client_phone, "
               "successful_payment.caption, successful_payment.cost, successful_payment.provider_payment_charge_id "
               "from flobot.orders "
               "left join clients on orders.client_order_id = clients.client_chat_id "
               "left join successful_payment on orders.client_order_id = successful_payment.client_id "
               "where successful_payment.id =%s;")
        cursor.execute(sql, (int(id),))

        cur = cursor.fetchone()

        msg = resp["Status"] + '\n' + " адрес доставки: " + cur[0] + '\n'
        print(msg)
        msg1 = "адрес магазина: " + cur[2] + '\n'
        print(msg1)
        ph = cur[4]
        print(type(ph), ph)
        msg2 = "покупатель: " + cur[3] + ' ' + ph + '\n'
        print(msg2)
        msg3 = "заказ: " + cur[5] + '\n'
        print(msg3)
        cc = cur[6]
        print(type(cc), cc)
        ttt = str
        msg4 = "финальная цена: \ntесли вы участвовали в аукционе - фактическая цена оплаты будет отличаться" + str(
            cc) + '\n'
        qqqq = cur[1]

        print(cur[7])
        cnx.close()

        cnx = connect()

        cursor = cnx.cursor()
        sql = ("select shops.manager_chat_id from shops where shops.shop_id = '%s'")
        cursor.execute(sql, (int(qqqq),))
        roww = cursor.fetchone()
        await bot.send_message(roww[0], msg + msg1 + msg2 + msg3 + msg4)
        await bot.send_message(roww[0], "обязательно свяжитесь с клиентом!")
    else:
        st = types.InlineKeyboardMarkup()
        bn = types.InlineKeyboardButton("проблемы при пользовании", callback_data="helper")
        bn1 = types.InlineKeyboardButton("статус оплаты", callback_data="payment_status")
        st.add(bn, bn1)
        await bot.send_message(callback_query.from_user.id,
                               "оплатите заказ, а если вы уже заплатили - нажмите кнопку 'подтвердить'",
                               reply_markup=st)

        cnx.close()


@dp.callback_query_handler(lambda c: c.data == 'helper', state='*')
async def process_callback_disarm(callback_query: types.CallbackQuery, state=FSMContext):
    print("helper")
    await bot.answer_callback_query(callback_query.id, "helper")
    await bot.send_message(callback_query.from_user.id, "свяжитесь с нами по телефону: +7-915-019-50-29")


@dp.callback_query_handler(lambda c: c.data == 'payment_status', state='*')
async def process_callback_disarm(callback_query: types.CallbackQuery, state=FSMContext):
    print("payment_status")
    await bot.answer_callback_query(callback_query.id, "payment_status")

    sql = (
        "select provider_payment_charge_id from flobot.successful_payment where client_id = %s ORDER BY id DESC LIMIT 1;")
    v = (callback_query.from_user.id,)

    payment_id = get_query(sql, v)

    from tink_payment import payment

    pay = payment("1615725763495", "2illo2v6pxz3brce")
    resp = pay.get_state(payment_id)

    print(resp, payment_id, "!!!!!")
    await bot.send_message(callback_query.from_user.id, "статус оплаты: " + resp["Status"])
    print(resp)


@dp.message_handler(commands=["refund"], state='*')
async def refund(msg: types.Message, state=FSMContext):
    print("refund")
    print(msg.text)
    ident = msg.text[8:]
    iiden = int(ident)
    print(ident)
    await bot.send_message(msg.chat.id, "initialize refund")
    cnx = connect()
    cursor = cnx.cursor()
    sql = ("select * from flobot.successful_payment where id = '%s';")
    cursor.execute(sql, (iiden,))
    row = cursor.fetchone()
    id_pay = row[1]
    inf = str(row[2]) + '\n' + str(row[3])

    print(inf)

    from tink_payment import payment

    pay = payment("1615725763495", "2illo2v6pxz3brce")
    info = pay.get_state(id_pay)
    bot.send_message(msg.chat.id, info)

    await bot.send_message(msg.chat.id, "вы оформили возврат!")

    sql = (""" select manager_chat_id from shops where shop_id = %s """)
    v = (row[7],)
    cnx = connect()
    cursor = cnx.cursor()
    cursor.execute(sql, v)
    cc = cursor.fetchone()
    bot.send_message(cc[0], "заказ был отменен: ")
    bot.send_message(cc[0], inf)

    cnx.close()

@dp.callback_query_handler(lambda c: c.data == 'fast_search', state=States.GEO_PROVE)
async def fast_search(callback_query: types.CallbackQuery):
    state = dp.current_state(user=callback_query.from_user.id)
    user_id = callback_query.from_user.id
    await bot.send_message(user_id, "выберите категорию цветов")
    state.set_state(States.FAST_SEARCH)
    # searching shops
    current_addr = get_query("select order_shipping_adress from orders where client_order_id = '%s'", (user_id,))

    lon = 0.0
    lat = 0.0
    from dadata import DadataAsync
    token = DADATA_TOKEN
    secret = config.DADATA_SECRET
    dadata = DadataAsync(token)
    result = await dadata.suggest("address", current_addr)
    await dadata.close()
    if not result:
        await bot.send_message(user_id, "сервис поддерживает адреса только из России, введите адрес корректно")
        await  state.set_state(States.TO_ME_ST)
        return -1

    for row in result:
        value = row['value']
        current_value = value
        dadata = DadataAsync(token, secret)
        try:
            result = await dadata.clean("address", current_value)
        except:
            await bot.send_message(user_id,
                                   "наблюдаются проблемы с сервисом определения адресов, повторите попытку позже")
            print("наблюдаются проблемы с сервисом определения адресов, повторите попытку позже")
            await bot.send_message(ADMIN_CHAT_ID,
                                   "наблюдаются проблемы с сервисом определения адресов dadata адрес: " + current_value)
            return -1
        lon = result['geo_lon']
        lat = result['geo_lat']
        await dadata.close()
        break

    cnx = connect()
    cursor = cnx.cursor()
    sqlin = (
        "select flobot.shop_addr.*, flobot.shops.shop_name from flobot.shop_addr left join flobot.shops on "
        "flobot.shops.shop_id = flobot.shop_addr.shop_id where flobot.shops.is_open = 'yes' and flobot.shops.tink_shop_code is not null;")
    id_of_min = 10000
    d_min = 1000000.
    cursor.execute(sqlin)

    tmp_keys = types.ReplyKeyboardMarkup(True, True)

    iterator = 0

    dict_of_shops = {}

    for row in cursor:
        print(lon, lat)
        lon1 = float(lon) * pi / 180
        lat1 = float(lat) * pi / 180

        lon2 = float(row[3]) * pi / 180
        lat2 = float(row[4]) * pi / 180
        d = 2. * 6371 * asin(sqrt(
            sin((lat2 - lat1) / 2) * sin((lat2 - lat1) / 2) + cos(lat1) * cos(lat2) * sin((lon2 - lon1) / 2) * sin(
                (lon2 - lon1) / 2)))
        idstr = float(d)
        # dstr = str(idstr)

        dict_of_shops.update({row[0]: idstr})  # with addr_id
    cnx.close()
    sort_dict = {}
    sort_keys = sorted(dict_of_shops, key=dict_of_shops.get)
    print(sort_keys)

    for w in sort_keys:
        sort_dict[w] = dict_of_shops[w]
        print("!")
    print(sort_dict, "dict_of_shops")
    cnx.close()
    shop_list = []
    iter = 5
    for i, v in sort_dict.items():
        if iter == 0:
            break
        print(i, v)
        shop_list.append(i)
        iter -= 1
    print(shop_list)
    # =======
    id = user_id

    shop_id = id_of_min
    list_of_shop = []

    for addr_id in shop_list:
        rw = get_query_all("select shop_id, addr from shop_addr where addr_id = %s;", (addr_id,))
        shop_id = (rw[0]).__str__()
        list_of_shop.append(shop_id)
        print(shop_id, "вот они наши id")


    print(list_of_shop, "list of shop")

    key_dict = {}
    for shop_id in list_of_shop:
        regex_dict
        print(shop_id, "shop_id")
        cnx = connect()
        curs = cnx.cursor()
        cost = 4000
        curs.execute("select categories from products where shop_id = %s and cost < 4000;", (shop_id,))
        products = curs.fetchall()
        # print(products, "@")
        for row in products:
            srstr = row[0]
            # print(row[0], "!!")
            for key in regex_dict:
                # print(regex_dict[key], "regex_dict[key]")
                # print(key), "key"
                # # print(key, "key")
                try:
                    res = re.search(regex_dict[key], srstr)
                except:
                    continue

                if res is not None and len(res[0]) > 1:
                    # print(key_dict[key])
                    try:
                        key_dict[key] += 1
                    except:
                        print("key_dict.update({key")
                        key_dict.update({key: 1})
                        print(res[0], "@$#")
        print(key_dict)
        keys = types.ReplyKeyboardMarkup(True, True)
        max = 15
        iter = 1
        btns = []
        j = 0
        for key in key_dict:
            znach = key_dict[key]
            stroka1 = key + ' ' + znach.__str__()
            btn = stroka1
            btns.append(btn)
            keys.row(btn)
            j += 1

        print(btns)
        tuple(btns)
        # print("tut")
        if j == 0:
            await bot.send_message(user_id,
                                   "🔥💐похоже, у магазина нет букетов в этом ценовом диапозоне, выберите другой",
                                   reply_markup=COST)
            return -1
        keys.row("☆ ↩️ Назад ↩️ ☆")
        # keys.row("к магазинам")
    await state.set_state(States.FAST_SEARCH_CATALOG)
    await state.update_data(list_of_shop = list_of_shop)
    await bot.send_message(user_id,
                               "🔥💐Отлично,выберите нужный цветок",
                               reply_markup=keys)



@dp.message_handler(state='*')
async def echo(msg: types.Message):
    print("echo")
    # print(msg.photo[-1].file_id)
    state = dp.current_state()
    if msg.text == "★ ⬆️ В начало ⬆️ ★":
        await bot.send_message(msg.chat.id, "начнем заново", reply_markup=INIT_KEYBOARD)
        await state.set_state(States.AFT_INIT_STATE)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=init(dp))