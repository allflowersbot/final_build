import config
from loader import dp, bot, instagram_basic_display
from config import *
import re
from keyboards import INIT_KEYBOARD
from utils import States
from aiogram import types
from dbcm import connect, commit_query, get_query

@dp.message_handler(state='*', commands=['new_shop'])  # done
async def vidget(msg: types.Message):
    state = dp.current_state(user=msg.chat.id)
    await bot.send_message(msg.chat.id, "new shop")
    message = "прежде чем добавить свой магазин, ознакомьтесь с правилами оферты и политикой конфиденциальности на нашем сайте:" \
              "\n https://allflowersbot.github.io/allflowers/term\n" \
              "https://allflowersbot.github.io/allflowers/Oferta\n"
    kb1 = types.InlineKeyboardMarkup()
    bm1 = types.InlineKeyboardButton("✅да, принимаю🖌", callback_data='S_PP_conf')
    bm2 = types.InlineKeyboardButton("нет, не принимаю", callback_data='S_PP_NOT')
    bm3 = types.InlineKeyboardButton("регистрация магазина без инстаграма", callback_data='not_inst')

    kb1.add(bm1, bm2)
    kb1.add(bm3)
    await bot.send_message(msg.chat.id,
                           message + "согласны ли вы с выше изложенными документами и принимаете соглашение?",
                           reply_markup=kb1)
    await state.set_state(States.NS0)

@dp.callback_query_handler(lambda c: c.data == 'not_inst', state=States.NS0)  # done
async def not_inst(callback_query: types.CallbackQuery):
    await callback_query.answer("without_inst")
    state = dp.current_state(user=callback_query.from_user.id)
    await bot.send_message(callback_query.from_user.id, "new shop without instagram")
    kb = types.ReplyKeyboardMarkup(True, True)
    kb.row("В начало")
    await bot.send_message(callback_query.from_user.id, "введите название своего магазина", reply_markup=kb)
    await state.set_state(States.Not_Inst)


@dp.message_handler(state=States.Not_Inst)
async def Not_Inst(msg: types.Message):
    state = dp.current_state(user=msg.chat.id)
    if msg.text == "В начало":
        await bot.send_message(msg.chat.id, "начнем заново", reply_markup=INIT_KEYBOARD)
        await state.set_state(States.AFT_INIT_STATE)
        return -1
    kb1 = types.InlineKeyboardMarkup()
    bm1 = types.InlineKeyboardButton("правильно", callback_data='NICN')
    bm2 = types.InlineKeyboardButton("нет, не правильно", callback_data='NINCN')
    kb1.add(bm1, bm2)
    await msg.answer(msg.text + "<- название вашего магазина", reply_markup=kb1)
    await state.set_state(States.Not_Inst1)

@dp.message_handler(state=States.Not_Inst1)
async def Not_Inst1(msg: types.Message):
    state = dp.current_state(user=msg.chat.id)
    if msg.text == "В начало":
        await bot.send_message(msg.chat.id, "начнем заново", reply_markup=INIT_KEYBOARD)
        await state.set_state(States.AFT_INIT_STATE)


@dp.callback_query_handler(lambda c: c.data == 'NICN', state=States.Not_Inst1)
async def process_callback_add(callback_query: types.CallbackQuery):
    await callback_query.answer("without_inst")
    state = dp.current_state(user=callback_query.from_user.id)
    await bot.send_message(callback_query.from_user.id, "хорошо, продолжите регистрация")

    name = callback_query.message.text
    print(name)
    i = name.find("<- н")
    full_name = name[:i]
    sql = ("insert into flobot.shops(shop_name, manager_chat_id, num_of_adress) "
           "values(%s, '%s', '%s');")
    value = (full_name, callback_query.message.chat.id, 1)
    commit_query(sql, value)

    sql2 = (" select shop_id from flobot.shops where manager_chat_id = %s ;")

    value2 = (callback_query.message.chat.id,)

    shop_id = get_query(sql2, value2)

    sql1 = ("insert into flobot.managers(shop_id, manager_chat_id) "
            "values('%s', '%s');")
    value1 = (shop_id, callback_query.message.chat.id,)

    commit_query(sql1, value1)

    await bot.send_message(callback_query.from_user.id,
                           "ваш магазин зарегистрирован под именем \"" + full_name + '\"' + " пожалуйста сообщите количество магазинов "
                                                                                            "из которых реализуется доставка"
                                                                                            " и их адреса")
    await bot.send_message(callback_query.from_user.id, "для начала количество адресов, цифрой")
    await state.set_state(States.NS2)


