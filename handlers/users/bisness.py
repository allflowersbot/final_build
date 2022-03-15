from math import *
from datetime import datetime
import config
import order_product
from loader import dp, bot, auctions, ADMIN_CHAT_ID, array, list_of_orders, list_of_confirmed_orders
from config import *
import re
from order_product import product, order
from async_auction import auction, payment_cooldown
import asyncio
from keyboards import TMP, INIT_KEYBOARD, TO_ME, COST, regex_dict, button_phone, REP_KEY_WHEN_INLINE, FLOWER_KEYS
from utils import States
from aiogram import types
from dbcm import connect, commit_query, get_query, get_query_all
from video_instruction import bot_videos, send_video_instruction
from aiogram.dispatcher import FSMContext

list_of_id = []
list_of_id.append(ADMIN_CHAT_ID)
list_of_id.append(494609919)


@dp.message_handler(state='*', commands=['start'])
async def process_start_command(message: types.Message):
    state = dp.current_state(user=message.chat.id)

    data = await state.get_data()
    try:
        curr_id = data["curr_order_id"]
        print("curr_id={}".format(curr_id))

        for ordr in list_of_orders:
            if ordr.get_order_id() == curr_id:
                list_of_orders.remove(ordr)
                break
        await state.reset_data()
    except:
        print("start without prev order")

    # add to db.orders
    first = message.chat.first_name
    last = message.chat.last_name
    id = message.chat.id
    # add to db.clients
    cnx = connect()
    cursor = cnx.cursor()
    sql = ("select client_chat_id from flobot.clients where client_chat_id = '%s';")
    cursor.execute(sql, (id,))
    row = cursor.fetchone()
    if (row == None):
        print("add client {} to db.clients".format(message.chat.id))
        vid = bot_videos['start']
        await bot.send_video(message.chat.id, vid)
        cursor.close()
        sqlin = ("insert into flobot.clients(first_name, last_name, client_chat_id) "
                 "values (%s, %s, '%s')")
        value = (first, last, id)
        commit_query(sqlin, value)
        cursor.close()
    cursor.close()
    cnx.close()
    # =======
    # add to db.orders
    id = message.chat.id
    cnx = connect()
    cursor = cnx.cursor()
    sql = ("select client_order_id from flobot.orders where client_order_id = '%s';")
    cursor.execute(sql, (id,))
    row = cursor.fetchone()
    if row is None:
        print("add client {} to db.orders".format(message.chat.id))
        sqlin = ("insert into flobot.orders(client_order_id) "
                 "values ('%s')")
        value = (id,)
        commit_query(sqlin, value)
    cnx.close()
    # =======
    cnx = connect()
    cursor = cnx.cursor()
    que = "delete from cart where client_id = %s;"
    cursor.execute(que, (id,))
    cnx.commit()
    cnx.close()
    # =======
    await bot.send_message(message.from_user.id,
                           "➡️Введите адрес доставки в заданном формате (улица,номер дома) c клавиатуры: "  # todo make start_message
                           "\"Никольская 21\"\n⭐️или пришлите геолокацию адреса доставки",
                           reply_markup=TO_ME)
    await state.set_state(States.TO_ME_ST_test)
    await send_video_instruction(message, 'order_shipping_adress', 'addr')


@dp.message_handler(state='*', commands=['help'])
async def help(msg: types.Message):
    await msg.answer("свяжитесь с нами в телеграмм по телефону: +7-915-019-50-29")


@dp.message_handler(state='*', commands=['show_buckets'])
async def NS(msg: types.Message):
    state = dp.current_state(user=msg.chat.id)
    await msg.answer("xt")
    await state.set_state(States.default_buckets)
    if msg.chat.id in list_of_id:
        cnx = connect()
        cursor = cnx.cursor()
        sql = ("select * from default_buckets;")
        print("!@!")
        cursor.execute(sql)
        curs = cursor.fetchall()
        for row in curs:
            await bot.send_photo(msg.chat.id, row[2], str(row[3]) + '\n' + row[4] + '\n' + str(row[5]))
    else:
        await msg.answer("У вас нет прав доступа")


@dp.message_handler(state='*', commands=['default_buckets'])
async def NS(msg: types.Message):
    state = dp.current_state(user=msg.chat.id)
    await bot.send_message(msg.chat.id, "system check")
    await state.set_state(States.default_buckets)
    await msg.answer("фото->короткое описание->состав букета(наименования цветов через запятую)->цена")


@dp.message_handler(state=States.AFT_INIT_STATE)
async def echo_message(msg: types.Message, state=FSMContext):
    state = dp.current_state(user=msg.chat.id)
    # if msg.text == '💐ХОЧУ ДОСТАВКУ БЕСПЛАТНО ЗА 40 МИНУТ🚚':
    #     await bot.send_message(msg.from_user.id, "⭐️вы выбрали доставку букета к себе", reply_markup=TO_ME)
    #     await state.set_state(States.TO_ME_ST)
    #
    # elif msg.text == '💐ХОЧУ ЗАКАЗАТЬ НА АДРЕС🚚':
    #     await bot.send_message(msg.from_user.id, "➡️Введите адрес доставки в заданном формате c клавиатуры: "
    #                                              "\"Никольская 21\"\n⭐️или пришлите геолокацию адреса доставки",
    #                            reply_markup=TMP)
    #     await state.set_state(States.TO_ME_ST)

    if msg.text == '💐НАЙТИ КОНКРЕТНЫЙ МАГАЗИН🔎':
        await bot.send_message(msg.from_user.id,
                               "➡️введите ❗️ТОЧНОЕ ❗️название магазина", reply_markup=TMP)
        await state.set_state(States.CURRENT_SHOP)
    elif msg.text == 'помощь':
        await bot.send_message(msg.chat.id, "свяжитесь с нами в телеграмм по телефону: +7-915-019-50-29")
    elif msg.text == 'категории':
        await msg.answer("ознакомьтесь с категориями товаров", reply_markup=FLOWER_KEYS)
        await state.set_state(States.FLOWER_CATALOG)

    elif msg.text == '💐АКЦИИ💐':

        await bot.send_message(msg.chat.id, "пришлите адрес куда доставлять геолокацию либо сам адрес",
                               reply_markup=TO_ME)
        await state.set_state(States.sales1)
        return -1
        # await bot.send_message(msg.chat.id, "раздел акций, ознакомьтесь с акционными товарами")
        # ## start
        # i = 0
        # cnx = connect()
        #
        # cursor = cnx.cursor()
        #
        # sqlin = ("select id, file_id, caption, categories, cost, shop_id "
        #          "from flobot.products "
        #          "where sale = 'sale';")
        # # value = (shop_id,)
        # cursor.execute(sqlin)
        # flowers = cursor.fetchall()
        # price = 0
        # number = 0
        # for current in flowers:
        #     print(current[0], current[4])
        #     flag = 0
        #     flagflo = 0
        #     price = (int(current[4]))  # + int(add_cost))
        #     # * 100
        #     #print(distance, add_cost, PRICE.amount, "qq")
        #
        #     # flower = re.search(regex_dict[capture], current[3])
        #     sh_id = current[5]
        #     addrs = ""
        #
        #     sq = ("select addr from shop_addr where shop_id = %s")
        #     v = (sh_id,)
        #     c = connect()
        #     cur = c.cursor()
        #     cur.execute(sq, v)
        #     ad = cur.fetchall()
        #     for j in ad:
        #         addrs += j[0] + '\n'
        #     number += 1
        #     kb1 = types.InlineKeyboardMarkup()
        #     bm1 = types.InlineKeyboardButton("+", callback_data='button1')
        #     bm2 = types.InlineKeyboardButton("-", callback_data='button2')
        #
        #     kb1.add(bm1, bm2)
        #     ch = await bot.send_photo(msg.chat.id, photo=current[1],
        #                               caption=current[2] + "конечная стоимость:" + str(
        #                                   price) + " доставка: уточним позже"  + "\n#" + str(
        #                                   current[0]) + "#" + "адреса магазина:" + addrs, reply_markup=kb1)
        #     ID = ch.photo[-1].file_id
        #     ID2 = current[1]
        #     i = int(i) + int(1)
        #
        # ##end

    elif msg.text == 'мои заказы':
        cnx = connect()
        cursor = cnx.cursor()
        sql = (
            "select successful_payment.caption, successful_payment.cost, successful_payment.status, successful_payment.id from flobot.successful_payment where client_id = '%s';")
        cursor.execute(sql, (msg.chat.id,))
        curs = cursor.fetchall()
        for row in curs:
            try:
                await bot.send_message(msg.chat.id, "id: " + str(row[3]) + " " + row[0] + str(row[1]) + row[2])
            except:
                print(row)
        cnx.close()

        kb = types.ReplyKeyboardMarkup(True, True)

    elif msg.text == 'очистить корзину':
        await msg.answer('очистить корзину')
        cnx = connect()
        cursor = cnx.cursor()
        sql = ("delete from cart where client_id = '%s';")
        cursor.execute(sql, (msg.chat.id,))
        cnx.commit()
        await state.set_state(States.AFT_INIT_STATE)

    elif msg.text == 'стать магазином':
        btn1 = types.InlineKeyboardButton(text="инструкция", url="https://allflowersbot.github.io/allflowers/instr")
        kb1 = types.InlineKeyboardMarkup(True, True)
        kb1.add(btn1)
        await bot.send_photo(msg.chat.id,
                             "AgACAgIAAxkBAAKPlmAf8YXfpoxbQjJ5zdX6qC_qKDo-AAJErzEbgxH4SMALfR3IKLJSUEMFly4AAwEAAwIAA3kAA-KpBgABHgQ",
                             reply_markup=kb1)  # todo стать магазином

        btn = types.InlineKeyboardButton(text="инстаграм магазин", url="https://www.instagram.com/all.flowru/")
        kb = types.InlineKeyboardMarkup(True, True)
        kb.add(btn)

        await bot.send_photo(msg.chat.id,
                             "AgACAgIAAxkBAAKPl2Af8YkaVJDAroukUNilBX-uJFnEAAJGrzEbgxH4SDAxWduraSI5EcbSmi4AAwEAAwIAA3kAA--SAQABHgQ",
                             reply_markup=kb)

    else:
        await bot.send_message(msg.from_user.id, "выберите место назначения используя клавиатуру внизу",
                               reply_markup=INIT_KEYBOARD)
        await state.set_state(States.AFT_INIT_STATE)


