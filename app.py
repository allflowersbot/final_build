from math import *

from datetime import datetime
import config
import asyncio
import logging
import re
from handlers.reg_shop import regshop
# from async_auction import auction, auctions
from utils import States
from messages import MESSAGES
from aiogram import Bot, types
from aiogram.utils import executor
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types.message import ContentType
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from instagram_basic_display.InstagramBasicDisplay import InstagramBasicDisplay
from keyboards import INIT_KEYBOARD, TO_ME, KEYBOARD3, COST, FLOWER_KEYS, button_phone, regex_dict, TMP, \
    REP_KEY_WHEN_INLINE, manager_mode_keys, manager_mode_edit_keys, tink_reg_keys, \
    manager_mode_keys2, manager_mode_keys1, MAIL
from config import APP_ID, APP_SECRET, REDIRECT_URL, DADATA_TOKEN, BOT_TOKEN, TEST_BOT_TOKEN
from dbcm import commit_query, get_query, connect, get_query_all
from video_instruction import send_video_instruction, bot_videos, test_bot_videos, mailing
ADMIN_CHAT_ID = 392875761
# init
def init():
    print("nachalo")




logging.basicConfig(format=u'%(filename)+13s [ LINE:%(lineno)-4s] %(levelname)-8s [%(asctime)s] %(message)s',
                    level=logging.INFO)
loop = asyncio.get_event_loop()
ID = ""
ID2 = ""
bot = Bot(token=BOT_TOKEN)
# TEST_
dp = Dispatcher(bot=bot, loop=loop, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())

instagram_basic_display = InstagramBasicDisplay(app_id=APP_ID,
                                                app_secret=APP_SECRET,
                                                redirect_url=REDIRECT_URL)

array = []
current_products = []
auctions = []

# auctin_order ={
#     "client_id": 0,
#     "product_id":0,
#     "shop_ids": [],
#     "curr_shop": 0,
#     "curr_manager": 0,
#     "curr_cost": 0,
#     "first_cost": 0,
#     "managers": []
# }


async def auction(order_id):
    await asyncio.sleep(60)
    print("second place")
    for ordr in auctions:
        print(ordr, "all")
        if ordr["client_id"] == order_id:

            state = dp.current_state(user=ordr["curr_manager"], chat=ordr["curr_manager"])
            cnx = connect()
            curs = cnx.cursor()
            curs.execute("select order_shipping_adress from orders where client_order_id = {}".format(order_id))
            addrs = curs.fetchone()
            shipp_addr=addrs[0]
            await bot.send_message(ordr["curr_manager"], "вы выйграли аукцион, укажите стоимость доставки до{}".format(shipp_addr))
            await state.set_state(States.auctions1)



@dp.message_handler(state='*', commands=['a_test'])
async def manager_mode(msg: types.Message):
    # task = asyncio.create_task(auction(1))
    print("auction")



@dp.message_handler(state='*', commands=['mailing'])
async def manager_mode(msg: types.Message):
    state = dp.current_state(user=msg.chat.id)

    await msg.answer("общая рассылка? или напоминание о незаконченном заказе?", reply_markup=MAIL)
    await state.set_state(States.MAILER)


@dp.message_handler(state=States.MAILER)
async def manager_mode(msg: types.Message):
    state = dp.current_state(user=msg.chat.id)
    i = 0
    if msg.text == "общая рассылка":
        await mailing(0)
    elif msg.text == "напоминание о незаконченном заказе":
       i =  await mailing(1)
    await msg.answer("отправили это сообщение всем, кто попал в выборку({} человек)".format(str(i)), reply_markup=INIT_KEYBOARD)
    await state.set_state(States.AFT_INIT_STATE)


@dp.message_handler(state='*', commands=['new_mail'])
async def manager_mode(msg: types.Message):
    print("zashel")
    state = dp.current_state(user=msg.chat.id)
    cnx = connect()
    curs = cnx.cursor()
    curs.execute("select count(*) as cnt, manager_chat_id from shops left join products on shops.shop_id = products.shop_id group by manager_chat_id;")
    data = curs.fetchall()
    for row in data:
        print(row)
        if int(row[0]) < 15:
            print("sended")
            await bot.send_message(row[1], """Добрый день!
Вам нужно добавить букеты,чтобы у покупателя был большой выбор ассортимента в вашем магазине.
Это позволит привлечь к вашему магазину большее внимание,а также увеличит продажи.
Добавить букеты можно через кнопку /manager_mode .
Спасибо""")
            await bot.send_message(ADMIN_CHAT_ID, "есть +1")


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
#
# @dp.message_handler(state='*', commands=['zakaz'])  # @dp.message_handler(state=States.NS3) #todo check
# async def NS(msg: types.Message):
#     state = dp.current_state(user=msg.chat.id)
#     await bot.send_message(msg.chat.id, "раздел акций, ознакомьтесь с акционными товарами")
#     ## start
#     i = 0
#     cnx = connect()
#
#     cursor = cnx.cursor()
#
#     sqlin = ("select id, file_id, caption, categories, cost, shop_id "
#              "from products "
#              "where shop_id = 40;")
#     # value = (shop_id,)
#     cursor.execute(sqlin)
#     flowers = cursor.fetchall()
#     price = 0
#     number = 0
#     for current in flowers:
#         print(current[0], current[4])
#         flag = 0
#         flagflo = 0
#         price = (int(current[4]))  # + int(add_cost))
#         # * 100
#         # print(distance, add_cost, PRICE.amount, "qq")
#
#         # flower = re.search(regex_dict[capture], current[3])
#         sh_id = current[5]
#         addrs = ""
#
#         sq = ("select addr from shop_addr where shop_id = %s")
#         v = (sh_id,)
#         c = connect()
#         cur = c.cursor()
#         cur.execute(sq, v)
#         ad = cur.fetchall()
#         for j in ad:
#             addrs += j[0] + '\n'
#         number += 1
#         kb1 = types.InlineKeyboardMarkup()
#         bm1 = types.InlineKeyboardButton("+", callback_data='button1')
#         bm2 = types.InlineKeyboardButton("-", callback_data='button2')
#
#         kb1.add(bm1, bm2)
#         ch = await bot.send_photo(msg.chat.id, photo=current[1],
#                                   caption=current[2] + "конечная стоимость:" + str(
#                                       price) + " доставка: уточним позже" + "\n#" + str(
#                                       current[0]) + "#" + "адреса магазина:" + addrs, reply_markup=kb1)
#         ID = ch.photo[-1].file_id
#         ID2 = current[1]
#         i = int(i) + int(1)
#
#     ##end

@dp.message_handler(state='*', commands=['check'])  # @dp.message_handler(state=States.NS3) #todo check
async def NS(msg: types.Message):
    state = dp.current_state(user=msg.chat.id)
    i = True
    if i == True:  # if msg.text == "завершить"
        print(msg.text[7:])

        cnx = connect()

        cursor = cnx.cursor()
        sql = (
            "select shop_name, access_token, shop_id from shops where shop_name = %s;")  # select shop_name, access_token, shop_id from flobot.shops;
        cursor.execute(sql, (msg.text[7:],))  # todo требует проверки state!
        curs = cursor.fetchall()
        print("!!", msg.text)
        print(curs)
        for shops in curs:
            instagram_basic_display.set_access_token(shops[1])
            profile = instagram_basic_display.get_user_profile()
            print(profile)
            media = instagram_basic_display.get_user_media(limit=100)  # по заказу - 100
            print(len(media['data']), "!!!")
            list = media['data']
            i = 0
            for curr in list:

                image = curr['media_url']
                ff = 100
                ff = re.search("https://video", image)

                print(ff, "ff")
                if ff == None:
                    caption = curr['caption']
                    ln = len(caption)
                    if ln > 1024:
                        continue
                    print(image, i)
                    print("len of cap = " + str(ln))
                    tmp = caption[:255]

                    if ln < 255:
                        tmp = caption[:ln]
                    ln = len(tmp)
                    print("len of tmp = " + str(ln))
                    # time.sleep(0.1)
                    ch = await bot.send_photo(msg.chat.id, image)
                    print(curr)
                    sql = ("insert into flobot.products(file_id, caption, shop_id, shop)"
                           "values(%s,  %s, %s, %s)")
                    value = (
                        ch.photo[-1].file_id,
                        tmp,
                        shops[2],
                        profile["username"]
                    )
                    print(value, "value")
                    commit_query(sql, value)
                    await bot.delete_message(ch.chat.id, ch.message_id)
                tmp = ""

        print("finish")
        await bot.send_message(msg.chat.id,
                               "спасибо за сотрудничество! теперь нужно уточнить информацию о продуктах в разделе /manager_mode, сделайте это как можно скорее!)",
                               reply_markup=INIT_KEYBOARD)  # todo

        await state.set_state(States.AFT_INIT_STATE)


@dp.message_handler(state='*', commands=['bad'])  # @dp.message_handler(state=States.NS3) #todo bad
async def NS(msg: types.Message):
    state = dp.current_state(user=msg.chat.id)

    cnx = connect()
    cursor = cnx.cursor()
    sql = ("select shop_name, access_token, shop_id, manager_chat_id from flobot.shops;")
    cursor.execute(sql)  # todo требует проверки state!
    curs = cursor.fetchall()
    for row in curs:
        try:
            await bot.send_message(int(row[3]),
                               "бот будет недоступен в течении некоторого времени. просьба не пользоваться его услугами некоторое время")
        except:
            await bot.send_message(ADMIN_CHAT_ID, "{row[0]} bot was blocked by the user")

@dp.message_handler(state='*', commands=['good'])  # @dp.message_handler(state=States.NS3) #todo bad
async def NS(msg: types.Message):
    state = dp.current_state(user=msg.chat.id)

    cnx = connect()
    cursor = cnx.cursor()
    sql = ("select shop_name, access_token, shop_id, manager_chat_id from flobot.shops;")
    cursor.execute(sql)  # todo требует проверки state!
    curs = cursor.fetchall()
    for row in curs:
        await bot.send_message(int(row[3]),
                               "бот возобновил свою работу, /manager_mode вы можете продолжить редактирование ваших товаров")


@dp.message_handler(state='*', commands=['new_shop'])
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


# todo start of new


@dp.message_handler(state='*', commands=['manager_mode'])
async def manager_mode(msg: types.Message):
    state = dp.current_state(user=msg.chat.id)
    #  todo if msg.id == shop_manager_id
    print(msg.from_user.full_name)

    cnx = connect()
    cursor = cnx.cursor()
    sql = (" select manager_chat_id "
           " from flobot.managers "
           " where manager_chat_id = '%s';")
    cursor.execute(sql, (msg.chat.id,))
    curs1 = cursor.fetchone()

    if curs1 is None:
        await msg.answer("у вас нет таких прав", reply_markup=INIT_KEYBOARD)
        await state.set_state(States.AFT_INIT_STATE)
        return -1

    cnx = connect()
    cursor = cnx.cursor()
    sql = (" select * "
           " from flobot.shops "
           " where manager_chat_id = '%s';")
    cursor.execute(sql, (msg.chat.id,))
    curs = cursor.fetchone()
    # if curs[1] is None:

    if curs is not None and curs[6] is None:
        mngr_pay = types.InlineKeyboardMarkup()
        bnn1 = types.InlineKeyboardButton("зарегистрироваться", callback_data='payment_registration')
        mngr_pay.add(bnn1)
        await state.set_state(States.manager_mode_reg)
        await msg.answer("вам бы пройти регистрацию в банковской системе", reply_markup=mngr_pay)
        # return -1

    req = (
        """ select is_open from shops left join managers on managers.shop_id = shops.shop_id where managers.manager_chat_id = %s """)
    val = (msg.chat.id,)
    st = get_query(req, val)
    if st == 'yes':
        await msg.answer("что вы хотите сделать?\nчтобы управлять видимостью используйте кнопки ниже(скрыть/показать)",
                         reply_markup=manager_mode_keys1)
    else:
        await msg.answer("что вы хотите сделать?\nчтобы управлять видимостью используйте кнопки ниже(скрыть/показать)",
                         reply_markup=manager_mode_keys2)

    kb1 = types.ReplyKeyboardMarkup(True, True)
    kb1.row("★ ⬆️ В начало ⬆️ ★")
    await msg.answer("для выхода нажмите на кнопку на клавиатуре ниже", reply_markup=kb1)
    await state.set_state(States.manager_mode)

    cnx = connect()
    cursor = cnx.cursor()
    sql = (" select * "
           " from flobot.editor "
           " where manager_id = '%s';")
    cursor.execute(sql, (msg.chat.id,))
    curs = cursor.fetchone()
    if curs == None:
        sql = (" insert into "
               " flobot.editor(manager_id) "
               " values(%s);")
        values = (msg.chat.id,)
        cursor.execute(sql, values)
        cnx.commit()


