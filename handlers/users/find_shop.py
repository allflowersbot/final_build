from math import *
from datetime import datetime
import config
from loader import dp, bot, auctions, ADMIN_CHAT_ID, array
from config import *
import re
from async_auction import auction
import asyncio
from keyboards import TMP, INIT_KEYBOARD, TO_ME, COST, KEYBOARD3
from video_instruction import mailing
from utils import States
from aiogram import types
from dbcm import connect, commit_query, get_query, get_query_all
from video_instruction import bot_videos, send_video_instruction
from aiogram.dispatcher import FSMContext


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