@dp.message_handler(state=States.sales1, content_types=types.ContentTypes.ANY)
async def sales1(msg: types.Message, state=FSMContext):
    state = dp.current_state(user=msg.chat.id)
    current_value = ""
    if msg.location:
        from dadata import DadataAsync
        DADATA_token = DADATA_TOKEN
        dadata = DadataAsync(DADATA_token)

        tmp = msg['location']
        result = await dadata.geolocate(name="address", lat=tmp['latitude'], lon=tmp['longitude'])
        await dadata.close()
        for i in result:
            value = i['value']
            current_value = value
            print(value)
            break

    elif msg.text == "☆ ↩️ Вернуться назад ↩️ ☆":
        await state.set_state(States.AFT_INIT_STATE)
        await bot.send_message(msg.chat.id, "начните заново", reply_markup=INIT_KEYBOARD)
        return -1

    elif msg.text:
        from dadata import DadataAsync
        token = DADATA_TOKEN
        secret = config.DADATA_SECRET
        dadata = DadataAsync(token)
        result = await dadata.suggest("address", msg.text)
        await dadata.close()
        if not result:
            await bot.send_message(msg.chat.id, "сервис поддерживает адреса только из России, введите адрес корректно")
            await  state.set_state(States.sales1)
            return -1
        current_value = ""
        lon = 1.
        lat = 1.
        for row in result:
            value = row['value']
            current_value = value
            dadata = DadataAsync(token, secret)
            result = await dadata.clean("address", current_value)
            lon = result['geo_lon']
            lat = result['geo_lat']
            await dadata.close()
            current_value = result["result"]
            break

    sql = ("update orders set order_shipping_adress = %s where client_order_id = %s;")
    val = (current_value, msg.chat.id)
    commit_query(sql, val)

    # BD

    await bot.send_message(msg.chat.id, "раздел акций, ознакомьтесь с акционными товарами")
    ## start
    i = 0
    cnx = connect()

    cursor = cnx.cursor()

    sqlin = ("select id, file_id, caption, categories, cost, shop_id "
             "from products "
             "where sale = 'sale';")
    # value = (shop_id,)
    cursor.execute(sqlin)
    flowers = cursor.fetchall()
    price = 0
    number = 0
    for current in flowers:
        print(current[0], current[4])
        flag = 0
        flagflo = 0
        price = (int(current[4]))  # + int(add_cost))
        # * 100
        # print(distance, add_cost, PRICE.amount, "qq")

        # flower = re.search(regex_dict[capture], current[3])
        sh_id = current[5]
        addrs = ""

        sq = ("select addr from shop_addr where shop_id = %s")
        v = (sh_id,)
        c = connect()
        cur = c.cursor()
        cur.execute(sq, v)
        ad = cur.fetchall()
        for j in ad:
            addrs += j[0] + '\n'
        number += 1
        kb1 = types.InlineKeyboardMarkup()
        bm1 = types.InlineKeyboardButton("+", callback_data='button1')
        bm2 = types.InlineKeyboardButton("-", callback_data='button2')

        kb1.add(bm1, bm2)
        ch = await bot.send_photo(msg.chat.id, photo=current[1],
                                  caption=current[2] + "конечная стоимость:" + str(
                                      price) + " доставка: уточним позже" + "\n#" + str(
                                      current[0]) + "#" + "адреса магазина:" + addrs, reply_markup=kb1)
        ID = ch.photo[-1].file_id
        ID2 = current[1]
        i = int(i) + int(1)

    ##end


@dp.message_handler(state=States.TO_ME_ST_test,
                    content_types=types.ContentTypes.ANY)  # -> States.TO_ME_ST_test -> States.COST