@dp.callback_query_handler(lambda c: c.data == 'NINCN', state=States.Not_Inst1)
async def process_callback_add(callback_query: types.CallbackQuery):
    await callback_query.answer("not correct")
    state = dp.current_state(user=callback_query.from_user.id)
    await bot.send_message(callback_query.from_user.id, "new shop without instagram")
    await bot.send_message(callback_query.from_user.id, "введите название своего магазина")
    await state.set_state(States.Not_Inst)


@dp.callback_query_handler(lambda c: c.data == 'S_PP_NOT', state=States.NS0)
async def process_callback_add(callback_query: types.CallbackQuery):
    await callback_query.answer("S_PP_NOT")
    state = dp.current_state(user=callback_query.from_user.id)
    await bot.send_message(callback_query.from_user.id, "возвращайтесь, когда сможете ;D")
    await state.set_state(States.AFT_INIT_STATE)


@dp.callback_query_handler(lambda c: c.data == 'S_PP_conf', state=States.NS0)
async def process_callback_add(callback_query: types.CallbackQuery):
    await callback_query.answer("S_PP_conf")
    state = dp.current_state(user=callback_query.from_user.id)
    await bot.send_message(callback_query.from_user.id, "new shop")
    url = instagram_basic_display.get_login_url()
    await bot.send_message(callback_query.from_user.id, url)
    kb1 = types.InlineKeyboardMarkup()
    bm1 = types.InlineKeyboardButton("подтвердили", callback_data='shop_prove')
    kb1.add(bm1)

    await bot.send_message(callback_query.from_user.id, "перейдите по ссылке и зайдите в инстаграмм аккаунт магазина",
                           reply_markup=kb1)
    await state.set_state(States.NS1)


@dp.callback_query_handler(lambda c: c.data == 'shop_prove', state=States.NS1)
async def process_callback_add(callback_query: types.CallbackQuery):
    await callback_query.answer("shop_prove")
    state = dp.current_state(user=callback_query.from_user.id)
    print("shop_prove")
    try:
        file = open("/root/token/token.txt", "r")
    except:
        print("file_read except")
        return -1

    token = file.read()
    print("token:\n", token)
    short_lived = instagram_basic_display.get_o_auth_token(token)
    long_lived = instagram_basic_display.get_long_lived_token(short_lived.get('access_token'))
    profile = instagram_basic_display.set_access_token(long_lived["access_token"])

    pro = instagram_basic_display.get_user_profile()
    name = pro["username"]
    sql = ("insert into flobot.shops(shop_name, access_token, manager_chat_id, num_of_adress) "
           "values(%s, %s, '%s', '%s');")
    value = (name, long_lived["access_token"], callback_query.message.chat.id, 1)
    commit_query(sql, value)

    sql2 = (" select shop_id from flobot.shops where manager_chat_id = %s ;")

    value2 = (callback_query.message.chat.id,)

    shop_id = get_query(sql2, value2)

    sql1 = ("insert into flobot.managers(shop_id, manager_chat_id) "
            "values('%s', '%s');")
    value1 = (shop_id, callback_query.message.chat.id,)

    commit_query(sql1, value1)

    await bot.send_message(callback_query.from_user.id,
                           "ваш магазин зарегистрирован под именем \"" + name + '\"' + "пожалуйста сообщите количество магазинов "
                                                                                       "из которых реализуется доставка"
                                                                                       " и их адреса")
    await bot.send_message(callback_query.from_user.id, "для начала количество адресов, цифрой")
    await state.set_state(States.NS2)


@dp.message_handler(state=States.NS2)
async def NS(msg: types.Message):
    state = dp.current_state(user=msg.chat.id)
    if msg.text == "В начало":
        await bot.send_message(msg.chat.id, "начнем заново", reply_markup=INIT_KEYBOARD)
        await state.set_state(States.AFT_INIT_STATE)
    print(msg)

    res = re.search("\d{1,2}", msg.text)
    print(res)

    await bot.send_message(
        msg.chat.id, "количество адресов: " + str(res[0])
    )
    sqlin = ("update flobot.shops set num_of_adress = '%s'"
             "where manager_chat_id = '%s';")
    value = (int(res[0]), msg.chat.id)
    commit_query(sqlin, value)
    key = types.ReplyKeyboardMarkup(True, True)
    key.row("завершить")
    key.row("назад, адрес не верен")
    await bot.send_message(
        msg.chat.id,
        "теперь скиньте адрес магазина, если их несколько - по одному в сообщении, в формате \"г. Москва, газгольдерная 10А\"\n"
        "как адреса закончатся - нажмите завершить на :: клавиатуре",
        reply_markup=key)
    await state.set_state(States.NS3)