@dp.callback_query_handler(lambda c: c.data == 'visual_ability', state=States.manager_mode)
async def visual_ability(callback_query: types.CallbackQuery):
    state = dp.current_state(user=callback_query.from_user.id)
    await callback_query.answer('visual_ability')
    msg_id = callback_query.message.message_id
    i_msg_id = callback_query.inline_message_id
    req = (
        """ select is_open from shops left join managers on managers.shop_id = shops.shop_id where managers.manager_chat_id = %s """)
    val = (callback_query.from_user.id,)
    st = get_query(req, val)
    print("visual_ability", st)

    if st == 'yes':
        st = 'no'
        await bot.edit_message_reply_markup(callback_query.from_user.id, msg_id, i_msg_id,
                                            reply_markup=manager_mode_keys2)
    else:
        st = 'yes'
        await bot.edit_message_reply_markup(callback_query.from_user.id, msg_id, i_msg_id,
                                            reply_markup=manager_mode_keys1)

    req = (
        """ update shops set is_open = %s where shop_id = (select shop_id from managers where managers.manager_chat_id = %s) ; """)
    val = (st, callback_query.from_user.id,)
    st = commit_query(req, val)


@dp.callback_query_handler(lambda c: c.data == 'payment_registration', state=States.manager_mode)
async def toSandBox(callback: types.CallbackQuery):
    print('Joba')
    state = dp.current_state(user=callback.from_user.id)
    sql = (" select shop_id from flobot.shops where manager_chat_id = '%s';")
    values = (callback.from_user.id,)
    shop_id = get_query(sql, values)
    sql = ("select * from registration_info where shop_id = '%s';")
    values = (shop_id,)
    reg_info = get_query_all(sql, values)

    if reg_info is None:
        sql = (" insert into "
               " flobot.registration_info(shop_id,type,country,citizenship) "
               " values(%s,'legal','RUS','Россия');")
        values = (shop_id,)
        commit_query(sql, values)
        await bot.send_message(callback.from_user.id, "начнем!")
        await bot.send_message(callback.from_user.id,
                               "Пришлите название магазина в СМС и на странице проверки 3DS на английском языке пример: \"IP SHENKAO V M\"")
    else:
        sql = (" select shop_id from flobot.shops where manager_chat_id = '%s';")
        values = (callback.from_user.id,)
        shop_id = get_query(sql, values)

        sql = ("select * from registration_info where shop_id = '%s';")
        values = (shop_id,)
        reg_info = get_query_all(sql, values)

        print(reg_info)
        if reg_info is not None:
            for i in range(25):
                if reg_info[i] is None:
                    await bot.send_message(callback.from_user.id, "Продолжим заполнять")
                    await regshop.print_reg_info(i - 1, callback.from_user.id)
                    break

    await state.set_state(States.SANDBOX)


@dp.message_handler(state=States.SANDBOX)
async def sandbox2(msg: types.Message):
    print(msg.text)
    state = dp.current_state(user=msg.chat.id)
    if msg.text == "назад":
        await regshop.on_back_press(msg.chat.id)

        return -1
    elif msg.text == "★ ⬆️ В начало ⬆️ ★":
        await bot.send_message(msg.chat.id, "начнем заново", reply_markup=INIT_KEYBOARD)
        await state.set_state(States.AFT_INIT_STATE)

    sql = (" select shop_id from flobot.shops where manager_chat_id = '%s';")
    values = (msg.chat.id,)
    shop_id = get_query(sql, values)

    sql = ("select * from registration_info where shop_id = '%s';")
    values = (shop_id,)
    reg_info = get_query_all(sql, values)

    print(reg_info)

    if reg_info is not None:
        for i in range(25):
            print(i)
            print(reg_info[i])
            if reg_info[i] is None:
                await regshop.fill_reg_info(i, msg.text, shop_id, msg.chat.id)
                await regshop.print_reg_info(i, msg.chat.id)
                break


