import asyncio

import dbcm
from dbcm import commit_query, connect, get_query
from aiogram import Bot, types

from config import TEST_BOT_TOKEN, BOT_TOKEN

bot = Bot(token=BOT_TOKEN)

test_bot_videos = {
              'start': "BAACAgIAAxkDAAIKXmDchaMYbRa5sbNIyLjZT4JnqIBkAALcDQACLvjgSgy7Dh_OGo1bIAQ",
              'addr': 'BAACAgIAAxkDAAIKTmDcgdDqOC4cXUAxtyhb-BhoqBqrAAK9DQACLvjgSq7fy0UwnIuHIAQ',
              'cost': "BAACAgIAAxkDAAIKUGDcgpQUPcyNGB28mOXoW15jY-2kAAK_DQACLvjgSuxp6H7lA_ZSIAQ",
              'flowers': "BAACAgIAAxkDAAIKUmDcgtHUFmrF7V3KaqDXKmin9vsPAALBDQACLvjgSltrLVRn7_8_IAQ",
              'correct_data': "BAACAgIAAxkDAAIKVGDcgzT4Q0DDPsVnH22zv5YWSZgLAALHDQACLvjgSgyGowR8AAFDSyAE",
              'delivery': "BAACAgIAAxkDAAIKVmDcg54Qj5JR2EH8bU3EV6X1N9JwAALMDQACLvjgSjZFtEE_VacYIAQ",
              'phone': "BAACAgIAAxkDAAIKWGDcg_bDKe3qrfXlpTf3lP23dKRRAALSDQACLvjgSo-pFBMklrt4IAQ",
              'main_menu': "BAACAgIAAxkDAAIKWmDchDbxaqBFxd4dL9Az6iuWoXsKAALUDQACLvjgSnigL7DPimsEIAQ",
              'ordering' : "BAACAgIAAxkDAAIKXGDchUuvd22tRE8xmOkgsPQqs7BfAALZDQACLvjgSkq31WBi7iedIAQ",
              'confirmed': "BAACAgIAAxkDAAIKYGDchfx4sRGWjjKNt8cJe0fEi-AvAALdDQACLvjgSmg6x8tAHvRcIAQ",
              'add_flowers': "BAACAgIAAxkDAAIKYmDchjck_7tF0n1k4fPxNg9qiWGIAALeDQACLvjgSnr9a0gTyTljIAQ"
              }
bot_videos = {
              'start': "BAACAgIAAxkDAAEBaTdg3Iycx6Ze8sI2ZFTOU6b5AAHM4j4AAjANAAKMnOBKUja7lZ-fBM0gBA",
              'addr': 'BAACAgIAAxkDAAEBaThg3IyiSnvDa5e16nQTj7Hho4u2ogACMQ0AAoyc4EqQuroXnx1t0SAE',
              'cost': "BAACAgIAAxkDAAEBaTlg3Iykqs1wHbdeH65kblaF3iVQ0gACMg0AAoyc4Epr3jdrkpDLGyAE",
              'flowers': "BAACAgIAAxkDAAEBaTpg3IylAAHfKLRPSLSY51ZZhjwU9MEAAjMNAAKMnOBKw9gOLWc4N-cgBA",
              'correct_data': "BAACAgIAAxkDAAEBaTtg3Iyo--2-9K2xQDjfoBlsdEl2hgACNA0AAoyc4Er1DFmyi6oJMCAE",
              'delivery': "BAACAgIAAxkDAAEBaTxg3IyqneOlXPzcXFGo58jut4s0owACNQ0AAoyc4ErsiCHd5RjXaSAE",
              'phone': "BAACAgIAAxkDAAEBaT1g3Iys1Kh10zMAAS9Wvn3Y7tpCZksAAjYNAAKMnOBK0536l0kT2x4gBA",
              'main_menu': "BAACAgIAAxkDAAEBaT5g3Iyuyn5Pw__j_jeyiBu_xLSL_AACNw0AAoyc4EoULJXGhnPEaiAE",
              'ordering': "BAACAgIAAxkDAAEBaT9g3Iyv4xDqilSjmhm64Q_WoEFkRwACOA0AAoyc4EohZd-bnZMOLyAE",
              'confirmed': "BAACAgIAAxkDAAEBaUBg3IywaeoAARRWg1PWSJfMbDv6P6wAAjkNAAKMnOBK0RrHCM4ffckgBA",
              'add_flowers': "BAACAgIAAxkDAAEBaUFg3Iyybr_ZyiwSqPJLmMB1qTj_8wACOg0AAoyc4EoCSnOSJ_uZgiAE"
              }