@dp.message_handler(state=States.NS3)  # @dp.message_handler(state=States.NS3)
async def NS(msg: types.Message):
    state = dp.current_state(user=msg.chat.id)
    i = True
    if msg.text == "завершить":  # if msg.text == "завершить"

        cnx = connect()

        cursor = cnx.cursor()
        sql = ("select shop_name, access_token, shop_id from flobot.shops where manager_chat_id = '%s';")
        cursor.execute(sql, (msg.chat.id,))  # todo требует проверки state!
        curs = cursor.fetchall()
        print(curs)
        for shops in curs:
            if shops[1]:
                instagram_basic_display.set_access_token(shops[1])
                profile = instagram_basic_display.get_user_profile()
                print(profile)
                media = instagram_basic_display.get_user_media(limit=100)  # по заказу - 100
                list = media['data']
                i = 0
                for curr in list:
                    i += 1
                    image = curr['media_url']
                    ff = 100
                    ff = re.search("https://video", image)

                    print(ff)
                    if ff == None:
                        caption = curr['caption']
                        tmp = caption[:255]
                        print(image, i)
                        # time.sleep(0.1)
                        ch = await bot.send_photo(msg.chat.id, image, caption)

                        sql = ("insert into flobot.products(file_id, caption, shop_id, shop)"
                               "values(%s,  %s, %s, %s)")
                        value = (
                            ch.photo[-1].file_id,
                            tmp,
                            shops[2],
                            profile["username"]
                        )

                        commit_query(sql, value)
                        # await bot.delete_message(ch.chat.id, ch.message_id)

        print("finish")
        await bot.send_message(msg.chat.id,
                               "спасибо за сотрудничество! теперь нужно уточнить информацию о продуктах в разделе /manager_mode, сделайте это как можно скорее!)",
                               reply_markup=INIT_KEYBOARD)  # todo

        await state.set_state(States.AFT_INIT_STATE)
    else:
        from dadata import DadataAsync
        token = DADATA_TOKEN
        secret = config.DADATA_SECRET
        dadata = DadataAsync(token)
        result = await dadata.suggest("address", msg.text)
        await dadata.close()
        if not result:
            await bot.send_message(msg.chat.id, "сервис поддерживает адреса только из России, введите адрес корректно")
            await  state.set_state(States.NS3)
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
            break

        sql = ("select shop_id from flobot.shops where manager_chat_id = '%s';")
        value = (msg.chat.id,)
        res = get_query(sql, value)

        sqlin = ("insert into flobot.shop_addr(shop_id, addr, lon, lat) "
                 "values(%s, %s, %s, %s);")
        value = (res, current_value, lon, lat)
        commit_query(sqlin, value)
        kb1 = types.InlineKeyboardMarkup()
        bm1 = types.InlineKeyboardButton("адрес верный", callback_data='addr_true')
        bm2 = types.InlineKeyboardButton("адрес не верный", callback_data='addr_false')

        kb1.add(bm1)
        kb1.add(bm2)

        await bot.send_message(msg.chat.id, "адрес: " + current_value, reply_markup=kb1)
        await state.set_state(States.NS4)


@dp.callback_query_handler(lambda c: c.data == 'addr_false', state=States.NS4)
async def process_callback_add(callback_query: types.CallbackQuery):
    state = dp.current_state(user=callback_query.from_user.id)
    await callback_query.answer("addr_false")
    await bot.send_message(callback_query.from_user.id, "сейчас исправим!")
    print(callback_query["message"]["text"])
    raw_addr = callback_query["message"]["text"]
    i = raw_addr.find("адрес: ")  # 7
    addr = raw_addr[7:]

    sql = (" delete from flobot.shop_addr where addr = %s")
    value = (addr,)
    commit_query(sql, value)

    await bot.send_message(callback_query.from_user.id, "сейчас просто введите адрес правильно) все получится!")
    await state.set_state(States.NS3)


@dp.callback_query_handler(lambda c: c.data == 'addr_true', state=States.NS4)
async def process_callback_add(callback_query: types.CallbackQuery):
    await callback_query.answer("addr_true")
    state = dp.current_state(user=callback_query.from_user.id)
    await bot.send_message(callback_query.from_user.id, "отлично!")
    await state.set_state(States.NS3)