@dp.callback_query_handler(lambda c: c.data == 'add_product', state=States.manager_mode)
async def add_product(callback_query: types.CallbackQuery):
    await callback_query.answer("add_product")
    state = dp.current_state(user=callback_query.from_user.id)
    kb1 = types.ReplyKeyboardMarkup(True, True)
    kb1.row("★ ⬆️ В начало ⬆️ ★")
    kb1.row("назад")
    await bot.send_message(callback_query.from_user.id,
                           "это раздел добавления товаров.\nСначала пришлите фото букета или добавьте поштучный товар", reply_markup=kb1)
    state = dp.current_state()

    current_prod = {
        'manager_chat': callback_query.from_user.id,
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

    await state.set_state(States.UPLOAD1)


@dp.callback_query_handler(lambda c: c.data == 'add_sale', state=States.manager_mode)
async def add_product(callback_query: types.CallbackQuery):
    await callback_query.answer("add_sale")
    state = dp.current_state(user=callback_query.from_user.id)
    kb1 = types.ReplyKeyboardMarkup(True, True)
    kb1.row("★ ⬆️ В начало ⬆️ ★")
    kb1.row("назад")
    await bot.send_message(callback_query.from_user.id,
                           "это раздел добавления акционных товаров.\nСначала пришлите фото букета или добавьте поштучный товар",
                           reply_markup=kb1)
    current_prod = {
        'manager_chat': callback_query.from_user.id,
        'sale': "sale",
        'file_id': "",
        'caption': "",
        'categ': "",
        'cost': 0,
        'shop': "",
        'time': 0,
        'inspired_in': "нет"
    }
    current_products.append(current_prod)
    state = dp.current_state()
    await state.set_state(States.UPLOAD1)


@dp.callback_query_handler(lambda c: c.data == 'show_product', state=States.manager_mode)
async def show_prdouct(callback_query: types.CallbackQuery):
    await callback_query.answer("show_product")
    state = dp.current_state(user=callback_query.from_user.id)

    cnx = connect()
    cursor = cnx.cursor()
    sql = (" select products.id, products.file_id, products.caption, products.categories, products.cost "
           " from flobot.products join managers on products.shop_id = managers.shop_id "
           " where managers.manager_chat_id = '%s';")
    cursor.execute(sql, (callback_query.from_user.id,))
    curs = cursor.fetchall()
    for row in curs:
        await bot.send_photo(callback_query.from_user.id, row[1], "id товара в боте = " + str(row[0]) + '\n' + row[2])

    await bot.send_message(callback_query.from_user.id, "что вы хотите сделать?", reply_markup=manager_mode_keys)

    kb1 = types.ReplyKeyboardMarkup(True, True)
    kb1.row("★ ⬆️ В начало ⬆️ ★")
    # kb.row("назад")
    await bot.send_message(callback_query.from_user.id, "для выхода нажмите на кнопку на клавиатуре ниже",
                           reply_markup=kb1)
    await state.set_state(States.manager_mode)


@dp.callback_query_handler(lambda c: c.data == 'edit_product', state=States.manager_mode)
async def edit_product(callback_query: types.CallbackQuery):
    await callback_query.answer("edit_product")
    state = dp.current_state(user=callback_query.from_user.id)
    kb = types.ReplyKeyboardMarkup(True, True)
    kb.row("назад")
    kb.row("★ ⬆️ В начало ⬆️ ★")
    await bot.send_message(callback_query.from_user.id, "введите с клавиатуры id продукта в боте", reply_markup=kb)
    await state.set_state(States.manager_mode_edit_product)


@dp.callback_query_handler(lambda c: c.data == 'add_manager', state=States.manager_mode)
async def add_manager(callback_query: types.CallbackQuery):
    await callback_query.answer("add_manager")
    state = dp.current_state(user=callback_query.from_user.id)
    kb = types.ReplyKeyboardMarkup(True, True)
    kb.row("назад")
    kb.row("★ ⬆️ В начало ⬆️ ★")
    await bot.send_message(callback_query.from_user.id, "перешлите любое сообщение от нового менеджера",
                           reply_markup=kb)
    await state.set_state(States.manager_mode8)


@dp.message_handler(state=States.manager_mode8)
async def add_manager(msg: types.Message):
    state = dp.current_state(user=msg.chat.id)

    if msg.text == "назад":
        await bot.send_message(msg.chat.id, "что вы хотите сделать?", reply_markup=manager_mode_keys)
        kb1 = types.ReplyKeyboardMarkup(True, True)
        kb1.row("★ ⬆️ В начало ⬆️ ★")
        kb1.row("назад")
        await bot.send_message(msg.chat.id, "для выхода нажмите на кнопку на клавиатуре ниже",
                               reply_markup=kb1)
        await state.set_state(States.manager_mode)
    elif msg.text == "★ ⬆️ В начало ⬆️ ★":
        await bot.send_message(msg.chat.id, "начнем заново", reply_markup=INIT_KEYBOARD)
        await state.set_state(States.AFT_INIT_STATE)

    manager_chat_id = (msg['forward_from']['id'])
    f_name = (msg['forward_from']['first_name'])
    l_name = (msg['forward_from']['last_name'])

    sql = (" select shop_id from flobot.managers where manager_chat_id = '%s';")
    values = (msg.chat.id,)

    shop_id = get_query(sql, values)

    sql = (" insert into "
           " flobot.managers(shop_id, manager_chat_id) "
           " values(%s,%s);")
    values = (shop_id, manager_chat_id,)
    commit_query(sql, values)
    await msg.reply("ваш новый менеджер {} {}".format(f_name, l_name))
    state = dp.current_state()
    await state.set_state(States.manager_mode)


@dp.callback_query_handler(lambda c: c.data == 'delete_product', state=States.manager_mode2)
async def delete_product(callback_query: types.CallbackQuery):
    await callback_query.answer("delete_product")
    state = dp.current_state(user=callback_query.from_user.id)
    print(callback_query["message"]["caption"])
    if callback_query["message"]["caption"] == "назад":
        await bot.send_message(callback_query.from_user.id, "что вы хотите сделать?", reply_markup=manager_mode_keys)
        kb1 = types.ReplyKeyboardMarkup(True, True)
        kb1.row("★ ⬆️ В начало ⬆️ ★")
        kb1.row("назад")
        await bot.send_message(callback_query.from_user.id, "для выхода нажмите на кнопку на клавиатуре ниже",
                               reply_markup=kb1)
        await state.set_state(States.manager_mode)
        return -1
    print(callback_query["message"]["caption"])
    idi = callback_query["message"]["caption"].find("id = ")
    idj = callback_query["message"]["caption"].find("\n")
    id = callback_query["message"]["caption"][idi + 5:idj]

    sql = """delete from products where id = %s;"""
    v = (id,)
    commit_query(sql, v)

    cnx = connect()
    cursor = cnx.cursor()

    sql = (" select products.id, products.file_id, products.caption, products.categories, products.cost "
           " from flobot.products join managers on products.shop_id = managers.shop_id "
           " where managers.manager_chat_id = '%s';")
    cursor.execute(sql, (callback_query.from_user.id,))
    id = int(id)
    curs = cursor.fetchall()
    print(curs)
    if not curs:
        print("NONE CURSOR")
        await bot.send_message(callback_query.from_user.id,
                               "у вас видимо нет ни одного товара!\nчто вы хотите сделать?",
                               reply_markup=manager_mode_keys)
        await state.set_state(States.manager_mode)
    else:
        target = curs[0]

        for row in curs:
            if int(row[0]) >= int(id) + 1:
                target = row
                break
            else:
                print("o_O")

        row = target
        id = row[0]
        cappa = row[2]
        catta = ""
        ccosta = ""
    if (row[3] == None):
        catta = "добавьте категории"
    else:
        catta = row[3]

    if (row[4] == None):
        ccosta = "добавьте стоимость"
    else:
        ccosta = row[4]

    cap = "id = " + str(
        row[0]) + "\nописание:\" " + cappa + "\"\n" + "категории: \"" + catta + "\"\n" + "цена: \"" + str(
        ccosta) + '\"\n' + "что именно вы хотите отредактировать?"

    cnx = connect()
    cursor = cnx.cursor()
    sql = (" update editor set product_id = %s where manager_id = %s;")
    values = (id, callback_query.from_user.id)
    cursor.execute(sql, values)
    cnx.commit()
    await bot.send_photo(callback_query.from_user.id, row[1], cap, reply_markup=manager_mode_edit_keys)
    await state.set_state(States.manager_mode2)


@dp.message_handler(state=States.manager_mode7)
async def manager_mode7(msg: types.Message):
    state = dp.current_state(user=msg.chat.id)

    if msg.text == "назад":
        await bot.send_message(msg.chat.id, "что вы хотите сделать?", reply_markup=manager_mode_keys)
        kb1 = types.ReplyKeyboardMarkup(True, True)
        kb1.row("★ ⬆️ В начало ⬆️ ★")
        kb1.row("назад")
        await bot.send_message(msg.chat.id, "для выхода нажмите на кнопку на клавиатуре ниже",
                               reply_markup=kb1)
        await state.set_state(States.manager_mode)
        return -1

    id = msg.text
    cnx = connect()
    cursor = cnx.cursor()
    sql = (" delete "
           " from flobot.products "
           " where id = %s;")
    cursor.execute(sql, (id,))
    await msg.answer("вы его удалили")

    await bot.send_message(msg.chat.id, "что вы хотите сделать?", reply_markup=manager_mode_keys)
    kb1 = types.ReplyKeyboardMarkup(True, True)
    kb1.row("★ ⬆️ В начало ⬆️ ★")
    kb1.row("назад")
    await bot.send_message(msg.chat.id, "для выхода нажмите на кнопку на клавиатуре ниже",
                           reply_markup=kb1)
    await state.set_state(States.manager_mode)


@dp.message_handler(state=States.manager_mode_edit_product)
async def manager_mode1(msg: types.Message):
    state = dp.current_state(user=msg.chat.id)
    if msg.text == "назад":
        await bot.send_message(msg.chat.id, "что вы хотите сделать?", reply_markup=manager_mode_keys)
        kb1 = types.ReplyKeyboardMarkup(True, True)
        kb1.row("★ ⬆️ В начало ⬆️ ★")
        # kb.row("назад")
        await bot.send_message(msg.chat.id, "для выхода нажмите на кнопку на клавиатуре ниже",
                               reply_markup=kb1)
        await state.set_state(States.manager_mode)
        return -1
    elif msg.text == "★ ⬆️ В начало ⬆️ ★":
        print("!!/")
        await bot.send_message(msg.chat.id, "начнем заново", reply_markup=INIT_KEYBOARD)
        await state.set_state(States.AFT_INIT_STATE)
        return -1

    id = msg.text

    cnx = connect()
    cursor = cnx.cursor()

    sql = (" select products.id, products.file_id, products.caption, products.categories, products.cost "
           " from flobot.products join managers on products.shop_id = managers.shop_id "
           " where managers.manager_chat_id = '%s';")
    cursor.execute(sql, (msg.chat.id,))

    curs = cursor.fetchall()
    print(curs)
    if not curs:
        print("NONE CURSOR")
        await msg.answer("у вас видимо нет ни одного товара!\nчто вы хотите сделать?", reply_markup=manager_mode_keys)
        await state.set_state(States.manager_mode)
    else:
        target = curs[0]

        for row in curs:
            if int(row[0]) >= int(id):
                target = row
                break
            else:
                print("o_O")
        print(target, "$$")
        row = target
        id = row[0]
        cappa = row[2]
        catta = ""
        ccosta = ""
        if (row[3] == None):
            catta = "добавьте категории"
        else:
            catta = row[3]

        if (row[4] == None):
            ccosta = "добавьте стоимость"
        else:
            ccosta = row[4]

        cap = "id = " + str(
            row[0]) + "\nописание:\" " + cappa + "\"\n" + "категории: \"" + catta + "\"\n" + "цена: \"" + str(
            ccosta) + '\"\n' + "что именно вы хотите отредактировать?"

        cnx = connect()
        cursor = cnx.cursor()
        sql = (" update editor set product_id = %s where manager_id = %s;")
        values = (id, msg.chat.id)
        print(id, "edit")
        cursor.execute(sql, values)
        cnx.commit()
        await bot.send_photo(msg.chat.id, row[1], cap, reply_markup=manager_mode_edit_keys)
        await state.set_state(States.manager_mode2)


@dp.callback_query_handler(lambda c: c.data == 'edit_next', state=States.manager_mode2)
async def edit_next(callback_query: types.CallbackQuery):
    await callback_query.answer("edit_next")
    state = dp.current_state(user=callback_query.from_user.id)  # TODO PIDR
    idi = callback_query["message"]["caption"].find("id = ")
    idj = callback_query["message"]["caption"].find("\n")
    id = callback_query["message"]["caption"][idi + 5:idj]  # todo edit next
    cnx = connect()
    cursor = cnx.cursor()

    sql = (" select products.id, products.file_id, products.caption, products.categories, products.cost "
           " from flobot.products join managers on products.shop_id = managers.shop_id "
           " where managers.manager_chat_id = '%s';")
    cursor.execute(sql, (callback_query.from_user.id,))
    id = int(id)
    curs = cursor.fetchall()
    print(curs)
    if not curs:
        print("NONE CURSOR")
        await bot.send_message(callback_query.from_user.id,
                               "у вас видимо нет ни одного товара!\nчто вы хотите сделать?",
                               reply_markup=manager_mode_keys)
        await state.set_state(States.manager_mode)
    else:
        target = curs[0]

        for row in curs:
            if int(row[0]) >= int(id) + 1:
                target = row
                break
            else:
                print("o_O")

        row = target
        id = row[0]
        cappa = row[2]
        catta = ""
        ccosta = ""
        if (row[3] == None):
            catta = "добавьте категории"
        else:
            catta = row[3]

        if (row[4] == None):
            ccosta = "добавьте стоимость"
        else:
            ccosta = row[4]

        cap = "id = " + str(
            row[0]) + "\nописание:\" " + cappa + "\"\n" + "категории: \"" + catta + "\"\n" + "цена: \"" + str(
            ccosta) + '\"\n' + "что именно вы хотите отредактировать?"
        cnx = connect()
        cursor = cnx.cursor()
        sql = (" update editor set product_id = %s where manager_id = %s;")
        values = (id, callback_query.from_user.id)
        cursor.execute(sql, values)
        cnx.commit()
        ch = await bot.send_photo(callback_query.from_user.id, row[1], cap, reply_markup=manager_mode_edit_keys)
        await bot.delete_message(ch.chat.id, ch.message_id - 1)
        await state.set_state(States.manager_mode2)


@dp.callback_query_handler(lambda c: c.data == 'edit_prev', state=States.manager_mode2)
async def edit_prev(callback_query: types.CallbackQuery):
    await callback_query.answer("edit_prev")
    state = dp.current_state(user=callback_query.from_user.id)  # TODO PIDR
    idi = callback_query["message"]["caption"].find("id = ")
    idj = callback_query["message"]["caption"].find("\n")
    id = callback_query["message"]["caption"][idi + 5:idj]
    id = int(id)
    cnx = connect()
    cursor = cnx.cursor()
    sql = (" select products.id, products.file_id, products.caption, products.categories, products.cost "
           " from flobot.products join managers on products.shop_id = managers.shop_id "
           " where managers.manager_chat_id = '%s';")
    cursor.execute(sql, (callback_query.from_user.id,))
    curs = cursor.fetchall()
    print(curs)
    if not curs:
        print("NONE CURSOR")
        await bot.send_message(callback_query.from_user.id,
                               "у вас видимо нет ни одного товара!\nчто вы хотите сделать?",
                               reply_markup=manager_mode_keys)
        await state.set_state(States.manager_mode)
    else:
        target = curs[0]

        for row in curs:
            if int(row[0]) < int(id):
                target = row
            else:
                break

        row = target
        id = row[0]
        cappa = row[2]
        catta = ""
        ccosta = ""
        if (row[3] == None):
            catta = "добавьте категории"
        else:
            catta = row[3]

        if (row[4] == None):
            ccosta = "добавьте стоимость"
        else:
            ccosta = row[4]

        cap = "id = " + str(
            row[0]) + "\nописание:\" " + cappa + "\"\n" + "категории: \"" + catta + "\"\n" + "цена: \"" + str(
            ccosta) + '\"\n' + "что именно вы хотите отредактировать?"
        cnx = connect()
        cursor = cnx.cursor()
        sql = (" update editor set product_id = %s where manager_id = %s;")
        values = (id, callback_query.from_user.id)
        cursor.execute(sql, values)
        cnx.commit()
        ch = await bot.send_photo(callback_query.from_user.id, row[1], cap, reply_markup=manager_mode_edit_keys)
        await bot.delete_message(ch.chat.id, ch.message_id - 1)
        await state.set_state(States.manager_mode2)


@dp.message_handler(state=States.manager_mode2)
async def manager_mode2(msg: types.Message):
    state = dp.current_state(user=msg.chat.id)

    if msg.text == "назад":
        await bot.send_message(msg.chat.id, "что вы хотите сделать?", reply_markup=manager_mode_keys)
        kb1 = types.ReplyKeyboardMarkup(True, True)
        kb1.row("★ ⬆️ В начало ⬆️ ★")
        kb1.row("назад")
        await bot.send_message(msg.chat.id, "для выхода нажмите на кнопку на клавиатуре ниже",
                               reply_markup=kb1)
        await state.set_state(States.manager_mode)
    elif msg.text == "★ ⬆️ В начало ⬆️ ★":
        await bot.send_message(msg.chat.id, "начнем заново", reply_markup=INIT_KEYBOARD)
        await state.set_state(States.AFT_INIT_STATE)


@dp.callback_query_handler(lambda c: c.data == 'edit_caption', state=States.manager_mode2)
async def edit_caption(callback_query: types.CallbackQuery):
    await callback_query.answer("edit_caption")
    state = dp.current_state(user=callback_query.from_user.id)
    print(callback_query['message']['caption'])
    i = callback_query['message']['caption'].find("id = ")
    j = callback_query['message']['caption'].find("описание")
    id = callback_query['message']['caption'][i:j]
    print("id = " + str(id))

    await bot.send_message(callback_query.from_user.id, "введите новое описание товара " + str(id))
    await state.set_state(States.manager_mode3)


@dp.message_handler(state=States.manager_mode3)
async def manager_mode3(msg: types.Message):
    state = dp.current_state(user=msg.chat.id)
    cnx = connect()
    cursor = cnx.cursor()
    sql = (" select product_id from flobot.editor where manager_id = %s;")
    values = (msg.chat.id,)
    cursor.execute(sql, values)
    row = cursor.fetchone()
    print(row, "!!")
    sql = (" update flobot.products set caption = %s where id = %s;")
    values = (msg.text, row[0])
    cursor.execute(sql, values)
    cnx.commit()

    cursor = cnx.cursor()
    sql = (" select products.id, products.file_id, products.caption, products.categories, products.cost "
           " from flobot.products join managers on products.shop_id = managers.shop_id "
           " where managers.manager_chat_id = '%s' and products.id = %s;")
    cursor.execute(sql, (msg.chat.id, row[0],))
    row = cursor.fetchone()
    if not row:
        await bot.send_message(msg.chat.id, "закончились")
        await msg.answer("что вы хотите сделать?", reply_markup=manager_mode_keys)
        await state.set_state(States.manager_mode)
        return -1
    cappa = row[2]
    catta = ""
    ccosta = ""
    if (row[3] == None):
        catta = "добавьте категории"
    else:
        catta = row[3]

    if (row[4] == None):
        ccosta = "добавьте стоимость"
    else:
        ccosta = row[4]

    cap = "id = " + str(
        row[0]) + "\nописание:\" " + cappa + "\"\n" + "категории: \"" + catta + "\"\n" + "цена: \"" + str(
        ccosta) + '\"\n' + "что именно вы хотите отредактировать?"

    await bot.send_photo(msg.chat.id, row[1], cap, reply_markup=manager_mode_edit_keys)
    await state.set_state(States.manager_mode2)


@dp.callback_query_handler(lambda c: c.data == 'edit_categories', state=States.manager_mode2)
async def edit_categories(callback_query: types.CallbackQuery):
    await callback_query.answer("edit_categories")
    state = dp.current_state(user=callback_query.from_user.id)
    print(callback_query['message']['caption'])
    i = callback_query['message']['caption'].find("id = ")
    j = callback_query['message']['caption'].find("описание")
    id = callback_query['message']['caption'][i:j]
    print("id = " + str(id))

    await bot.send_message(callback_query.from_user.id, "введите новую категорию товара " + str(id), reply_markup=FLOWER_KEYS)
    await state.set_state(States.manager_mode4)


@dp.message_handler(state=States.manager_mode4)
async def manager_mode4(msg: types.Message):
    state = dp.current_state(user=msg.chat.id)
    cnx = connect()
    cursor = cnx.cursor()
    sql = (" select product_id from flobot.editor where manager_id = %s;")
    values = (msg.chat.id,)
    cursor.execute(sql, values)
    row = cursor.fetchone()

    sql = (" update flobot.products set categories = %s where id = %s;")
    values = (msg.text, row[0])
    cursor.execute(sql, values)
    cnx.commit()

    cursor = cnx.cursor()
    sql = (" select products.id, products.file_id, products.caption, products.categories, products.cost "
           " from flobot.products join shops on products.shop_id = shops.shop_id "
           " where shops.manager_chat_id = '%s' and products.id = %s;")
    cursor.execute(sql, (msg.chat.id, row[0],))
    row = cursor.fetchone()
    if not row:
        await bot.send_message(msg.chat.id, "закончились")
        return -1
    cappa = row[2]
    catta = ""
    ccosta = ""
    if (row[3] == None):
        catta = "добавьте категории"
    else:
        catta = row[3]

    if (row[4] == None):
        ccosta = "добавьте стоимость"
    else:
        ccosta = row[4]

    cap = "id = " + str(
        row[0]) + "\nописание:\" " + cappa + "\"\n" + "категории: \"" + catta + "\"\n" + "цена: \"" + str(
        ccosta) + '\"\n' + "что именно вы хотите отредактировать?"

    await bot.send_photo(msg.chat.id, row[1], cap, reply_markup=manager_mode_edit_keys)
    await state.set_state(States.manager_mode2)


@dp.callback_query_handler(lambda c: c.data == 'edit_cost', state=States.manager_mode2)
async def edit_cost(callback_query: types.CallbackQuery):
    await callback_query.answer("edit_cost")
    state = dp.current_state(user=callback_query.from_user.id)
    print(callback_query['message']['caption'])
    i = callback_query['message']['caption'].find("id = ")
    j = callback_query['message']['caption'].find("описание")
    id = callback_query['message']['caption'][i:j]
    print("id = " + str(id))

    await bot.send_message(callback_query.from_user.id, "введите новую стоимость товара " + str(id))
    await state.set_state(States.manager_mode5)


@dp.message_handler(state=States.manager_mode5)
async def manager_mode5(msg: types.Message):
    state = dp.current_state(user=msg.chat.id)
    cnx = connect()
    cursor = cnx.cursor()
    sql = (" select product_id from flobot.editor where manager_id = %s;")
    values = (msg.chat.id,)
    cursor.execute(sql, values)
    row = cursor.fetchone()

    sql = (" update flobot.products set cost = %s where id = %s;")
    values = (msg.text, row[0])
    cursor.execute(sql, values)
    cnx.commit()

    cursor = cnx.cursor()
    sql = (" select products.id, products.file_id, products.caption, products.categories, products.cost "
           " from flobot.products join shops on products.shop_id = shops.shop_id "
           " where shops.manager_chat_id = '%s' and products.id = %s;")
    cursor.execute(sql, (msg.chat.id, row[0],))
    row = cursor.fetchone()
    if not row:
        await bot.send_message(msg.chat.id, "закончились")
        return -1
    cappa = row[2]
    catta = row[3]
    ccosta = row[4]
    if (row[3] == None):
        catta = "добавьте категории"

    if (row[4] == None):
        ccosta = "добавьте стоимость"

    cap = "id = " + str(
        row[0]) + "\nописание:\" " + cappa + "\"\n" + "категории: \"" + catta + "\"\n" + "цена: \"" + str(
        ccosta) + '\"\n' + "что именно вы хотите отредактировать?"

    await bot.send_photo(msg.chat.id, row[1], cap, reply_markup=manager_mode_edit_keys)
    await state.set_state(States.manager_mode2)


# todo end of new


@dp.callback_query_handler(lambda c: c.data == 'not_inst', state=States.NS0)
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


@dp.callback_query_handler(lambda c: c.data == 'S_PP_NOT', state=States.NS0)
async def process_callback_add(callback_query: types.CallbackQuery):
    await callback_query.answer("S_PP_NOT")
    state = dp.current_state(user=callback_query.from_user.id)
    await bot.send_message(callback_query.from_user.id, "возвращайтесь, когда сможете ;D")
    await state.set_state(States.AFT_INIT_STATE)


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


@dp.message_handler(state='*', commands=['refresh'])
async def NS(msg: types.Message):
    state = dp.current_state(user=msg.chat.id)
    bot.send_message(msg.from_user.username)
    cnx = connect()

    cursor = cnx.cursor()
    sql = ("select shop_name, access_token, shop_id from flobot.shops;")
    cursor.execute(sql)  # todo требует проверки state!
    curs = cursor.fetchall()

    for shops in curs:
        print(shops[0], shops[1], shops[2])
        new_token = instagram_basic_display.refresh_token(shops[1])

        cnx = connect()

        cursor = cnx.cursor()

        sql = ("update flobot.shops set access_token = %s where shop_id = '%s';")
        values = (new_token['access_token'], shops[2])
        print("new")
        print(shops[0], new_token, shops[2])

        cursor.execute(sql, values)  # todo требует проверки state!
        cnx.commit()


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


# todo end of new


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


@dp.message_handler(state='*', commands=['start'])
async def process_start_command(message: types.Message):
    state = dp.current_state(user=message.chat.id)
    await bot.send_message(message.from_user.id, "➡️Введите адрес доставки в заданном формате (улица,номер дома) c клавиатуры: "
                                                 "\"Никольская 21\"\n⭐️или пришлите геолокацию адреса доставки",
                               reply_markup=TO_ME)
    await state.set_state(States.TO_ME_ST)
    # add user
    # add to db.clients
    # add to db.orders
    first = message.chat.first_name
    last = message.chat.last_name
    id = message.chat.id
    cnx = connect()

    cursor = cnx.cursor()
    sql = ("select client_chat_id from flobot.clients where client_chat_id = '%s';")
    cursor.execute(sql, (id,))
    row = cursor.fetchone()
    if (row == None):
        print("new client!")

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

    # ======

    first = message.chat.first_name
    last = message.chat.last_name
    id = message.chat.id
    cnx = connect()
    cursor = cnx.cursor()
    sql = ("select client_order_id from flobot.orders where client_order_id = '%s';")
    cursor.execute(sql, (id,))
    row = cursor.fetchone()

    if row is None:
        print(" new client!")

        sqlin = ("insert into flobot.orders(client_order_id) "
                 "values ('%s')")
        value = (id,)
        commit_query(sqlin, value)
    cnx.close()

    cnx = connect()
    cursor = cnx.cursor()
    que = "delete from cart where client_id = %s;"
    cursor.execute(que, (id,))
    cnx.commit()
    cnx.close()
    await send_video_instruction(message, 'order_shipping_adress', 'addr')


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

    elif msg.text == 'категории':
        await msg.answer("ознакомьтесь с категориями товаров", reply_markup=FLOWER_KEYS)
        await state.set_state(States.FLOWER_CATALOG)

    elif msg.text == '💐АКЦИИ💐':

        await bot.send_message(msg.chat.id, "пришлите адрес куда доставлять геолокацию либо сам адрес", reply_markup=TO_ME)
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


@dp.message_handler(state=States.sales2)
async def sales2(msg: types.Message, state=FSMContext):
    state = dp.current_state(user=msg.chat.id)



@dp.message_handler(state=States.TO_ME_ST, content_types=types.ContentTypes.ANY)
async def geo(msg: types.Message, state=FSMContext):

    flag_vid = False
    sql = "select order_shipping_adress from orders where client_order_id = {}".format(msg.chat.id)
    cnx = connect()
    curs = cnx.cursor()
    curs.execute(sql)
    info = curs.fetchone()
    print(info)
    if info[0] is None:
        print('vid')
        flag_vid = True
        # vid = test_bot_videos[state]
        # vid = bot_videos[state]
        # await bot.send_video(msg.chat.id, vid)


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
            await  state.set_state(States.TO_ME_ST)
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

    cnx = connect()
    cursor = cnx.cursor()
    sqlin = (
        "select flobot.shop_addr.*, flobot.shops.shop_name from flobot.shop_addr left join flobot.shops on "
        "flobot.shops.shop_id = flobot.shop_addr.shop_id where flobot.shops.is_open = 'yes' and flobot.shops.tink_shop_code is not null;")
    id_of_min = 10000
    d_min = 1000000.
    cursor.execute(sqlin)

    tmp_keys = types.ReplyKeyboardMarkup(True, True)

    # await bot.send_message(msg.chat.id,
    #                        "⭐️Есть несколько ближайших магазинов, по умолчанию выбирается ближайший.❗️\n"
    #                        "Вы можете изменить магазин, выбрав название нужного среди кнопок снизу✨")
    # await bot.send_message(msg.chat.id, "⬇️Проверьте правильность введенного адреса⬇️", reply_markup=tmp_keys)
    # await bot.send_message(msg.chat.id, current_value)
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
        dstr = str(idstr)

        dict_of_shops.update({row[0]: idstr}) # with addr_id
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
    sh_list = []
    managers = []
    for addr_id in shop_list:
        rw = get_query_all("select shop_id, addr from shop_addr where addr_id = %s;", (addr_id,))
        shop_id = str(rw[0])
        sh_list.append(shop_id)
        cnx = connect()
        curs = cnx.cursor()
        curs.execute("select manager_chat_id from managers where shop_id = {};".format(shop_id))
        mngrs = curs.fetchall()
        for manager in mngrs:
            managers.append(manager)
    auctin_order = {
        "client_id": msg.chat.id,
        "product_id": [],
        "shop_ids": sh_list,
        "curr_shop": 0,
        "curr_manager": 0,
        "curr_cost": 0,
        "first_cost": 0,
        "offer": "",
        "managers": managers,
        "delivery_cost": 0,
        "photos": []
    }
    exist = False
    for ordr in auctions:
        if ordr["client_id"] == msg.chat.id:
            exist = True

    if not exist:
        auctions.append(auctin_order)
    shop_id = id_of_min
    sqlin = ("update flobot.orders set order_shipping_adress = %s, len ='%s' "
             "where client_order_id = '%s';")
    value = (current_value, d_min, id)
    commit_query(sqlin, value)

    str1 = str(id_of_min)
    str2 = int(d_min)
    str2 = str(str2)
    for addr_id in shop_list:

        rw = get_query_all("select shop_id, addr from shop_addr where addr_id = %s;", (addr_id,))
        shop_id = str(rw[0])
        print(shop_id)
        addr = rw[1]
        shop_name = get_query("select shop_name from shops where shop_id = %s;", (shop_id,))
        tmp_keys.add(shop_name + ' адрес ' + str(addr) + ' расстояние: ' + str(round(dict_of_shops[addr_id])) + 'км')
        print()
        print("!!")
        cnx = connect()
        cursor = cnx.cursor()
        sqlin = ("select id, file_id, caption, categories, cost, shop_id "
                 "from products where shop_id = %s order by cost asc LIMIT 2;")
        value = (shop_id,)
        cursor.execute(sqlin, value)
        flowers = cursor.fetchall()
        price = 0
        number = 0
        for current in flowers:
            print(current[0], current[4])
            flag = 0
            flagflo = 0
            try:
                price = (int(current[4]))  # + int(add_cost))
            except:
                print("product without cost")
                continue
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
                                      caption=str(shop_name) + ' ' + str(current[2]) + "конечная стоимость:" + str(
                                          price) + " доставка: уточним позже" + "\n#" + str(
                                          current[0]) + "#" + "адреса магазина:" + addrs, reply_markup=kb1)
            ID = ch.photo[-1].file_id
            ID2 = current[1]
            i = int(i) + int(1)

    tmp_keys.row("🟥↩️главное меню↩️🟥")
    await bot.send_message(msg.chat.id, "ниже представлены магазины и их адреса", reply_markup=tmp_keys)

    if flag_vid:
        vid = bot_videos['addr']
        await bot.send_video(msg.chat.id, vid)


    await state.set_state(States.GEO_PROVE)
    # end



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