mail = """Вы забыли забрать свой букет!

Привет! 💐 
Это команда Allflow. Мы заметили, что ты зашёл на нашу платформу, но так и не определился с выбором букета. 

На 1-й заказ действует скидка!
А доставка в радиусе 2-ух километров от магазина бесплатно!"""

mail1 = """Покупать нельзя раздумывать!

17 городов, 378 цветочных магазинов, бесплатная доставка и скидка 30% на первый заказ. 

Это и есть платформа Allflow.

Всё ещё думаете, покупать здесь или переплачивать другим платформам за разработанное мобильное приложение? 🤔

Ответ очевиден - выбирай адрес и радуй любимых свежими букетами по лучшим ценам💐"""

async def send_video_instruction(msg, argument, state):
    print("send_video")

    sql = "select {} from orders where client_order_id = {}".format(argument,msg.chat.id)
    cnx = dbcm.connect()
    curs = cnx.cursor()
    curs.execute(sql)
    info = curs.fetchone()
    print(info)
    if argument == "force":
        print('vid')
        # vid = test_bot_videos[state]
        vid = bot_videos[state]
        await bot.send_video(msg.chat.id, vid)
        return 0

    if info[0] is None:
        print('vid')
        # vid = test_bot_videos[state]
        vid = bot_videos[state]
        await bot.send_video(msg.chat.id, vid)


async def mailing(mode):
    if mode == 0:
        cur_mail = mail
    else:
        cur_mail = mail1
    sql = "select client_order_id from orders where order_shipping_adress is NULL or order_caption is null or order_cost is null;"
    cnx = dbcm.connect()
    curs = cnx.cursor()
    curs.execute(sql)
    info = curs.fetchall()
    i = 0
    for each in info:
        try:
            await bot.send_message(each[0], cur_mail)
        except:
            pass
        i+=1
    return i



async def process_callback_add():
    print("invoice")
    # await bot.answer_callback_query(callback_query.id, "invoice")
    flag = True
    # str1 = callback_query["message"]["text"]

    # i = str1.find("заказа")
    # j = str1.find("!")
    # id = str1[i + 7:j]
    id = 70
    print(id)
    cnx = connect()

    cursor = cnx.cursor()

    sql = ("select provider_payment_charge_id from flobot.successful_payment where id = '%s';")
    cursor.execute(sql, (int(id),))
    row = cursor.fetchone()

    payment_id = row[0]

    # print(callback_query)
    from tink_payment import payment

    pay = payment("1615725763495", "2illo2v6pxz3brce")
    resp = pay.get_state(payment_id)

    print(resp, payment_id, "!!!!!")
    # await bot.send_message(callback_query.from_user.id, "статус оплаты: " + resp["Status"])
    print(resp)
    r = "CONFIRMED"
    if resp["Status"] == "CONFIRMED":  # resp["Status"] == "CONFIRMED":

        sql = "select confirmed from orders where client_order_id = {}".format(624630819)
        cnx = connect()
        curs = cnx.cursor()
        curs.execute(sql)
        info = curs.fetchone()
        print(info)
        if info[0] is None:
            print('vid')
            # vid = test_bot_videos[state]
            vid = bot_videos['confirmed']
            # await bot.send_video(callback_query.from_user.id, vid)

        commit_query("update orders set ordering = 'yes' where client_order_id = %s", (624630819,))

        sql = (" update flobot.successful_payment "
               "set status = %s where successful_payment.id =%s;")
        value = ("CONFIRMED", int(id))
        commit_query(sql, value)

        sql = ("delete from flobot.cart where client_id = '%s'")
        value = (624630819,)
        commit_query(sql, value)

        st = types.InlineKeyboardMarkup()
        bn = types.InlineKeyboardButton("проблемы при пользовании", callback_data="helper")
        bn1 = types.InlineKeyboardButton("статус оплаты", callback_data="payment_status")
        st.add(bn, bn1)
        # await bot.send_message(624630819,
        #                        "поздравляю, вы сделали все правильно, менеджер уже начал делать букет", reply_markup=st)
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
        msg4 = "финальная цена: " + str(cc) + '\n'
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
        # await bot.send_message(callback_query.from_user.id,
        #                        "оплатите заказ, а если вы уже заплатили - нажмите кнопку 'подтвердить'",
        #                        reply_markup=st)

        cnx.close()



# loop = asyncio.get_event_loop()
# loop.run_until_complete(process_callback_add())