async def geo(msg: types.Message, state=FSMContext):  # ||
    # =======                                                                          #        \/
    flag_vid = False  # States.AFT_INIT_STATE
    sql = "select order_shipping_adress from orders where client_order_id = {}".format(msg.chat.id)
    cnx = connect()
    curs = cnx.cursor()
    curs.execute(sql)
    info = curs.fetchone()
    if info[0] is None:
        print('vid')
        flag_vid = True
        # vid = test_bot_videos[state]
        # vid = bot_videos[state]
        # await bot.send_video(msg.chat.id, vid)
    # =======
    state = dp.current_state(user=msg.chat.id)
    current_value = ""
    lon = 1.
    lat = 1.

    if msg.text == "☆ ↩️ Вернуться назад ↩️ ☆":
        await state.set_state(States.AFT_INIT_STATE)
        await bot.send_message(msg.chat.id, "начните заново", reply_markup=INIT_KEYBOARD)
        return -1

    elif msg.location:
        from dadata import DadataAsync
        DADATA_token = DADATA_TOKEN
        dadata = DadataAsync(DADATA_token)

        tmp = msg['location']
        result = await dadata.geolocate(name="address", lat=tmp['latitude'], lon=tmp['longitude'])
        await dadata.close()
        for i in result:
            value = i['value']
            current_value = value
            break

        lon = tmp['longitude']
        lat = tmp['latitude']

    elif msg.text:
        from dadata import DadataAsync
        token = DADATA_TOKEN
        secret = config.DADATA_SECRET
        dadata = DadataAsync(token)
        result = await dadata.suggest("address", msg.text)
        await dadata.close()
        if not result:
            await bot.send_message(msg.chat.id, "сервис поддерживает адреса только из России, введите адрес корректно")
            await state.set_state(States.TO_ME_ST_test)
            return -1

        for row in result:
            value = row['value']
            current_value = value
            dadata = DadataAsync(token, secret)
            result = await dadata.clean("address", current_value)
            lon = result['geo_lon']
            lat = result['geo_lat']
            await dadata.close()
            break

    # =======
    cnx = connect()
    cursor = cnx.cursor()
    sqlin = (
        "select flobot.shop_addr.*, flobot.shops.shop_name from flobot.shop_addr left join flobot.shops on "
        "flobot.shops.shop_id = flobot.shop_addr.shop_id where flobot.shops.is_open = 'yes' and flobot.shops.tink_shop_code is not null;")
    cursor.execute(sqlin)

    id_of_min = 10000
    d_min = 1000000.
    tmp_keys = types.ReplyKeyboardMarkup(True, True)
    dict_of_addrs = {}
    for row in cursor:
        lon1 = float(lon) * pi / 180
        lat1 = float(lat) * pi / 180

        lon2 = float(row[3]) * pi / 180
        lat2 = float(row[4]) * pi / 180
        d = 2. * 6371 * asin(sqrt(
            sin((lat2 - lat1) / 2) * sin((lat2 - lat1) / 2) + cos(lat1) * cos(lat2) * sin((lon2 - lon1) / 2) * sin(
                (lon2 - lon1) / 2)))
        dict_of_addrs.update({row[0]: float(d)})  # with addr_id
    cnx.close()

    sort_addrs_dict = {}
    sort_keys = sorted(dict_of_addrs, key=dict_of_addrs.get)
    print("sort_addrs={}".format(sort_keys))

    for w in sort_keys:
        sort_addrs_dict[w] = dict_of_addrs[w]
    print("sort_addrs_dict={}".format(sort_addrs_dict))
    d_min = list(sort_addrs_dict.items())[0][1]
    print("d_min={}".format(d_min))

    # cnx.close()
    addrs_list = []
    iter = 5  # число адресов в выборке #

    for i, v in sort_addrs_dict.items():
        if iter == 0:
            break
        addrs_list.append(i)
        iter -= 1
    print("addrs_list={}".format(addrs_list))
    # =======
    id = msg.chat.id
    sh_list = []
    managers = []
    for addr_id in addrs_list:
        rw = get_query_all("select shop_id, addr from shop_addr where addr_id = %s;", (addr_id,))
        shop_id = str(rw[0])
        sh_list.append(shop_id)

        cnx = connect()
        curs = cnx.cursor()
        curs.execute("select manager_chat_id from managers where shop_id = {};".format(shop_id))
        mngrs = curs.fetchall()
        for manager in mngrs:
            managers.append(manager[0])
    print("sh_list={}".format(sh_list))
    print("managers={}".format(managers))

    sqlin = ("update flobot.orders set order_shipping_adress = %s, len ='%s' "
             "where client_order_id = '%s';")
    value = (current_value, d_min, id)
    commit_query(sqlin, value)
    no_duplicate_sh_list = set(sh_list)
    #####
    shop_name = get_query("select shop_name from shops where shop_id = %s;", (1,))

    cnx = connect()
    cursor = cnx.cursor()
    sqlin = ("select id, file_id, caption, categories, cost, shop_id "
                 "from products where default_bucket = true order by cost asc LIMIT 6;")

    cursor.execute(sqlin)
    flowers = cursor.fetchall()
    price = 0
    number = 0
    for current in flowers:
        flag = 0
        flagflo = 0
        try:
            price = (int(current[4]))
        except:
            print("product without cost")
            continue

        sh_id = 1
        addrs = ""

        sq = ("select addr from shop_addr where shop_id = %s")
        v = (sh_id,)
        c = connect()
        cur = c.cursor()
        cur.execute(sq, v)
        ad = cur.fetchall()
        for j in ad:
            addrs += j[0] + '\n'
        number += 1
        kb1 = types.InlineKeyboardMarkup()
        bm1 = types.InlineKeyboardButton("+", callback_data='button1')
        bm2 = types.InlineKeyboardButton("-", callback_data='button2')

        kb1.add(bm1, bm2)
        ch = await bot.send_photo(msg.chat.id, photo=current[1],
                                  caption="магазин: " + str(shop_name) + '\n' + str(
                                      current[2]) + "\nконечная стоимость:" + str(
                                      price) + "\nдоставка: уточним позже" + "\n#" + str(
                                      current[0]) + "#" + "\nадреса магазина:\n" + addrs, reply_markup=kb1)
        ID = ch.photo[-1].file_id
        ID2 = current[1]
        # i = int(i) + int(1)
    ####
    tmp_keys.row("🟥↩️главное меню↩️🟥")
    await bot.send_message(msg.chat.id, "🔥💰Отлично, теперь выберите предполагаемую ценовую категорию",
                           reply_markup=COST)
    await state.set_state(States.COST)
    print("no_duplicate_sh_list={}".format(no_duplicate_sh_list), "async geo")
    await state.update_data(list_of_shops=no_duplicate_sh_list)

    # await state.set_state(States.GEO_PROVE)
    # end


@dp.message_handler(state=States.FAST_SEARCH_CATALOG)  # -> States.CART
async def fast_search(msg: types.Message, state=FSMContext):
    print("FAST_SEARCH_CATALOG")
    state = dp.current_state(user=msg.chat.id)
    if msg.text == "☆ ↩️ Назад ↩️ ☆":
        await bot.send_message(msg.chat.id, "🔥💰Отлично, теперь выберите предполагаемую ценовую категорию ",
                               reply_markup=COST)
        await state.set_state(States.COST)
        return -1

    data = await state.get_data()
    list_of_shop = data["list_of_shops"]
    cost = data["cost"]
    flo = msg.text
    i = flo.find(' ')
    flor = flo[:i]
    flower = flor
    cnt = 0
    for key in regex_dict:
        res = re.search(regex_dict[key], flor)
        if res:
            cnt += 1

    if cnt == 0:
        await bot.send_message(msg.chat.id, "выберите цветы")
        return -1

    id = msg.chat.id

    sqlin = ("update flobot.orders"
             " set order_caption = %s"
             "where client_order_id = '%s';")
    value = (flower, id)
    commit_query(sqlin, value)

    key = ""
    for k in regex_dict:
        res = re.search(regex_dict[k], flower)
        if res is not None and len(res[0]) > 1:
            key = regex_dict[k]
            break

    await bot.send_message(msg.chat.id, "ознакомьтесь с каталогом магазина:", reply_markup=REP_KEY_WHEN_INLINE)
    print("cost={},\nlist_of_shop={},\nflower={},\nkey={}".format(cost, list_of_shop, flower, key))
    i = 1
    for shop_id in list_of_shop:
        print(shop_id)
        # здесь часть про показать букеты
        cnx = connect()
        cursor = cnx.cursor()
        if i == 1:
            sqlin = (
                "select id, file_id, caption, categories, cost, default_bucket from flobot.products where (shop_id = '%s' and cost <= %s) or (default_bucket is true and cost <=%s);")
            value = (int(shop_id), cost, cost,)
        else:
            sqlin = (
                "select id, file_id, caption, categories, cost from flobot.products where shop_id = '%s' and cost <= %s")
            value = (int(shop_id), cost,)
        cursor.execute(sqlin, value)
        flowers = cursor.fetchall()
        for current in flowers:
            shop_name = ""
            categ = current[3]
            res = re.search(key, categ)
            if res is not None and len(res[0]) > 1:
                if i == 1:
                    if current[5]:
                        shop_name = 'default_bucket'
                else:
                    shop_name = get_query("select shop_name from shops where shop_id = %s;", (shop_id,))
                kb1 = types.InlineKeyboardMarkup()
                bm1 = types.InlineKeyboardButton("добавить", callback_data='button1')  # +
                bm2 = types.InlineKeyboardButton("убрать", callback_data='button2')  # -
                kb1.add(bm1, bm2)
                ch = await bot.send_photo(msg.chat.id, photo=current[1],
                                          caption="магазин: " + str(shop_name) + '\n' + str(
                                              current[2]) + "\nцена:" + str(
                                              current[4]) + "\nдоставка: уточним у менеджера" + "\n#" + str(
                                              current[0]) + "#",
                                          reply_markup=kb1)
        i -= 1
    await state.set_state(States.CART)


@dp.message_handler(state=States.GEO_PROVE)
async def echo_message(msg: types.Message, state=FSMContext):
    await send_video_instruction(msg, 'order_cost', "cost")
    state = dp.current_state(user=msg.chat.id)
    id = msg.chat.id

    if msg.text == "🟥↩️главное меню↩️🟥":
        await state.set_state(States.AFT_INIT_STATE)
        await bot.send_message(msg.chat.id, "ИСПОЛЬЗУЙТЕ КНОПКИ ВНИЗУ", reply_markup=INIT_KEYBOARD)
    elif msg.text == "✅ Продолжить по умолчанию, всё верно ✅":
        await state.set_state(States.COST)
        await bot.send_message(msg.chat.id, "🔥💰Отлично, теперь выберите предполагаемую ценовую категорию ",
                               reply_markup=COST)
    else:
        iaddr = msg.text.find(" адрес ")
        addr = msg.text[iaddr + 7:]
        print(addr)
        import mysql.connector
        cnx = mysql.connector.connect(user='root', password='0000',
                                      host='127.0.0.1',
                                      database='flobot')
        cursor = cnx.cursor()
        sqlin = (
            "select flobot.shops.shop_name, shop_id from flobot.shops where shop_name = %s;")
        value = (msg.text[:iaddr],)
        cursor.execute(sqlin, value)
        row = cursor.fetchone()
        if row:
            sqlin = ("update flobot.orders set shop_order_id = '%s', shop_addr = %s "
                     "where client_order_id = '%s';")
            value = (row[1], addr, id)
            commit_query(sqlin, value)
            await bot.send_message(msg.chat.id, "🔥💰Отлично, теперь выберите предполагаемую ценовую категорию",
                                   reply_markup=COST)
            await state.set_state(States.COST)
            print("States.COST")

        else:
            await state.set_state(States.AFT_INIT_STATE)
            await bot.send_message(msg.chat.id, "начните заново", reply_markup=INIT_KEYBOARD)
        cnx.close()