@dp.message_handler(state=States.COST)
async def echo_message(msg: types.Message, state=FSMContext):
    state = dp.current_state(user=msg.chat.id)

    if msg.text == "☆ ↩️ Назад ↩️ ☆": #TODO вернуться к выбору магазинов
        print("Назад вернуться к выбору магазинов")

        current_addr = get_query("select order_shipping_adress from orders where client_order_id = '%s'", (msg.chat.id,))

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
                await bot.send_message(msg.chat.id, "наблюдаются проблемы с сервисом определения адресов, повторите попытку позже")
                print("наблюдаются проблемы с сервисом определения адресов, повторите попытку позже")
                await bot.send_message(ADMIN_CHAT_ID, "наблюдаются проблемы с сервисом определения адресов dadata адрес: " + current_value)
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

        # await bot.send_message(msg.chat.id,
        #                        "⭐️Есть несколько ближайших магазинов, по умолчанию выбирается ближайший.❗️\n"
        #                        "Вы можете изменить магазин, выбрав название нужного среди кнопок снизу✨")
        # await bot.send_message(msg.chat.id, "⬇️Проверьте правильность введенного адреса⬇️", reply_markup=tmp_keys)
        # await bot.send_message(msg.chat.id, current_value)
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
        # sqlin = ("update flobot.orders set order_shipping_adress = %s, len ='%s' "
        #          "where client_order_id = '%s';")
        # value = (current_value, d_min, id)
        # commit_query(sqlin, value)

        # str1 = str(id_of_min)
        str2 = int(d_min)
        # str2 = str(str2)
        for addr_id in shop_list:

            rw = get_query_all("select shop_id, addr from shop_addr where addr_id = %s;", (addr_id,))
            shop_id = (rw[0]).__str__()
            print(shop_id)
            addr = rw[1]
            shop_name = get_query("select shop_name from shops where shop_id = %s;", (shop_id,))
            tmp_keys.add(shop_name + ' адрес ' + str(addr) + ' расстояние: ' + str(round(dict_of_shops[addr_id])) + 'км')
            print()
            print("!!")
            # cnx = connect()
            # cursor = cnx.cursor()
            # sqlin = ("select id, file_id, caption, categories, cost, shop_id "
            #          "from products where shop_id = %s LIMIT 4;")
            # value = (shop_id,)
            # cursor.execute(sqlin, value)
            # flowers = cursor.fetchall()
            # price = 0
            # number = 0
            # for current in flowers:
            #     print(current[0], current[4])
            #     flag = 0
            #     flagflo = 0
            #     try:
            #         price = (int(current[4]))  # + int(add_cost))
            #     except:
            #         print("product without cost")
            #         continue
            #     # * 100
            #     # print(distance, add_cost, PRICE.amount, "qq")
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
            #                               caption=str(shop_name) + ' ' + str(current[2]) + "конечная стоимость:" + str(
            #                                   price) + " доставка: уточним позже" + "\n#" + str(
            #                                   current[0]) + "#" + "адреса магазина:" + addrs, reply_markup=kb1)
            #     ID = ch.photo[-1].file_id
            #     ID2 = current[1]
            #     i = int(i) + int(1)
        tmp_keys.row("🟥↩️главное меню↩️🟥")
        await bot.send_message(msg.chat.id, "ниже представлены магазины и их адреса", reply_markup=tmp_keys)
        await state.set_state(States.GEO_PROVE)
        return 1
        # end

    cost_str = msg.text
    strS = re.search(r'\d{4}', cost_str)

    if not strS:
        await bot.send_message(msg.chat.id, "выберите цену используя клавиатуру ниже", reply_markup=COST)
        await state.set_state(States.COST)
        return -1

    print(strS[0])
    cost_str = strS[0]

    sqlin = ("update flobot.orders"
             " set order_cost = %s"
             "where client_order_id = '%s';")
    value = (cost_str, msg.chat.id)
    commit_query(sqlin, value)

    regex_dict
    key_dict = {}
    shop_id = get_query("select shop_order_id from orders where client_order_id = %s;", (msg.chat.id,))

    cnx = connect()
    curs = cnx.cursor()
    cost = get_query("select order_cost from orders where client_order_id = %s;", (msg.chat.id,))
    curs.execute("select categories from products where shop_id = '%s' and cost < %s;", (shop_id,cost,))
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
                    key_dict[key]+=1
                except:
                    print("key_dict.update({key")
                    key_dict.update({key : 1})
                    print(res[0],"@$#")
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
        j+=1

    print(btns)
    tuple(btns)
    # print("tut")
    if j == 0:
        await bot.send_message(msg.chat.id, "🔥💐похоже, у магазина нет букетов в этом ценовом диапозоне, выберите другой", reply_markup=COST)
        return -1
    keys.row("☆ ↩️ Назад ↩️ ☆")
    keys.row("к магазинам")

    await state.set_state(States.FLOWER_CATALOG)
    await bot.send_message(msg.chat.id, "🔥💐Отлично, теперь выберите цветы, если выбор вас не устраивает - вернитесь на несколько пункотов назад и выберите другой магазин", reply_markup=keys)
    await bot.send_message(msg.chat.id,
                           "если ваших цветов нет,выберите другой магазин",
                           reply_markup=keys)
    await send_video_instruction(msg, 'order_caption', "flowers")


