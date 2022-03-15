from math import *
from datetime import datetime
import config
from loader import dp, bot, auctions, ADMIN_CHAT_ID, instagram_basic_display
from config import *
import re
from async_auction import auction
import asyncio
from keyboards import TMP, INIT_KEYBOARD, TO_ME, COST, regex_dict, button_phone, REP_KEY_WHEN_INLINE, FLOWER_KEYS
from video_instruction import mailing
from utils import States
from aiogram import types
from dbcm import connect, commit_query, get_query, get_query_all
from video_instruction import bot_videos, send_video_instruction
from aiogram.dispatcher import FSMContext



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