@dp.message_handler(state=States.COST)  # -> States.COST -> FAST_SEARCH_CATALOG
async def echo_message(msg: types.Message, state=FSMContext):
    print("States.COST")
    state = dp.current_state(user=msg.chat.id)

    if msg.text == "☆ ↩️ Назад ↩️ ☆":
        await state.set_state(States.AFT_INIT_STATE)
        await bot.send_message(msg.chat.id, "начните заново", reply_markup=INIT_KEYBOARD)
        return -1

    data = await state.get_data()
    no_duplicate_list_of_shop = data["list_of_shops"]
    print("no_duplicate_list_of_shop ={}".format(no_duplicate_list_of_shop))
    print("data ={}".format(data))
    cost_str = msg.text
    strS = re.search(r'\d{4}', cost_str)
    print("strS = {}".format(strS))

    if not strS:
        await bot.send_message(msg.chat.id, "выберите цену используя клавиатуру ниже", reply_markup=COST)
        await state.set_state(States.COST)
        return -1

    print("strS[0]= {}".format(strS[0]))
    cost_str = strS[0]
    # тут мы уже знаем стоимость
    sqlin = ("update flobot.orders"
             " set order_cost = %s"
             "where client_order_id = '%s';")
    value = (cost_str, msg.chat.id)
    commit_query(sqlin, value)

    user_id = msg.chat.id
    await bot.send_message(user_id, "выберите категорию цветов")
    # searching shops
    key_dict = {}
    cost = int(cost_str)
    print("cost={}".format(cost))
    i = 1
    for shop_id in no_duplicate_list_of_shop:
        print("shop_id={}".format(shop_id))
        cnx = connect()
        curs = cnx.cursor()
        if i == 1:
            curs.execute(
                "select categories from products where (shop_id = %s and cost <= %s) or (default_bucket is true and cost <=%s);",
                (shop_id, cost, cost,))
        else:
            curs.execute(
                "select categories from products where shop_id = %s and cost <= %s;",
                (shop_id, cost,))
        products = curs.fetchall()
        for row in products:
            categ = row[0]
            for key in regex_dict:
                res = re.search(regex_dict[key], categ)
                if res is not None and len(res[0]) > 1:
                    try:
                        key_dict[key] += 1
                    except:
                        key_dict.update({key: 1})
        i = 0
    print("key_dict={}".format(key_dict))

    keys = types.ReplyKeyboardMarkup(True, True)
    for k in key_dict:
        keys.add(types.KeyboardButton(str(k) + ' ' + str(key_dict[k]) + ' шт'))

    keys.row("☆ ↩️ Назад ↩️ ☆")
    await state.set_state(States.FAST_SEARCH_CATALOG)
    info = {"los": no_duplicate_list_of_shop, 'cost': cost}
    print("info={}".format(info))
    await state.update_data(cost=cost)
    await bot.send_message(user_id,
                           "🔥💐Отлично,выберите нужный цветок, число справа от категории - "
                           "количество подходящих букетов",
                           reply_markup=keys)

    # тут