@dp.message_handler(state=States.FLOWER_CATALOG)
async def echo_message(msg: types.Message, state=FSMContext):
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

        # await bot.send_message(msg.chat.id,
        #                        "⭐️Есть несколько ближайших магазинов, по умолчанию выбирается ближайший.❗️\n"
        #                        "Вы можете изменить магазин, выбрав название нужного среди кнопок снизу✨")
        # await bot.send_message(msg.chat.id, "⬇️Проверьте правильность введенного адреса⬇️", reply_markup=tmp_keys)
        # await bot.send_message(msg.chat.id, current_value)
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
        # sqlin = ("update flobot.orders set order_shipping_adress = %s, len ='%s' "
        #          "where client_order_id = '%s';")
        # value = (current_value, d_min, id)
        # commit_query(sqlin, value)

        # str1 = str(id_of_min)
        str2 = int(d_min)
        # str2 = str(str2)
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
            # cnx = connect()
            # cursor = cnx.cursor()
            # sqlin = ("select id, file_id, caption, categories, cost, shop_id "
            #          "from products where shop_id = %s LIMIT 4;")
            # value = (shop_id,)
            # cursor.execute(sqlin, value)
            # flowers = cursor.fetchall()
            # price = 0
            # number = 0
            # for current in flowers:
            #     print(current[0], current[4])
            #     flag = 0
            #     flagflo = 0
            #     try:
            #         price = (int(current[4]))  # + int(add_cost))
            #     except:
            #         print("product without cost")
            #         continue
            #     # * 100
            #     # print(distance, add_cost, PRICE.amount, "qq")
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
            #                               caption=str(shop_name) + ' ' + str(current[2]) + "конечная стоимость:" + str(
            #                                   price) + " доставка: уточним позже" + "\n#" + str(
            #                                   current[0]) + "#" + "адреса магазина:" + addrs, reply_markup=kb1)
            #     ID = ch.photo[-1].file_id
            #     ID2 = current[1]
            #     i = int(i) + int(1)
        tmp_keys.row("🟥↩️главное меню↩️🟥")
        await bot.send_message(msg.chat.id, "ниже представлены магазины и их адреса", reply_markup=tmp_keys)
        await state.set_state(States.GEO_PROVE)
        return 1
        # end

    flo = msg.text
    i = flo.find(' ')
    flor = flo[:i]
    cnt=0
    for key in regex_dict:
        res = re.search(regex_dict[key], flor)
        if  res:
            cnt+=1

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
    await state.set_state(States.DATETIME1)
    key = types.ReplyKeyboardMarkup(True, True)
    key.row("нет, продолжить дальше")
    key.row("да, хочу назначить время")
    # key.add(button_phone)

    await bot.send_message(msg.chat.id, "✨букет передадут курьеру как только соберут\n "
                                        "хотите назначить конкретное время доставки?",
                           reply_markup=key)
    await send_video_instruction(msg, 'order_shipping_adress', 'delivery')


@dp.message_handler(state=States.PHONE)
async def echo_message(msg: types.Message, state=FSMContext):
    state = dp.current_state(user=msg.chat.id)

    if msg.text == "🟥↩️ Не верно, вернуться назад ↩️🟥":
        await state.set_state(States.COST)
        await bot.send_message(msg.chat.id, "🔥💰Отлично, теперь выберите предполагаемую ценовую категорию",
                               reply_markup=COST)
        await state.set_state(States.COST)
    elif msg.text == "✅ Все верно ✅":
        #\

        #/
        await state.set_state(States.DATETIME1)
        key = types.ReplyKeyboardMarkup(True, True)
        key.row("нет, продолжить дальше")
        key.row("да, хочу назначить время")
        # key.add(button_phone)

        await bot.send_message(msg.chat.id, "✨букет передадут курьеру как только соберут\n "
                                            "хотите назначить конкретное время доставки?",
                               reply_markup=key)
        await send_video_instruction(msg,'order_shipping_adress', 'delivery')


