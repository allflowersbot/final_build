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
            product["Price"] = int(row[3]) * 70  # 50
            final_cost += int(row[2]) * int(row[3]) * 0.7  # 0.5

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

    resp, Amount = pay.init_pay(shops, Items, ordr_id)
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
        await bot.send_message(callback_query.from_user.id,
                               "как только клиент подтвердит оплату - вам придут его контактные данные и точный адрес доставки")