@dp.message_handler(state=States.FLOWER_CATALOG)  # -> States.FLOWER_CATALOG ->
async def echo_message(msg: types.Message, state=FSMContext):
    print("FLOWER_CATALOG")
    state = dp.current_state(user=msg.chat.id)
    if msg.text == "☆ ↩️ Назад ↩️ ☆":
        await bot.send_message(msg.chat.id, "🔥💰Отлично, теперь выберите предполагаемую ценовую категорию ",
                               reply_markup=COST)
        await state.set_state(States.COST)
        return -1
    elif msg.text == "к магазинам":
        print("Назад вернуться к выбору магазинов")

        current_addr = get_query("select order_shipping_adress from orders where client_order_id = '%s'",
                                 (msg.chat.id,))

        lon = 0.0
        lat = 0.0
        from dadata import DadataAsync
        token = DADATA_TOKEN
        secret = config.DADATA_SECRET
        dadata = DadataAsync(token)
        result = await dadata.suggest("address", current_addr)
        await dadata.close()
        if not result:
            await bot.send_message(msg.chat.id, "сервис поддерживает адреса только из России, введите адрес корректно")
            await  state.set_state(States.TO_ME_ST)
            return -1

        for row in result:
            value = row['value']
            current_value = value
            dadata = DadataAsync(token, secret)
            try:
                result = await dadata.clean("address", current_value)
            except:
                await bot.send_message(msg.chat.id,
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
        id = msg.chat.id

        shop_id = id_of_min
        str2 = int(d_min)
        for addr_id in shop_list:
            rw = get_query_all("select shop_id, addr from shop_addr where addr_id = %s;", (addr_id,))
            shop_id = (rw[0]).__str__()
            print(shop_id)
            addr = rw[1]
            shop_name = get_query("select shop_name from shops where shop_id = %s;", (shop_id,))
            tmp_keys.add(
                shop_name + ' адрес ' + str(addr) + ' расстояние: ' + str(round(dict_of_shops[addr_id])) + 'км')
            print()
            print("!!")
        tmp_keys.row("🟥↩️главное меню↩️🟥")
        await bot.send_message(msg.chat.id, "ниже представлены магазины и их адреса", reply_markup=tmp_keys)
        await state.set_state(States.GEO_PROVE)
        return 1
        # end

    flo = msg.text
    i = flo.find(' ')
    flor = flo[:i]
    cnt = 0
    for key in regex_dict:
        res = re.search(regex_dict[key], flor)
        if res:
            cnt += 1

    if cnt == 0:
        await bot.send_message(msg.chat.id, "выберите цветы")
        return -1

    # await send_video_instruction(msg, 'order_caption', "correct_data")
    id = msg.chat.id

    sqlin = ("update flobot.orders"
             " set order_caption = %s"
             "where client_order_id = '%s';")
    value = (flor, id)
    commit_query(sqlin, value)
    # здесь часть про показать букеты

    cnx = connect()

    cursor = cnx.cursor()

    sqlin = ("select order_cost, order_caption, len, shop_order_id "
             "from flobot.orders "
             "where client_order_id = '%s';")
    value = (msg.chat.id,)
    cursor.execute(sqlin, value)
    # cnx.commit()
    mcost = cursor.fetchone()
    add_cost = 0

    cost = mcost[0]
    capture = mcost[1]
    distance = mcost[2]
    shop_id = mcost[3]
    cnx.close()

    if distance > 1.4:
        add_cost = (int(distance) - 1.4) * 50
        print(distance, add_cost, "dist + add")

    number = 0
    PRICE = types.LabeledPrice(label='букет ' + capture, amount=0)

    await bot.send_message(msg.chat.id, "ознакомьтесь с каталогом магазина:", reply_markup=REP_KEY_WHEN_INLINE)
    i = 0

    cnx = connect()

    cursor = cnx.cursor()

    sqlin = ("select id, file_id, caption, categories, cost "
             "from flobot.products "
             "where shop_id = '%s' and cost <='%s' or default_bucket is True;")
    value = (shop_id, cost)
    cursor.execute(sqlin, value)
    flowers = cursor.fetchall()

    for current in flowers:
        print(current[0], current[4])
        flag = 0
        flagflo = 0
        PRICE.amount = (int(current[4]) + int(add_cost))
        # * 100
        print(distance, add_cost, PRICE.amount, "qq")
        try:
            flower = re.search(regex_dict[capture], current[3])
        except:
            continue
        print(flower, "@@@@@@@@@@@@@@@@@")
        if flower:
            flagflo = 1

        if flagflo:
            number += 1
            kb1 = types.InlineKeyboardMarkup()
            bm1 = types.InlineKeyboardButton("+", callback_data='button1')
            bm2 = types.InlineKeyboardButton("-", callback_data='button2')

            kb1.add(bm1, bm2)
            ch = await bot.send_photo(msg.chat.id, photo=current[1], caption=current[2] + " цена:" + str(
                current[4]) + "\nдоставка:" + " уточним у менеджера" + "\n#" + str(current[0]) + "#", reply_markup=kb1)
            ID = ch.photo[-1].file_id
            ID2 = current[1]
            i = int(i) + int(1)
    if i == 0:
        await bot.send_message(msg.chat.id, "видимо магазин не продаёт такие цветы", reply_markup=FLOWER_KEYS)
        await state.set_state(States.FLOWER_CATALOG)
        return -1
    await state.set_state(States.CART)
    print(i)
    await send_video_instruction(msg, 'ordering', 'ordering')
    commit_query("update orders set ordering = 'yes' where client_order_id = %s", (msg.chat.id,))


@dp.message_handler(state=States.DATETIME1)
async def datetime1(msg: types.Message, state=FSMContext):
    state = dp.current_state(user=msg.chat.id)
    if msg.text == "нет, продолжить дальше":

        key = types.ReplyKeyboardMarkup(True, True)

        key.add("☆ ↩️ Назад ↩️ ☆")
        await bot.send_message(msg.chat.id, "уточните номер дома и квартиру для заказа", reply_markup=key)
        await state.set_state(States.HOME_NUM)
        sql = "select client_phone from clients where client_chat_id = {}".format(msg.chat.id)
        cnx = connect()
        curs = cnx.cursor()
        curs.execute(sql)
        info = curs.fetchone()
        print(info)

        if info[0] is None:
            print('vid')
            # vid = test_bot_videos[state]
            vid = bot_videos['phone']
            await bot.send_video(msg.chat.id, vid)

        await state.set_state(States.HOME_NUM)

    elif msg.text == "да, хочу назначить время":
        await msg.answer("на какой день вы хотите назначить доставку? введите дату в формате \"15.01.2020\"",
                         reply_markup=types.ReplyKeyboardMarkup(True, True).row("сегодня", "завтра"))
        await state.set_state(States.DATETIME2)


@dp.message_handler(state=States.DATETIME2)  # @dp.message_handler(state=States.DATETIME2)
async def datetime2(msg: types.Message, state=FSMContext):
    state = dp.current_state(user=msg.chat.id)
    if msg.text == "сегодня":
        dtm = datetime.now()
        print(dtm)
        await msg.answer(
            "хорошо, а время? не раньше {}:{} и не позже 21:00 (Мы работаем с 9:00 до 21:00, напишите точное время)".format(
                datetime.now().hour + 1, datetime.now().minute))
        await state.set_state(States.DATETIME3)

    elif msg.text == "завтра":
        dtm = datetime.now()
        print(dtm)
        await msg.answer(
            "хорошо, а время? не раньше 9:00 и не позже 21:00")
        await state.set_state(States.DATETIME3)

    else:
        res = datetime.strptime(msg.text, "%d.%m.%Y")
        print(res)
        await msg.answer("хорошо, а время? не раньше 9:00 и не позже 21:00")
        await state.set_state(States.DATETIME3)


@dp.message_handler(state=States.DATETIME3)  # @dp.message_handler(state=States.DATETIME2)
async def datetime2(msg: types.Message, state=FSMContext):
    state = dp.current_state(user=msg.chat.id)
    try:
        time = datetime.strptime(msg.text, "%H:%M")  # todo datetime
    except:
        await msg.answer("введите время в формате 10:00")
        return -1
    key = types.ReplyKeyboardMarkup(True, True)
    key.add("☆ ↩️ Назад ↩️ ☆")
    await bot.send_message(msg.chat.id, "уточните номер дома и квартиру для заказа", reply_markup=key)
    await state.set_state(States.HOME_NUM)


@dp.message_handler(state=States.HOME_NUM, content_types=types.ContentTypes.ANY)  # out: PHONE_CATALOG
async def home_num(msg: types.Message, state=FSMContext):
    number = msg.text[:24]

    if msg.text == "☆ ↩️ Назад ↩️ ☆":
        await state.set_state(States.DATETIME1)
        key = types.ReplyKeyboardMarkup(True, True)
        key.row("нет, продолжить дальше")
        key.row("да, хочу назначить время")
        # key.add(button_phone)

        await bot.send_message(msg.chat.id, "✨букет передадут курьеру как только соберут\n "
                                            "хотите назначить конкретное время доставки?",
                               reply_markup=key)
        return 1

    state = dp.current_state(user=msg.chat.id)
    # alter table orders add column home_num varchar(25);

    commit_query("update orders set home_num = %s where client_order_id = %s;", (number, msg.chat.id))
    key = types.ReplyKeyboardMarkup(True, True).add(button_phone)
    key.add("☆ ↩️ Назад ↩️ ☆")
    await bot.send_message(msg.chat.id,
                           "осталось самое малое - ваш номер, можете прислать его в формате 88008454545, без тире, или воспользоваться кнопкой внизу",
                           reply_markup=key)
    await state.set_state(States.ONLY_PHONE)


@dp.message_handler(state=States.ONLY_PHONE, content_types=types.ContentTypes.ANY)
async def PHONE_CATALOG(msg: types.Message, state=FSMContext):
    print("PHONE_CATALOG")
    state = dp.current_state(user=msg.chat.id)
    if msg.text == "☆ ↩️ Назад ↩️ ☆":
        await msg.answer("назад")
        await state.set_state(States.DATETIME1)
        key = types.ReplyKeyboardMarkup(True, True)
        key.row("нет, продолжить дальше")
        key.row("да, хочу назначить время")
        # key.add(button_phone)

        await bot.send_message(msg.chat.id, "✨букет передадут курьеру как только соберут\n "
                                            "хотите назначить конкретное время доставки?",
                               reply_markup=key)
        return 1

    try:
        if msg.chat.id == msg['contact']["user_id"]:
            id = msg.chat.id

            sqlin = ("update flobot.clients"
                     " set client_phone = %s"
                     "where client_chat_id = '%s';")
            value = (msg['contact']["phone_number"], id)
            commit_query(sqlin, value)

            ans = types.ReplyKeyboardMarkup(True, True)
            # ans.row("ОФОРМИТЬ ЗАКАЗ", "ИСКАТЬ НАИЛУЧШУЮ ЦЕНУ")

            ans.row("💰 ИСКАТЬ НАИЛУЧШУЮ ЦЕНУ 💰")
            ans.row("☆ ↩️ Назад ↩️ ☆", "★ ⬆️ В начало ⬆️ ★")
            await bot.send_message(msg.chat.id, "🤩Спасибо🤩" + msg.chat.first_name, reply_markup=ans)
            await state.set_state(States.TRUE_ORDERING)
    except:

        print("without contact")

        try:
            number = re.search("^((\+7|7|8)+([0-9]){10})$", msg.text)

            id = msg.chat.id

            sqlin = ("update flobot.clients"
                     " set client_phone = %s"
                     "where client_chat_id = '%s';")
            value = (number[0], id)
            commit_query(sqlin, value)
            ans = types.ReplyKeyboardMarkup(True, True)
            # ans.row("ОФОРМИТЬ ЗАКАЗ", "ИСКАТЬ НАИЛУЧШУЮ ЦЕНУ")
            ans.row("💰 ИСКАТЬ НАИЛУЧШУЮ ЦЕНУ 💰")
            ans.row("☆ ↩️ Назад ↩️ ☆", "★ ⬆️ В начало ⬆️ ★")
            await bot.send_message(msg.chat.id, "🤩Спасибо🤩" + msg.chat.first_name, reply_markup=ans)
            await state.set_state(States.TRUE_ORDERING)

        except:
            print("error parse phone number")
            await bot.send_message(msg.chat.id,
                                   "вы неверно ввели телефон, можете прислать его в формате 88008454545, без тире, или воспользоваться кнопкой внизу")
            return -1


@dp.message_handler(state=States.TRUE_ORDERING, content_types=types.ContentTypes.ANY)  # true оформление заказа
async def PHONE_CATALOG(msg: types.Message, state=FSMContext):
    if msg.text == "☆ ↩️ Назад ↩️ ☆":
        await msg.answer("назад")
        await state.set_state(States.DATETIME1)
        key = types.ReplyKeyboardMarkup(True, True)
        key.row("нет, продолжить дальше")
        key.row("да, хочу назначить время")
        # key.add(button_phone)

        await bot.send_message(msg.chat.id, "✨букет передадут курьеру как только соберут\n "
                                            "хотите назначить конкретное время доставки?",
                               reply_markup=key)
        return 1

    elif msg.text == "💰 ИСКАТЬ НАИЛУЧШУЮ ЦЕНУ 💰":
        # await auction(order_id) # todo auction
        print("first place")
        final_offer = ''
        order = list_of_orders[0]
        data = await state.get_data()
        curr_id = data["curr_order_id"]
        print("data={}".format(data))
        for ord in list_of_orders:
            if ord.get_order_id() == curr_id:
                order = ord
                break

        task = asyncio.create_task(auction(order.get_order_id()))
        kb = types.InlineKeyboardMarkup()
        auct = types.InlineKeyboardButton(callback_data='auction', text="сделаем дешевле")
        kb.add(auct)
        managers = order.get_list_of_managers()

        offer, array_of_images = order.make_offer()
        print(offer)
        print(array_of_images)
        print(managers)
        for mngr in managers:
            if len(array_of_images) > 1:
                media = types.MediaGroup()
                for file_id in array_of_images:
                    media.attach_photo(file_id, "букет")
                try:
                    await bot.send_media_group(mngr, media)
                    await bot.send_message(mngr, offer, reply_markup=kb)  #
                except:

                    await bot.send_message(ADMIN_CHAT_ID, "менеджер {} is blocked now".format(mngr))
                    print("менеджер {} is blocked now".format(mngr))
                    continue
            else:
                try:
                    await bot.send_photo(mngr, array_of_images[0], offer, reply_markup=kb)  #
                except:
                    await bot.send_message(ADMIN_CHAT_ID, "менеджер {} is blocked now".format(mngr))
                    print("менеджер {} is blocked now".format(mngr))
                    continue
            try:
                men_state = dp.current_state(user=mngr, chat=mngr)
                await men_state.set_state(States.auctions)
                await bot.send_message(mngr, "вы можете поучаствовать в английском аукционе, "
                                         "клиент прислал заказ - сможете собрать подобный "
                                         "букет дешевле - заказ уйдет вам")
            except:
                await bot.send_message(ADMIN_CHAT_ID, "менеджер {} is blocked now".format(mngr))
                print("менеджер {} is blocked now".format(mngr))


        await msg.answer("аукцион идёт, подождите минутку, магазины уже сражаются за ваш заказ")




@dp.callback_query_handler(lambda c: c.data == 'button1', state='*')
async def process_callback_add(callback_query: types.CallbackQuery):
    state = dp.current_state(user=callback_query.from_user.id)
    print("добавление")

    await bot.answer_callback_query(callback_query.id, "add")
    caption = callback_query["message"]["caption"]
    client_id = callback_query["from"]["id"]

    sql = "select add_flowers from orders where client_order_id = {}".format(client_id)
    cnx = connect()
    curs = cnx.cursor()
    curs.execute(sql)
    info = curs.fetchone()
    print(info)
    if info[0] is None:
        print('vid')
        # vid = test_bot_videos[state]
        vid = bot_videos['add_flowers']
        await bot.send_video(client_id, vid)
        commit_query("update orders set add_flowers = 'yes' where client_order_id = %s;",
                     (callback_query.from_user.id,))
    cur_cost = 10000
    reg = "#[0-9]+#"
    result = re.findall(reg, caption)
    regg = "[0-9]+"
    res = re.search(regg, result[0])
    print(res[0])
    product_id = res[0]
    prdct_id = int(product_id)
    #
    cnx = connect()

    cursor = cnx.cursor()

    sql = ("select amount, client_id from flobot.cart where product_id = '%s' and client_id ='%s';")
    cursor.execute(sql, (prdct_id, client_id))
    row = cursor.fetchone()

    if row == None:
        cnx.close()
        sqlin = ("insert into flobot.cart(client_id, product_id, amount)"
                 " values ('%s','%s', '%s');")
        value = (client_id, prdct_id, 1)
        commit_query(sqlin, value)
    else:
        cnx.close()
        sqlin = ("update flobot.cart"
                 " set amount='%s' where product_id = '%s' and client_id ='%s';")
        value = (row[0] + 1, prdct_id, client_id)
        commit_query(sqlin, value)
    await state.set_state(States.CART)
    await bot.send_message(callback_query.from_user.id, "добавил букет в вашу корзину",
                           reply_markup=REP_KEY_WHEN_INLINE)


@dp.callback_query_handler(lambda c: c.data == 'button2', state='*')
async def process_callback_delete(callback_query: types.CallbackQuery):
    print("удаление")
    await bot.answer_callback_query(callback_query.id, "rm")
    caption = callback_query["message"]["caption"]
    client_id = callback_query["from"]["id"]

    reg = "#[0-9]+#"
    result = re.findall(reg, caption)
    regg = "[0-9]+"
    res = re.search(regg, result[0])
    product_id = res[0]
    prdct_id = int(product_id)
    curr_amount = 1
    #
    cnx = connect()

    cursor = cnx.cursor()

    sql = ("select amount, client_id from flobot.cart where product_id = '%s' and client_id ='%s';")
    cursor.execute(sql, (prdct_id, client_id))
    row = cursor.fetchone()
    curr_amount = int(row[0]) - 1
    print(curr_amount)
    cnx.close()
    if row == None:
        cnx.close()
        await bot.send_message(client_id, "их там и не было")
    else:
        cnx.close()
        if curr_amount == 0:

            cnx = connect()

            cursor = cnx.cursor()

            sqlin = ("delete from flobot.cart "
                     "where product_id = '%s' and client_id ='%s';")
            cursor.execute(sqlin, (prdct_id, client_id))
            cnx.commit()
            cnx.close()

        else:
            sqlin = ("update flobot.cart"
                     " set amount='%s' where product_id = '%s' and client_id ='%s';")
            value = (curr_amount, prdct_id, client_id)
            commit_query(sqlin, value)

    await bot.send_message(callback_query.from_user.id, "убрал букет из вашей корзины")
    cnx.close()


@dp.message_handler(state=States.CART)  # корзина
async def cart(msg: types.Message, state=FSMContext):
    print("States.CART^^")
    state = dp.current_state(user=msg.chat.id)
    if msg.text == "☆ ↩️ Назад ↩️ ☆":
        data = await state.get_data()
        no_duplicate_list_of_shop = data["list_of_shops"]
        print("data={}".format(data))
        cost_str = data["cost"]
        user_id = msg.chat.id
        await bot.send_message(user_id, "выберите категорию цветов")
        # searching shops
        key_dict = {}
        cost = int(cost_str)
        print("cost={}".format(cost))
        i = 1
        for shop_id in no_duplicate_list_of_shop:
            print("shop_id={}".format(shop_id))
            cnx = connect()
            curs = cnx.cursor()
            if i == 1:
                curs.execute(
                    "select categories from products where (shop_id = %s and cost <= %s) or (default_bucket is true and cost <=%s);",
                    (shop_id, cost, cost,))
            else:
                curs.execute(
                    "select categories from products where shop_id = %s and cost <= %s;",
                    (shop_id, cost,))
            products = curs.fetchall()
            for row in products:
                categ = row[0]
                print(categ)
                for key in regex_dict:
                    res = re.search(regex_dict[key], categ)
                    if res is not None and len(res[0]) > 1:
                        try:
                            print("res.search {}".format(key))
                            key_dict[key] += 1
                        except:
                            print("add_new_categ {}".format(key))
                            key_dict.update({key: 1})
            i = 0
        print(key_dict)

        keys = types.ReplyKeyboardMarkup(True, True)
        print(len(key_dict))
        for k in key_dict:
            keys.add(types.KeyboardButton(str(k) + ' ' + str(key_dict[k])))
            print(k, key_dict[k])

        keys.row("☆ ↩️ Назад ↩️ ☆")
        await state.set_state(States.FAST_SEARCH_CATALOG)
        await bot.send_message(user_id,
                               "🔥💐Отлично,выберите нужный цветок",
                               reply_markup=keys)

    elif msg.text == "🔥 корзина 💰":
        kb = types.InlineKeyboardMarkup()
        print("корзина")
        cnx = connect()

        cursor = cnx.cursor()

        sqlin = (
            "select cart.id, cart.product_id, cart.amount, products.caption from flobot.cart left join flobot.products on cart.product_id = products.id where client_id = %s;")
        value = (msg.chat.id,)
        cursor.execute(sqlin, value)
        row = cursor.fetchall()
        print(row)
        if not row:
            await bot.send_message(msg.chat.id, "кажется ваша корзина пуста\nсперва добавьте туда что-нибудь",
                                   reply_markup=REP_KEY_WHEN_INLINE)
            await state.set_state(States.CART)
            cnx.close()
            return -1

        str1 = ""
        for i in row:  # todo всратый нейминг
            str1 = str1 + str(i[3]) + " шт: " + str(i[2]) + '\n'


        ans = types.ReplyKeyboardMarkup(True, True)
        ans.row("🔥 перейти к оформлению 🔥")
        ans.row("☆ ↩️ Назад ↩️ ☆", "★ ⬆️ В начало ⬆️ ★")
        await bot.send_message(msg.chat.id, str1, reply_markup=ans)
        await state.set_state(States.ORDERING_BUCKET)

    elif msg.text == "★ ⬆️ В начало ⬆️ ★":
        await msg.reply("используйте клавиатуру ниже:", reply_markup=INIT_KEYBOARD)
        await state.set_state(States.AFT_INIT_STATE)
        return -1
    elif msg.text == "мои заказы":  # todo "мои заказы"
        print("q")
        await bot.send_message(msg.chat.id, "ваши заказы")


@dp.message_handler(state=States.ORDERING_BUCKET)  # оформить заказ/искать наилучшую цену
async def cart(msg: types.Message, state=FSMContext):
    state = dp.current_state(user=msg.chat.id)
    if msg.text == "★ ⬆️ В начало ⬆️ ★":
        sql = ("delete from flobot.cart where client_id = '%s';")
        value = (msg.from_user.id,)
        commit_query(sql, value)

        await msg.reply("используйте клавиатуру ниже:", reply_markup=INIT_KEYBOARD)
        await state.set_state(States.AFT_INIT_STATE)
        return -1

    elif msg.text == "☆ ↩️ Назад ↩️ ☆":
        await bot.send_message(msg.chat.id, "выберите что-нибудь из каталога:", reply_markup=REP_KEY_WHEN_INLINE)
        await bot.delete_message(msg.chat.id, msg.message_id)
        await bot.delete_message(msg.chat.id, msg.message_id - 1)
        await bot.delete_message(msg.chat.id, msg.message_id - 2)

        await state.set_state(States.CART)
        return -1


    elif msg.text == "🔥 перейти к оформлению 🔥":
        print("создание заказа")
        cnx = connect()
        cursor = cnx.cursor()
        sqlin = (
            "select cart.id, cart.product_id, cart.amount, products.caption from flobot.cart left join flobot.products on cart.product_id = products.id where client_id = %s;")
        value = (msg.chat.id,)
        cursor.execute(sqlin, value)

        row = cursor.fetchall()

        if not row:
            await bot.send_message(msg.chat.id, "кажется ваша корзина пуста\nсперва добавьте туда что-нибудь",
                                   reply_markup=REP_KEY_WHEN_INLINE)
            await state.set_state(States.CART)
            cnx.close()
            return -1

        list_of_product_and_amount = []
        for i in row:  # todo всратый нейминг
            prod = product(i[1])
            pair = [prod, i[2]]
            list_of_product_and_amount.append(pair)

        print("list_of_product_and_amount={}".format(list_of_product_and_amount))
        cnx.close()
        data = await state.get_data()

        list_of_shop = data["list_of_shops"]
        print("data={}".format(data))
        user_id = msg.chat.id
        ordr = order(user_id, list_of_shop, list_of_product_and_amount)
        print("ordr.get_curr_cost()={}".format(ordr.get_curr_cost()))
        list_of_orders.append(ordr)
        print("list_of_orders={}".format(list_of_orders))
        await state.update_data(curr_order_id=ordr.get_order_id())
        await state.set_state(States.DATETIME1)
        key = types.ReplyKeyboardMarkup(True, True)
        key.row("нет, продолжить дальше")
        key.row("да, хочу назначить время")

        await bot.send_message(msg.chat.id, "✨букет передадут курьеру как только соберут\n "
                                            "хотите назначить конкретное время доставки?",
                               reply_markup=key)
        await send_video_instruction(msg, 'order_shipping_adress', 'delivery')

    else:
        ans = types.ReplyKeyboardMarkup(True, True)
        # ans.row("ОФОРМИТЬ ЗАКАЗ", "ИСКАТЬ НАИЛУЧШУЮ ЦЕНУ")
        ans.row("💰 ИСКАТЬ НАИЛУЧШУЮ ЦЕНУ 💰")
        ans.row("☆ ↩️ Назад ↩️ ☆", "★ ⬆️ В начало ⬆️ ★")
        await state.set_state(States.ORDERING_BUCKET)
        await bot.send_message(msg.chat.id, "Упс, я не понял... Пожалуйста, напишите название как-нибудь по-другому 🙏",
                               reply_markup=ans)


@dp.callback_query_handler(lambda c: c.data == 'disapprove', state='*')
async def process_callback_disarm(callback_query: types.CallbackQuery, state=FSMContext):
    print("dis")
    await bot.answer_callback_query(callback_query.id, "dis")
    await bot.send_message(callback_query.from_user.id,
                           "товар отсутствует, клиент проинформирован")
    mid = callback_query.message.message_id
    txt = caption = callback_query["message"]["caption"]
    print(txt)
    result1 = txt.find(":")
    result2 = txt.find("\n")
    id_pay = txt[result1 + 1:result2]
    print(id_pay)
    cnx = connect()

    cursor = cnx.cursor()
    sql = ("delete from flobot.cart"
           " where id = %s;")
    value = (id_pay,)
    commit_query(sql, value)
    txxt = txt[result2:]

    cursor.execute(sql, value)
    print("!!", cnx.commit())
    result = txxt.find("\n")
    ttxt = txt[result:]
    print(ttxt)
    photo_id = callback_query["message"]["photo"][0]["file_id"]
    await bot.send_message(int(txt[:result]), "следующий товар отсутствует:")
    await bot.send_photo(int(txt[:result]), photo_id, caption)
    cnx.close()


@dp.callback_query_handler(lambda c: c.data == 'prove', state='*')
async def process_callback_add(callback_query: types.CallbackQuery):
    print("prove")
    await callback_query.answer("prove")
    await bot.answer_callback_query(callback_query.id, "prove")
    mid = callback_query.message.message_id
    txt = caption = callback_query["message"]["caption"]
    print(txt)
    result1 = txt.find(":")
    result2 = txt.find("\n")
    id_pay = txt[result1 + 1:result2]
    print(id_pay)
    cnx = connect()

    cursor = cnx.cursor()
    sql = ("update flobot.cart"
           " set cart.st=%s where id = '%s';")
    value = ("prove", int(id_pay))
    txxt = txt[result2:]
    cursor.execute(sql, value)
    print("!!", cnx.commit())
    result = txxt.find("\n")
    ttxt = txt[result:]
    print(ttxt)
    kb = types.InlineKeyboardMarkup()
    bm2 = types.InlineKeyboardButton("нет в наличии", callback_data='disapprove')
    kb.add(bm2)
    # callback_query.
    await bot.edit_message_reply_markup(callback_query.from_user.id, mid, reply_markup=kb)
    await bot.send_message(callback_query.from_user.id,
                           "вы подтвердили наличие одного из букетов, как закончите, введите стоимость доставки")
    await bot.send_message(int(txt[:result1]), "подтвердили один из букетов")
    # print(result)
    cnx.close()


@dp.message_handler(state=States.wait_for_delivery_cost)  #
async def wait_for_delivery_cost(msg: types.Message):
    print("wait_for_delivery_cost")
    print(msg.text)
    state = dp.current_state(user=msg.chat.id)
    try:
        delivery_cost = int(msg.text)
    except:
        await msg.answer("введите стоимость корректно")
        return -1

    for z in array:
        if msg.chat.id == z['id_manager']:
            z['cost'] = delivery_cost
    await bot.send_message(msg.chat.id, "хорошо, стоимость доставки:" + msg.text)


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
        ordr = list_of_confirmed_orders[0]

        for order in list_of_confirmed_orders:
            if order.payment_order_id == id:
                order.pay = True
                ordr = order
                break


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

        msg, photo = ordr.make_final_offer()

        cnx.close()


        await bot.send_message(ordr.get_curr_manager(),msg)
        await bot.send_message(ordr.get_curr_manager(), "обязательно свяжитесь с клиентом!")
        for order in list_of_confirmed_orders:
            if order.payment_order_id == payment_id:
                if order.pay:
                    print("{} status=true".format(payment_id))
                else:
                    list_of_confirmed_orders.remove(order)
                    print("{} status=false".format(payment_id))
    else:
        st = types.InlineKeyboardMarkup()
        bn = types.InlineKeyboardButton("проблемы при пользовании", callback_data="helper")
        bn1 = types.InlineKeyboardButton("статус оплаты", callback_data="payment_status")
        st.add(bn, bn1)
        await bot.send_message(callback_query.from_user.id,
                               "оплатите заказ, а если вы уже заплатили - нажмите кнопку 'подтвердить'",
                               reply_markup=st)

        cnx.close()


@dp.callback_query_handler(lambda c: c.data == 'auction', state=States.auctions)
async def process_callback_add(callback_query: types.CallbackQuery):
    print("auction")
    state = dp.current_state(user=callback_query.from_user.id)
    await callback_query.answer("auction")
    await bot.answer_callback_query(callback_query.id, "auction")
    mid = callback_query.message.message_id
    txt = callback_query["message"]["caption"]
    print("txt ={}".format(txt))
    result = re.search("#[0-9]*#", txt)
    board = result.span()
    ordr_id = txt[board[0] + 1:board[1] - 1]
    print(ordr_id)
    await state.update_data(ordr_id=int(ordr_id))
    await bot.send_message(callback_query.from_user.id, "пришлите новую стоимость, числом")


@dp.message_handler(state=States.auctions)
async def cart(msg: types.Message, state=FSMContext):
    cost = msg.text
    result = re.search("[0-9]*", cost)
    board = result.span()
    new_cost = cost[board[0]:board[1]]
    print("new_cost={}".format(new_cost))
    await bot.send_message(msg.chat.id, f"новая стоимость: {new_cost}")
    state = dp.current_state(user=msg.chat.id)
    data = await state.get_data()
    print(data["ordr_id"])
    ordr_id = data["ordr_id"]

    order = list_of_orders[0]

    for ord in list_of_orders:
        if ord.get_order_id() == ordr_id:
            order = ord
            break
    try:
        if not order.change_curr_cost(int(cost)):
            await bot.send_message(msg.chat.id, "введите число корректно")
            return -1

    except:
        await bot.send_message(msg.chat.id, "введите число корректно, только цифры")
    order.change_curr_manager(msg.chat.id)

    kb = types.InlineKeyboardMarkup()
    auct = types.InlineKeyboardButton(callback_data='auction', text="сделаем дешевле")
    kb.add(auct)
    managers = order.get_list_of_managers()

    offer, array_of_images = order.make_offer()
    print(offer)
    print(array_of_images)
    print(managers)
    for mngr in managers:
        if len(array_of_images) > 1:
            media = types.MediaGroup()
            for file_id in array_of_images:
                media.attach_photo(file_id, "букет")
            try:
                await bot.send_media_group(mngr, media)
                await bot.send_message(mngr, offer, reply_markup=kb)  #
            except:
                await bot.send_message(ADMIN_CHAT_ID, "менеджер {} is blocked now".format(mngr))
                print("менеджер {} is blocked now".format(mngr))
        else:
            try:
                await bot.send_photo(mngr, array_of_images[0], offer, reply_markup=kb)  #
            except:
                await bot.send_message(ADMIN_CHAT_ID, "менеджер {} is blocked now".format(mngr))
                print("менеджер {} is blocked now".format(mngr))

        try:
            men_state = dp.current_state(user=mngr, chat=mngr)
            await men_state.set_state(States.auctions)
            await bot.send_message(mngr, "вы можете поучаствовать в английском аукционе, "
                                     "клиент прислал заказ - сможете собрать подобный "
                                     "букет дешевле - заказ уйдет вам")
        except:
            await bot.send_message(ADMIN_CHAT_ID, "менеджер {} is blocked now".format(mngr))
            print("менеджер {} is blocked now".format(mngr))

@dp.message_handler(state=States.auctions1)  # send_invoice
async def auctions1(msg: types.Message, state=FSMContext):
    print("auctions1")
    cost = msg.text
    result = re.search("[0-9]*", cost)
    if not result:
        await bot.send_message(msg.chat.id, "введите число корректно")
        return -1

    board = result.span()
    delivery_cost = cost[board[0]:board[1]]

    state = dp.current_state(user=msg.chat.id)
    data = await state.get_data()
    print("data={}".format(data))
    ordr_id = data["ordr_id"]

    order = list_of_orders[0]

    for ord in list_of_orders:
        if ord.get_order_id() == ordr_id:
            order = ord
            break

    mngr = order.get_curr_manager()
    client = order.get_client_id()

    await bot.send_message(ADMIN_CHAT_ID, order.get_curr_cost())
    order.set_delivery_cost(delivery_cost)
    final_cost = order.get_curr_cost()
    final_offer, photo = order.make_client_offer()
    amount = 1

    cnx = connect()
    cursor = cnx.cursor()
    sqlinn = (""" select client_id from successful_payment where status = 'CONFIRMED' and client_id = %s; """)
    v = (order.get_client_id(),)
    cursor.execute(sqlinn, v)
    first_gift = cursor.fetchall()
    print("first_gift={}", first_gift)

    cnx = connect()
    cursor = cnx.cursor()
    shop_id = order.get_curr_shop()
    ordr_id = 0
    Items = []
    shops = []
    print(shop_id)
    # shop_code = get_query("select tink_shop_code from shops where shop_id = %s;", (shop_id,))
    shop_code = 492585
    print("shop_code={}".format(shop_code))
    shiper = {
        "Name": "доставка",
        "Price": int(delivery_cost) * 100,
        "Quantity": 1,
        "Amount": int(delivery_cost) * 100,  # price * quantity
        "Tax": "vat10",
        "ShopCode": shop_code
    }

    Items.append(shiper)

    list_of_prod = order.get_list_of_prod()
    cnt = len(list_of_prod)
    for pair in list_of_prod:
        prod = pair[0]
        Quantity = pair[1]

        product = {
            "Name": "",
            "Price": 0,
            "Quantity": 0,
            "Amount": 0,  # price * quantity
            "Tax": "vat10",
            "ShopCode": ""
        }

        product["Name"] = prod.get_caption()

        if first_gift:
            product["Price"] = int(int(order.get_curr_cost()) / cnt) * 100
        else:
            product["Price"] = int(int(order.get_curr_cost()) / cnt) * 70  # 50
        # final_cost += int(row[2]) * int(row[3]) * 0.7  # 0.5

        product["Quantity"] = int(Quantity)
        product["Amount"] = int(product["Price"]) * int(product["Quantity"])
        product["ShopCode"] = str(shop_code)  # str(row[6])
        print(product)
        Items.append(product)

    for i in Items:
        print("curr_item = {}".format(i))

    cnx = connect()
    curs = cnx.cursor()
    curs.execute("select id from successful_payment order by id desc;")
    ordr = curs.fetchone()
    ordr_id = int(ordr[0]) + 1
    Amount = 0
    for i in Items:
        Amount += int(i["Price"]) * int(i["Quantity"])
    shops = [
        {
            "ShopCode": shop_code,  # row[6]
            "Amount": Amount,
            "Name": "букеты"
        },
    ]

    from tink_payment import payment
    pay = payment("1615725763495", "2illo2v6pxz3brce")  # TODO upd config.py ("1615725763495", "n2YLD8x0hd")
    print("Items={}".format(Items))
    resp, amount_from_tink = pay.init_pay(shops, Items, ordr_id)
    print("resp={}".format(resp))
    if resp['Success'] == False:
        print("error failure payment")
        await bot.send_message(msg.chat.id, "error failure payment\ntype '\help'")
    else:
        confirmation_url = resp["PaymentURL"]
        c = str(float(final_cost))
        str_inv = "Pay: " + str(amount_from_tink) + " RUB"
        print(str_inv, "qq")
        inv = types.InlineKeyboardMarkup()
        bm1 = types.InlineKeyboardButton(str_inv, url=confirmation_url)
        inv.add(bm1)
        cnx.close()
        import time
        print(time.strftime('%Y-%m-%d %H:%M:%S'))
        await bot.send_message(int(order.get_client_id()), final_offer, reply_markup=inv)

        sqlin = (
            "insert into flobot.successful_payment(provider_payment_charge_id, caption, cost, client_id, status, create_at, shop_id)"
            "values (%s, %s, %s, %s, %s, %s, %s);")
        value = (resp['PaymentId'], final_offer, float(final_cost), int(order.get_client_id()), resp["Status"],
                 time.strftime('%Y-%m-%d %H:%M:%S'), shop_id)
        commit_query(sqlin, value)

        cnx = connect()

        cursor = cnx.cursor()

        sql = ("select id from flobot.successful_payment where provider_payment_charge_id = %s;")
        cursor.execute(sql, (resp['PaymentId'],))
        row = cursor.fetchone()
        kb1 = types.InlineKeyboardMarkup()
        bm2 = types.InlineKeyboardButton("подтвердить", callback_data="invoice")
        kb1.add(bm2)
        list_of_confirmed_orders.append(order)
        print("order.get_order_id()={}".format(order.get_order_id()))
        await bot.send_message(order.get_client_id(),
                               "не забудьте вернуться к нам и подтвердить свою оплату заказа " + str(
                                   row[0]) + "! иначе не дождётесь свой букет))", reply_markup=kb1)
        order.set_payment_order_id(int(row[0]))
        cnx.close()
        task = asyncio.create_task(payment_cooldown(order.payment_order_id))
        await bot.send_message(order.get_curr_manager(),
                               "вы все сделали правильно, клиент уже направлен на оплату")
        await bot.send_message(order.get_curr_manager(),
                               "как только клиент подтвердит оплату - вам придут его контактные данные и точный адрес доставки")