@dp.message_handler(state=States.INVOICE, content_types=types.ContentTypes.CONTACT)
async def geofoo(msg: types.Message, state=FSMContext):
    state = dp.current_state(user=msg.chat.id)
    print("тут")
    if msg.chat.id == msg['contact']["user_id"]:
        id = msg.chat.id

        sqlin = ("update flobot.clients"
                 " set client_phone = %s"
                 "where client_chat_id = '%s';")
        value = (msg['contact']["phone_number"], id)
        commit_query(sqlin, value)

        await bot.send_message(msg.chat.id, "🤩Спасибо🤩" + msg.chat.first_name, reply_markup=KEYBOARD3)
        await state.set_state(States.ONLY_PHONE)
    else:
        await state.set_state(States.INVOICE)
        key = types.ReplyKeyboardMarkup(True, True)
        key.add(button_phone)
        await bot.send_message(msg.chat.id, "вы явно сделали что - то не так, используйте клавиатуру внизу",
                               reply_markup=key)
        return -1


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
            "хорошо, а время? не раньше {}:{} и не позже 21:00 (Мы работаем с 9:00 до 21:00, напишите точное время)".format(datetime.now().hour + 1, datetime.now().minute))
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
        time = datetime.strptime(msg.text, "%H:%M") # todo datetime
    except:
        await msg.answer("введите время в формате 10:00")
        return -1
    key = types.ReplyKeyboardMarkup(True, True)
    key.add("☆ ↩️ Назад ↩️ ☆")
    await bot.send_message(msg.chat.id, "уточните номер дома и квартиру для заказа", reply_markup=key)
    await state.set_state(States.HOME_NUM)


@dp.message_handler(state=States.HOME_NUM, content_types=types.ContentTypes.ANY)
async def home_num(msg:types.Message, state=FSMContext):
    number = msg.text
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
async def catalog(msg: types.Message, state=FSMContext):
    #

    print("NEW_SHOP_ST_2")
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

            await bot.send_message(msg.chat.id, "🤩Спасибо🤩" + msg.chat.first_name)
            await state.set_state(States.ONLY_PHONE)
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

            await bot.send_message(msg.chat.id, "🤩Спасибо🤩" + msg.chat.first_name)
            await state.set_state(States.ONLY_PHONE)


        except:
            print("error parse phone number")
            await bot.send_message(msg.chat.id, "вы неверно ввели телефон, можете прислать его в формате 88008454545, без тире, или воспользоваться кнопкой внизу")
            return -1

        # await state.set_state(States.NEW_SHOP_ST_2)
        # key = types.ReplyKeyboardMarkup(True, True)
        # key.add(button_phone)
        # await bot.send_message(msg.chat.id, "вы явно сделали что - то не так, используйте клавиатуру внизу",
        #                        reply_markup=key)
        # return -1

    #
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
             "where shop_id = '%s' and cost <='%s' ;")
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
            ch = await bot.send_photo(msg.chat.id, photo=current[1], caption=current[2] + " цена:" + str(current[4]) + "\nдоставка:" + " уточним у менеджера" + "\n#" + str(current[0]) + "#", reply_markup=kb1)
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


@dp.message_handler(state=States.CART)
async def cart(msg: types.Message, state=FSMContext):
    state = dp.current_state(user=msg.chat.id)


    if msg.text == "☆ ↩️ Назад ↩️ ☆":
        print("назад при инлайн")
        cost_str = get_query("select order_cost from orders where client_order_id = '%s'", (msg.chat.id,))
        print(cost_str)
        strS = re.search(r'\d{4}', str(cost_str))

        if not strS:
            await bot.send_message(msg.chat.id, "выберите цену используя клавиатуру ниже", reply_markup=COST)
            await state.set_state(States.COST)
            return -1

        print(strS[0])
        cost_str = strS[0]

        sqlin = ("update flobot.orders"
                 " set order_cost = %s"
                 "where client_order_id = '%s';")
        value = (cost_str, msg.chat.id)
        commit_query(sqlin, value)

        regex_dict
        key_dict = {}
        shop_id = get_query("select shop_order_id from orders where client_order_id = %s;", (msg.chat.id,))

        cnx = connect()
        curs = cnx.cursor()
        cost = get_query("select order_cost from orders where client_order_id = %s;", (msg.chat.id,))
        curs.execute("select categories from products where shop_id = '%s' and cost < %s;", (shop_id, cost,))
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
            await bot.send_message(msg.chat.id,
                                   "🔥💐похоже, у магазина нет букетов в этом ценовом диапозоне, выберите другой",
                                   reply_markup=COST)
            return -1
        keys.row("☆ ↩️ Назад ↩️ ☆")
        keys.row("к магазинам")
        await state.set_state(States.FLOWER_CATALOG)
        await bot.send_message(msg.chat.id, "🔥💐Отлично, теперь выберите цветы, если выбор вас не устраивает - вернитесь на несколько пункотов назад и выберите другой магазин", reply_markup=keys)
        await bot.send_message(msg.chat.id,
                               "если ваших цветов нет,выберите другой магазин",
                               reply_markup=keys)

        await send_video_instruction(msg, 'order_caption', "flowers")

    elif msg.text == "корзина":
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
        for i in row:
            str1 = str1 + str(i[3]) + " шт: " + str(i[2]) + '\n'
        print(str1)
        cnx.close()

        ans = types.ReplyKeyboardMarkup(True, True)
        ans.row("ОФОРМИТЬ ЗАКАЗ", "ИСКАТЬ НАИЛУЧШУЮ ЦЕНУ")
        ans.row("☆ ↩️ Назад ↩️ ☆", "★ ⬆️ В начало ⬆️ ★")
        await bot.send_message(msg.chat.id, str1, reply_markup=ans)
        await state.set_state(States.ORDERING_BUCKET)

    elif msg.text == "★ ⬆️ В начало ⬆️ ★":
        await msg.reply("используйте клавиатуру ниже:", reply_markup=INIT_KEYBOARD)
        await state.set_state(States.AFT_INIT_STATE)
        return -1
    elif msg.text == "мои заказы":
        print("q")
        await bot.send_message(msg.chat.id, "ваши заказы")


@dp.message_handler(state=States.ORDERING_BUCKET)
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


    elif msg.text == "ИСКАТЬ НАИЛУЧШУЮ ЦЕНУ":

        cnx = connect()
        curs = cnx.cursor()
        curs.execute("select order_id from orders where client_order_id = {};".format(msg.chat.id))
        order = curs.fetchone()
        order_id = msg.chat.id
        task = asyncio.create_task(auction(order_id))
        # await auction(order_id) # todo auction
        print("first place")
        final_offer = ''
        cnx = connect()

        cursor = cnx.cursor()

        sqlin = ("select cart.client_id, cart.amount, products.cost, cart.id, products.caption, products.file_id "
                 "from flobot.cart "
                 "left join flobot.products on cart.product_id = products.id"
                 " where client_id = '%s';")
        value = (msg.chat.id,)
        cursor.execute(sqlin, value)
        curs = cursor.fetchall()
        kb = types.InlineKeyboardMarkup()
        auct = types.InlineKeyboardButton(callback_data='auction', text="сделаем дешевле")
        kb.add(auct)

        for auction_order in auctions:
            if auction_order["client_id"] == order_id:
                for manager in auction_order["managers"]:
                    mngr = manager[0]
                    for tow in curs:
                        final_cost = int(tow[1]) * int(tow[2])
                        auction_order["curr_cost"] = final_cost
                        final_offer = final_offer + "\n" + str(tow[1]) + "\n шт:" + str(tow[4])
                        auction_order["offer"] = final_offer
                        auction_order["photos"].append(tow[5])
                        await bot.send_photo(mngr, tow[5],
                                             str(msg.chat.id) + ':' + str(tow[3]) + '\n' + final_offer + '\n' + str(final_cost),
                                             reply_markup=kb)
                        men_state = dp.current_state(user=mngr, chat=mngr)
                        await men_state.set_state(States.auctions)
                        await bot.send_message(mngr, "вы можете поучаствовать в английском аукционе, "
                                                        "клиент прислал заказ - сможете собрать подобный "
                                                        "букет дешевле - заказ уйдет вам")


    elif msg.text == "ОФОРМИТЬ ЗАКАЗ":
        final_cost = 0
        final_offer = ""
        amount = 0
        photo = ""
        cnx = connect()

        cursor = cnx.cursor()

        sqlin = ("select cart.client_id, cart.amount, products.cost, cart.id, products.caption, products.file_id "
                 "from flobot.cart "
                 "left join flobot.products on cart.product_id = products.id"
                 " where client_id = '%s';")
        value = (msg.chat.id,)
        cursor.execute(sqlin, value)
        curs = cursor.fetchall()
        for row in curs:
            final_cost += int(row[1]) * int(row[2])
            final_offer = final_offer + '\n' + str(row[1]) + "\n шт:" + str(row[4])
        #########
        shop_id = 0
        cnx.close()
        cnx = connect()

        cursor = cnx.cursor()

        sql = ("select shop_order_id from flobot.orders where client_order_id = '%s';")
        cursor.execute(sql, (msg.chat.id,))

        for row in cursor:
            print(row[0], "!!")
            shop_id = row[0]

        cursor.close()
        cnx.close()
        ###########
        cnx = connect()

        cursor = cnx.cursor()

        sql = ("select manager_chat_id from flobot.managers where shop_id = '%s';")
        cursor.execute(sql, (shop_id,))
        curs_managers = cursor.fetchall()
        print(curs_managers)
        for row in curs_managers:
            print(row[0], "!!!!!!loop for managers@!!!!!!!!!")

            ####################
            kb = types.InlineKeyboardMarkup()
            bm1 = types.InlineKeyboardButton("подтвердить наличие", callback_data='prove')
            bm2 = types.InlineKeyboardButton("нет в наличии", callback_data='disapprove')
            kb.add(bm1, bm2)
            kbk = types.InlineKeyboardMarkup()
            bm3 = types.InlineKeyboardButton("сформировать ответное предложение", callback_data='men_answer')
            kbk.add(bm3)
            final_offer = ""
            for tow in curs:
                final_cost = int(tow[1]) * int(tow[2])
                final_offer = final_offer + '\n' + str(tow[1]) + "\n шт:" + str(tow[4])
                await bot.send_photo(row[0], tow[5],
                                     str(msg.chat.id) + ':' + str(tow[3]) + '\n' + final_offer + '\n' + str(final_cost),
                                     reply_markup=kb)


            sql1 = "select order_shipping_adress from orders where client_order_id = %s;"
            val = (msg.chat.id,)
            addr = get_query(sql1, val)
            await bot.send_message(row[0], "адрес доставки:" + addr + "\nпришлите стоимость доставки, в рублях")

            zapis = {
                'id_client': msg.chat.id,
                'id_manager' : row[0],
                'cost' : 0
            }
            array.append(zapis)

            await bot.send_message(row[0], str(
                msg.chat.id) + '\n' + "как закончите с заказом, нажмите кнопку \"сформировать ответное предложение\"",
                                   reply_markup=kbk)

            manager_state = dp.current_state(chat=row[0], user=row[0])
            await manager_state.set_state(States.wait_for_delivery_cost)


        # await bot.send_message(row[0], str(msg.chat.id) + '\n' "final cost: "+ str(final_cost) + "\nfinal_offer:\n" + str(final_offer), reply_markup=kb)
        await bot.send_message(msg.chat.id, "ожидайте, мы подтвердим наличие заказа")
        await state.set_state(States.CART)
    else:
        ans = types.ReplyKeyboardMarkup(True, True)
        ans.row("ОФОРМИТЬ ЗАКАЗ", "ИСКАТЬ НАИЛУЧШУЮ ЦЕНУ")
        ans.row("☆ ↩️ Назад ↩️ ☆", "★ ⬆️ В начало ⬆️ ★")
        await state.set_state(States.ORDERING_BUCKET)
        await bot.send_message(msg.chat.id, "Упс, я не понял... Пожалуйста, напишите название как-нибудь по-другому 🙏",
                               reply_markup=ans)


@dp.message_handler(state=States.wait_for_delivery_cost) #
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




@dp.callback_query_handler(lambda c: c.data == 'auction', state=States.auctions)
async def process_callback_add(callback_query: types.CallbackQuery):
    print("auction")
    state = dp.current_state(user=callback_query.from_user.id)
    await callback_query.answer("auction")
    await bot.answer_callback_query(callback_query.id, "auction")
    mid = callback_query.message.message_id
    txt = caption = callback_query["message"]["caption"]

    print(txt)
    result1 = txt.find(":")
    result2 = txt.find("\n")
    id_pay = txt[:result1]
    print(id_pay)
    data = {
        "id_ordr": int(id_pay)
    }

    await state.update_data(ordr_id=int(id_pay))
    await bot.send_message(callback_query.from_user.id, "пришлите новую стоимость")

