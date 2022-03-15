from handlers.reg_shop import regshop
from loader import dp, bot, auctions, ADMIN_CHAT_ID, current_products
from config import *
import re
from keyboards import MAIL, INIT_KEYBOARD, manager_mode_keys1, manager_mode_keys2, manager_mode_keys
from video_instruction import mailing
from utils import States
from aiogram import types
from dbcm import connect, commit_query, get_query, get_query_all


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
    state = dp.current_state(user=msg.chat.id)
    await state.set_state(States.manager_mode)