@dp.message_handler(state=States.auctions)
async def cart(msg: types.Message, state=FSMContext):
    cost = msg.text
    await bot.send_message(msg.chat.id, f"новая стоимость: {cost}")
    state = dp.current_state(user=msg.chat.id)
    data = await state.get_data()
    print(data["ordr_id"])
    ordr_id = data["ordr_id"]

    final_offer = ''
    cnx = connect()

    cursor = cnx.cursor()

    sqlin = ("select cart.client_id, cart.amount, products.cost, cart.id, products.caption, products.file_id "
             "from flobot.cart "
             "left join flobot.products on cart.product_id = products.id"
             " where client_id = '%s';")
    value = (ordr_id,)
    cursor.execute(sqlin, value)
    curs = cursor.fetchall()
    kb = types.InlineKeyboardMarkup()
    auct = types.InlineKeyboardButton(callback_data='auction', text="сделаем дешевле")
    kb.add(auct)
    final_cost = cost
    for auction_order in auctions:
        if auction_order["client_id"] == ordr_id:
            for manager in auction_order["managers"]:
                mngr = manager[0]
                auction_order["curr_cost"] = cost
                auction_order["curr_manager"] = msg.chat.id
                for tow in curs:
                    await bot.send_photo(mngr, tow[5],
                                     str(msg.chat.id) + ':' + str(tow[3]) + '\n' + final_offer + '\n' + str(final_cost),
                                     reply_markup=kb)
                    men_state = dp.current_state(user=mngr, chat=mngr)
                    await men_state.set_state(States.auctions)
                    print("он тут был")
                    await bot.send_message(mngr, "вы можете поучаствовать в английском аукционе, "
                                             "клиент прислал заказ - сможете собрать подобный "
                                             "букет дешевле - заказ уйдет вам")



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
    await bot.send_message(callback_query.from_user.id, "вы подтвердили наличие одного из букетов, как закончите, введите стоимость доставки")
    await bot.send_message(int(txt[:result1]), "подтвердили один из букетов")
    # print(result)
    cnx.close()


@dp.callback_query_handler(lambda c: c.data == 'men_answer', state='*')
async def kek(callback_query: types.CallbackQuery):
    print("men_answer")
    await bot.answer_callback_query(callback_query.id, "men_answer")
    mid = callback_query.message.message_id
    txt = callback_query.message.text
    result = txt.find("\n")
    print(result)
    final_cost = 0
    final_offer = ""

    cnx = connect()
    cursor = cnx.cursor()
    sqlinn = (""" select client_id from successful_payment where status = 'CONFIRMED' and client_id = %s; """)
    v = ((txt[:result]),)
    cursor.execute(sqlinn, v)
    first_gift = cursor.fetchall()
    print(first_gift)

    cnx = connect()

    cursor = cnx.cursor()

    sqlin = (
        """select cart.client_id, products.caption, cart.amount, products.cost, products.file_id, cart.st, shops.tink_shop_code, cart.id, shops.shop_id
        from flobot.cart 
        left join products on cart.product_id = products.id 
        left join shops on products.shop_id = shops.shop_id 
        where client_id = %s and st = %s ;""")
    value = ((txt[:result]), "prove")
    cursor.execute(sqlin, value)
    curs = cursor.fetchall()
    shop_id = 0
    ordr_id = 0
    Items = []
    shops = []
    delivery_cost = 0
    for z in array:
        if callback_query.from_user.id == z['id_manager']:
            delivery_cost = z['cost']
    print(delivery_cost)
    shiper = {
            "Name": "доставка",
            "Price": delivery_cost * 100,
            "Quantity": 1,
            "Amount": delivery_cost * 100,  # price * quantity
            "Tax": "vat10",
            "ShopCode": curs[0][6]
        }
    final_cost += int(delivery_cost)
    Items.append(shiper)

    for row in curs:
        product = {
            "Name": "",
            "Price": 0,
            "Quantity": 0,
            "Amount": 0,  # price * quantity
            "Tax": "vat10",
            "ShopCode": ""
        }

        product["Name"] = row[1]

        if first_gift:
            product["Price"] = int(row[3]) * 100
            final_cost += int(row[2]) * int(row[3])
        else:
            product["Price"] = int(row[3]) * 70 # 50
            final_cost += int(row[2]) * int(row[3]) * 0.7 # 0.5

        product["Quantity"] = int(row[2])
        product["Amount"] = product["Price"] * product["Quantity"]
        product["ShopCode"] = str(row[6])  # str(row[6])
        shop_id = row[8]
        print(product, '\n')


        Items.append(product)
        for i in Items:
            print(i, "@@")
        final_offer = final_offer + '\n' + row[1] + "\n шт:" + str(row[2])

        ordr_id = row[7]
        shops = [
            {
                "ShopCode": row[6],  # row[6]
                "Amount": final_cost * 100,
                "Name": "букеты"
            },
            # {
            # "ShopCode": "700017436",
            # "Amount": "140000",
            # "Name": "варежки"
            # },
        ]

    print("final_cost", final_cost)
    print("final_offer", final_offer)

    ttxt = txt[result:]
    print("ttxt", ttxt)

    from tink_payment import payment

    pay = payment("1615725763495", "2illo2v6pxz3brce")  # TODO upd config.py ("1615725763495", "n2YLD8x0hd")

    print(Items)

    resp = pay.init_pay(shops, Items, ordr_id)
    print(resp)
    if resp['Success'] == False:
        print("error failure payment")
    else:
        confirmation_url = resp["PaymentURL"]
        c = str(float(final_cost))
        str_inv = "Pay: " + c + " RUB"
        print(str_inv, "qq")
        inv = types.InlineKeyboardMarkup()
        bm1 = types.InlineKeyboardButton(str_inv, url=confirmation_url)
        inv.add(bm1)
        cnx.close()
        import time
        print(time.strftime('%Y-%m-%d %H:%M:%S'))
        await bot.send_message(int(txt[:result]), final_offer, reply_markup=inv)

        sqlin = (
            "insert into flobot.successful_payment(provider_payment_charge_id, caption, cost, client_id, status, create_at, shop_id)"
            "values (%s, %s, %s, %s, %s, %s, %s);")
        value = (resp['PaymentId'], final_offer, float(final_cost), int(txt[:result]), resp["Status"],
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
        await bot.send_message(int(txt[:result]), "не забудьте вернуться к нам и подтвердить свою оплату заказа " + str(
            row[0]) + "! иначе не дождётесь свой букет))", reply_markup=kb1)
        cnx.close()
        await bot.send_message(callback_query.from_user.id, "вы все сделали правильно, клиент уже направлен на оплату")
        await bot.send_message(callback_query.from_user.id, "как только клиент подтвердит оплату - вам придут его контактные данные и точный адрес доставки")

# @dp.callback_query_handler(lambda c: c.data == 'prove', state='*')
# async def process_callback_add(callback_query: types.CallbackQuery):
#     print("prove")
#     await callback_query.answer("prove")
#     await bot.answer_callback_query(callback_query.id, "prove")
#     mid = callback_query.message.message_id
#     txt = caption = callback_query["message"]["caption"]
#     print(txt)
#     result1 = txt.find(":")
#     result2 = txt.find("\n")
#     id_pay = txt[result1 + 1:result2]
#     print(id_pay)
#     cnx = connect()
#
#     cursor = cnx.cursor()
#     sql = ("update flobot.cart"
#            " set cart.st=%s where id = '%s';")
#     value = ("prove", int(id_pay))
#     txxt = txt[result2:]
#     cursor.execute(sql, value)
#     print("!!", cnx.commit())
#     result = txxt.find("\n")
#     ttxt = txt[result:]
#     print(ttxt)
#     await bot.send_message(int(txt[:result1]), "подтвердили один из букетов")
#     # print(result)
#     cnx.close()


# @dp.callback_query_handler(lambda c: c.data == 'men_answer', state='*')
# async def kek(callback_query: types.CallbackQuery):
#     print("men_answer")
#     await bot.answer_callback_query(callback_query.id, "men_answer")
#     mid = callback_query.message.message_id
#     txt = callback_query.message.text
#     result = txt.find("\n")
#     print(result)
#     final_cost = 0
#     final_offer = ""
#
#     cnx = connect()
#     cursor = cnx.cursor()
#     sqlinn = (""" select client_id from successful_payment where status = 'CONFIRMED' and client_id = %s; """)
#     v = ((txt[:result]),)
#     cursor.execute(sqlinn, v)
#     first_gift = cursor.fetchall()
#     print(first_gift)
#
#     cnx = connect()
#
#     cursor = cnx.cursor()
#
#     sqlin = (
#         """select cart.client_id, products.caption, cart.amount, products.cost, products.file_id, cart.st, shops.tink_shop_code, cart.id, shops.shop_id
#         from flobot.cart
#         left join products on cart.product_id = products.id
#         left join shops on products.shop_id = shops.shop_id
#         where client_id = %s and st = %s ;""")
#     value = ((txt[:result]), "prove")
#     cursor.execute(sqlin, value)
#     curs = cursor.fetchall()
#     shop_id = 0
#     ordr_id = 0
#     Items = []
#     shops = []
#     product = {
#         "Name": "",
#         "Price": 0,
#         "Quantity": 0,
#         "Amount": 0,  # price * quantity
#         "Tax": "vat10",
#         "ShopCode": ""
#     }
#     for row in curs:
#         product["Name"] = row[1]
#
#         if first_gift:
#             product["Price"] = int(row[3]) * 100
#             final_cost += int(row[2]) * int(row[3])
#         else:
#             product["Price"] = int(row[3]) * 50
#             final_cost += int(row[2]) * int(row[3]) * 0.5
#
#         product["Quantity"] = int(row[2])
#         product["Amount"] = product["Price"] * product["Quantity"]
#         product["ShopCode"] = str(row[6])  # str(row[6])
#         shop_id = row[8]
#         print(product, '\n')
#
#         final_offer = final_offer + '\n' + row[1] + "\n шт:" + str(row[2])
#
#         Items.append(product)
#         ordr_id = row[7]
#         shops = [
#             {
#                 "ShopCode": row[6],  # row[6]
#                 "Amount": final_cost * 100,
#                 "Name": "букеты"
#             },
#             # {
#             # "ShopCode": "700017436",
#             # "Amount": "140000",
#             # "Name": "варежки"
#             # },
#         ]
#
#     print("final_cost", final_cost)
#     print("final_offer", final_offer)
#
#     ttxt = txt[result:]
#     print("ttxt", ttxt)
#
#     from tink_payment import payment
#
#     pay = payment("1615725763495", "2illo2v6pxz3brce")  # TODO upd config.py ("1615725763495", "n2YLD8x0hd")
#     resp = pay.init_pay(shops, Items, ordr_id)
#     print(resp)
#     if resp['Success'] == False:
#         print("error failure payment")
#     else:
#         confirmation_url = resp["PaymentURL"]
#         c = str(float(final_cost))
#         str_inv = "Pay: " + c + " RUB"
#         print(str_inv, "qq")
#         inv = types.InlineKeyboardMarkup()
#         bm1 = types.InlineKeyboardButton(str_inv, url=confirmation_url)
#         inv.add(bm1)
#         cnx.close()
#         import time
#         print(time.strftime('%Y-%m-%d %H:%M:%S'))
#         await bot.send_message(int(txt[:result]), final_offer, reply_markup=inv)
#
#         sqlin = (
#             "insert into flobot.successful_payment(provider_payment_charge_id, caption, cost, client_id, status, create_at, shop_id)"
#             "values (%s, %s, %s, %s, %s, %s, &s);")
#         value = (resp['PaymentId'], final_offer, float(final_cost), int(txt[:result]), resp["Status"],
#                  time.strftime('%Y-%m-%d %H:%M:%S'), shop_id)
#         commit_query(sqlin, value)
#
#         cnx = connect()
#
#         cursor = cnx.cursor()
#
#         sql = ("select id from flobot.successful_payment where provider_payment_charge_id = %s;")
#         cursor.execute(sql, (resp['PaymentId'],))
#         row = cursor.fetchone()
#         kb1 = types.InlineKeyboardMarkup()
#         bm2 = types.InlineKeyboardButton("подтвердить", callback_data="invoice")
#         kb1.add(bm2)
#         await bot.send_message(int(txt[:result]), "не забудьте вернуться к нам и подтвердить свою оплату заказа " + str(
#             row[0]) + "! иначе не дождётесь свой букет))", reply_markup=kb1)
#         cnx.close()


@dp.message_handler(state=States.auctions1)
async def refund(msg: types.Message, state=FSMContext):
    print("second place")
    delivery_cost = msg.text
    for ordr in auctions:
        print(ordr, "all")
        if ordr["curr_manager"] == msg.chat.id:
            await bot.send_message(ADMIN_CHAT_ID, ordr["curr_cost"])
            final_cost = ordr["curr_cost"]
            final_offer = ordr["offer"]
            amount = 1
            photo = ordr["photos"]

            cnx = connect()
            cursor = cnx.cursor()
            sqlinn = (""" select client_id from successful_payment where status = 'CONFIRMED' and client_id = %s; """)
            v = (ordr["client_id"],)
            cursor.execute(sqlinn, v)
            first_gift = cursor.fetchall()
            print(first_gift)
            cnx = connect()
            cursor = cnx.cursor()
            shop_id = 0
            ordr_id = 0
            Items = []
            shops = []
            sql = "select shop_id from managers where manager_chat_id = {};".format(msg.chat.id)
            cnx = connect()
            curs = cnx.cursor()
            curs.execute(sql)
            shop_id = curs.fetchone()[0]
            sql = "select tink_shop_code from shops where shop_id = {};".format(shop_id)
            curs.execute(sql)
            shop_code = curs.fetchone()[0]
            print(delivery_cost)
            shiper = {
                "Name": "доставка",
                "Price": delivery_cost * 100,
                "Quantity": 1,
                "Amount": delivery_cost * 100,  # price * quantity
                "Tax": "vat10",
                "ShopCode": shop_code
            }
            # final_cost += int(delivery_cost)
            Items.append(shiper)

            product = {
                "Name": "",
                "Price": 0,
                "Quantity": 0,
                "Amount": 0,  # price * quantity
                "Tax": "vat10",
                "ShopCode": ""
            }

            product["Name"] = ordr["offer"]

            if first_gift:
                product["Price"] = int(ordr["curr_cost"]) * 100
            else:
                product["Price"] = int(ordr["curr_cost"]) * 70  # 50
                # final_cost += int(row[2]) * int(row[3]) * 0.7  # 0.5

            product["Quantity"] = 1
            product["Amount"] = int(product["Price"]) * int(product["Quantity"])
            product["ShopCode"] = str(shop_code)  # str(row[6])

            print(product, '\n')
            print(product["Price"], product["Quantity"], "@@")
            Items.append(product)
            for i in Items:
                print(i, "@@")
            # final_offer = final_offer + '\n' + row[1] + "\n шт:" + str(row[2])

            cnx = connect()
            curs = cnx.cursor()
            curs.execute("select id from successful_payment order by id desc;")
            ordr = curs.fetchone()

            ordr_id = ordr[0]
            shops = [
                {
                    "ShopCode": shop_code,  # row[6]
                    "Amount": int(final_cost) * 100,
                    "Name": "букеты"
                },
                # {
                # "ShopCode": "700017436",
                # "Amount": "140000",
                # "Name": "варежки"
                # },
            ]

            print("final_cost", final_cost)
            print("final_offer", final_offer)

            # ttxt = txt[result:]
            # print("ttxt", ttxt)

            from tink_payment import payment

            pay = payment("1615725763495", "2illo2v6pxz3brce")  # TODO upd config.py ("1615725763495", "n2YLD8x0hd")

            print(Items)
            resp = pay.init_pay(shops, Items, ordr_id)
            print(resp)
            if resp['Success'] == False:
                print("error failure payment")
            else:
                confirmation_url = resp["PaymentURL"]
                c = str(float(final_cost))
                str_inv = "Pay: " + c + " RUB"
                print(str_inv, "qq")
                inv = types.InlineKeyboardMarkup()
                bm1 = types.InlineKeyboardButton(str_inv, url=confirmation_url)
                inv.add(bm1)
                cnx.close()
                import time
                print(time.strftime('%Y-%m-%d %H:%M:%S'))
                await bot.send_message(int(ordr["client_id"]), final_offer, reply_markup=inv)

                sqlin = (
                    "insert into flobot.successful_payment(provider_payment_charge_id, caption, cost, client_id, status, create_at, shop_id)"
                    "values (%s, %s, %s, %s, %s, %s, %s);")
                value = (resp['PaymentId'], final_offer, float(final_cost), int(ordr["client_id"]), resp["Status"],
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
                await bot.send_message(int(ordr["client_id"]),
                                       "не забудьте вернуться к нам и подтвердить свою оплату заказа " + str(
                                           row[0]) + "! иначе не дождётесь свой букет))", reply_markup=kb1)
                cnx.close()
                await bot.send_message(ordr["client_id"],
                                       "вы все сделали правильно, клиент уже направлен на оплату")
                await bot.send_message(ordr["client_id"],
                                       "как только клиент подтвердит оплату - вам придут его контактные данные и точный адрес доставки")


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
        msg4 = "финальная цена: \ntесли вы участвовали в аукционе - фактическая цена оплаты будет отличаться" + str(cc) + '\n'
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
        commit_query("update orders set add_flowers = 'yes' where client_order_id = %s;", (callback_query.from_user.id,))
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


@dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT, state='*')
async def process_successful_payment(message: types.SuccessfulPayment):
    print(message)
    await bot.send_message(
        message.chat.id,
        MESSAGES['successful_payment'].format(
            total_amount=message.successful_payment.total_amount // 100,
            currency=message.successful_payment.currency
        )
    )
    shop_id = 0
    cnx = connect()

    cursor = cnx.cursor()

    sql = ("select shop_order_id from flobot.orders where client_order_id = '%s';")
    cursor.execute(sql, (message.chat.id,))

    for row in cursor:
        print(row[0])
        shop_id = row[0]

    cursor.close()
    cnx.close()
    # =====================================================================
    cnx = connect()

    cursor = cnx.cursor()

    sql = ("select manager_chat_id from flobot.shops where shop_id = '%s';")
    cursor.execute(sql, (shop_id,))
    for row in cursor:
        print(row[0])

    await bot.send_message(392875761, "succesed payment, manager! client" + str(message.chat.id) + ' ' + str(
        message.chat.username) + ""
                                 " " + str(message.successful_payment['total_amount']) + message.successful_payment[
                               'provider_payment_charge_id'])

    cursor.close()
    cnx.close()

    cnx = connect()

    cursor = cnx.cursor()

    sql = ("insert into flobot.successful_payment(provider_payment_charge_id, cost, client_id) values(%s, '%s', '%s');")
    cursor.execute(sql, (
        message.successful_payment['provider_payment_charge_id'], message["successful_payment"]["total_amount"],
        message["from"]["id"]))
    cnx.commit()
    cursor.close()
    cnx.close()


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


@dp.message_handler(state=States.CURRENT_SHOP)
async def echo(msg: types.Message, state=FSMContext):
    cnx = connect()
    cursor = cnx.cursor()
    sqlin = ("select shop_id from flobot.shops where shop_name = %s;")

    value = (msg.text,)
    cursor.execute(sqlin, value)
    print("ok!")
    result = cursor.fetchone()
    cnx.close()
    if result == None:
        await msg.reply("не смог найти ваш магазин", reply_markup=INIT_KEYBOARD)
        await state.set_state(States.AFT_INIT_STATE)
    else:
        id = result[0]
        Key = types.ReplyKeyboardMarkup(True, True)
        Key.row("да")
        Key.row("нет, вернуться назад")
        await bot.send_message(msg.chat.id, "да, обнаружил этот магазин. хотите оформить заказ из него?",
                               reply_markup=Key)
        #
        cnx = connect()

        cursor = cnx.cursor()

        sqlin = ("update flobot.orders"
                 " set shop_order_id = '%s'"
                 "where client_order_id = '%s';")
        value = (id, msg.chat.id)
        cursor.execute(sqlin, value)
        cnx.commit()
        cnx.close()
        #
        await state.set_state(States.FIND_SHOP)


@dp.message_handler(state=States.FIND_SHOP)
async def echo(message: types.Message, state=FSMContext):
    if message.text == "да":
        Key = types.ReplyKeyboardMarkup(True, True)
        Key.row("вернуться в начало")
        await message.reply("напишите адрес доcтавки в формате \"ул никольская 3\"", reply_markup=Key)
        await state.set_state(States.SHOP_GEO)

    if message.text == "нет, вернуться назад":
        await message.reply("используйте клавиатуру ниже:", reply_markup=INIT_KEYBOARD)
        await state.set_state(States.AFT_INIT_STATE)


@dp.message_handler(state=States.SHOP_GEO)
async def echo(msg: types.Message, state=FSMContext):
    if msg.text == "вернуться в начало":
        await msg.reply("используйте клавиатуру ниже:", reply_markup=INIT_KEYBOARD)
        await state.set_state(States.AFT_INIT_STATE)
        return -1

    from dadata import DadataAsync
    token = DADATA_TOKEN
    secret = "0f543bff141d1fa34b465031dc89512244162ff0"
    dadata = DadataAsync(token)
    result = await dadata.suggest("address", msg.text)
    await dadata.close()
    current_value = ""

    for i in result:
        value = i['value']
        current_value = value
        print(value)
        break
    str = current_value + " адрес доставки"

    await bot.send_message(msg.chat.id, str, reply_markup=KEYBOARD3)
    sqlin = ("update flobot.orders"
             " set "
             "order_shipping_adress = %s "
             "where client_order_id = '%s';")
    value = (current_value, msg.chat.id)
    commit_query(sqlin, value)
    await state.set_state(States.SHOP_GEO_PROVE)


@dp.message_handler(state=States.SHOP_GEO_PROVE)
async def echo_message(msg: types.Message, state=FSMContext):
    state = dp.current_state(user=msg.chat.id)

    id = msg.chat.id

    if msg.text == "🟥↩️ Не верно, вернуться назад ↩️🟥":
        Key = types.ReplyKeyboardMarkup(True, True)
        Key.row("вернуться в начало")
        await msg.reply("напишите адрес дотставки в формате \"ул никольская 3\"", reply_markup=Key)
        await state.set_state(States.SHOP_GEO)

    elif msg.text == "✅ Все верно ✅":
        await state.set_state(States.COST)
        await bot.send_message(msg.chat.id, "отлично, теперь выберите предполагаемую ценовую категорию",
                               reply_markup=COST)


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
                           "перечислите цветы в составе букета через запятую пример:\n\"пионы, розы \"\n не более 15-20 слов")


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
    await state.set_state(States.UPLOAD2)
    await bot.send_message(msg.chat.id, "цена? в рублях \"1000\"")


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


@dp.message_handler(state='*')
async def echo(msg: types.Message):
    print("echo")
    # print(msg.photo[-1].file_id)
    state = dp.current_state()
    if msg.text == "★ ⬆️ В начало ⬆️ ★":
        await bot.send_message(msg.chat.id, "начнем заново", reply_markup=INIT_KEYBOARD)
        await state.set_state(States.AFT_INIT_STATE)

