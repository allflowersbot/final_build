from loader import dp, bot, auctions, ADMIN_CHAT_ID, current_products
from config import *
import re
from keyboards import MAIL, INIT_KEYBOARD, manager_mode_keys1, manager_mode_keys2, manager_mode_keys, FLOWER_KEYS
from video_instruction import mailing
from utils import States
from aiogram import types
from dbcm import connect, commit_query, get_query

list_of_id= []
list_of_id.append(ADMIN_CHAT_ID)
list_of_id.append(494609919)
#
# @dp.message_handler(state='*', commands=['show_buckets'])
# async def NS(msg: types.Message):
#     state = dp.current_state(user=msg.chat.id)
#     await state.set_state(States.default_buckets)
#     if msg.chat.id in list_of_id:
#         cnx = connect()
#         cursor = cnx.cursor()
#         sql = (" select * from default_buckets;")
#         cursor.execute(sql)
#         curs = cursor.fetchall()
#         for row in curs:
#             await bot.send_photo(msg.chat.id, row[2],str(row[3]) + '\n' + row[4] + '\n' + str(row[5]))
#     else:
#         await msg.answer("У вас нет прав доступа")
#

@dp.message_handler(content_types=types.ContentTypes.PHOTO, state=States.default_buckets)
async def NS(msg: types.Message):
    state = dp.current_state(user=msg.chat.id)
    if not msg.photo:
        await msg.answer("error send photos")
        return -1

    await bot.send_message(msg.chat.id, "photo")

    value = msg.photo[-1].file_id

    await state.update_data(file_id=value)
    await state.set_state(States.default_buckets_cap)
    await msg.answer("теперь описание")


@dp.message_handler(state=States.default_buckets_cap)
async def NS(msg: types.Message):
    state = dp.current_state(user=msg.chat.id)
    caption = msg.text
    cap = caption[:127]
    print(cap)
    await state.update_data(caption=cap)
    await state.set_state(States.default_buckets_categ)
    await msg.answer("теперь категории")

@dp.message_handler(state=States.default_buckets_categ)
async def NS(msg: types.Message):
    state = dp.current_state(user=msg.chat.id)
    categ = msg.text
    cat = categ[:127]
    print(cat)
    await state.update_data(categ=cat)
    await state.set_state(States.default_buckets_cost)
    await msg.answer("теперь цену")


@dp.message_handler(state=States.default_buckets_cost)
async def NS(msg: types.Message):
    state = dp.current_state(user=msg.chat.id)
    try:
        cost = int(msg.text)
    except:
        await bot.send_message(msg.chat.id, "цифрами, например '1000'")
        return -1
    await state.update_data(cost=cost)
    await state.set_state(States.default_buckets_prove)
    await msg.answer("так выглядит ваш букет:")
    data = await state.get_data()
    print(data)
    kb = types.InlineKeyboardMarkup()
    btn = types.InlineKeyboardButton(text="всё верно", callback_data='good')
    kb.add(btn)
    btn = types.InlineKeyboardButton(text="переделать", callback_data='bad')
    kb.add(btn)
    await bot.send_photo(msg.chat.id, data['file_id'], data['caption'] + '\n' + data['categ'] + '\n' + str(cost), reply_markup=kb)

@dp.callback_query_handler(lambda c: c.data == 'good', state=States.default_buckets_prove)
async def process_callback_add(callback_query: types.CallbackQuery):
    print(callback_query.message)
    await callback_query.answer("proving")
    state = dp.current_state(user=callback_query.from_user.id)
    data = await state.get_data()
    print(data)
    cnx = connect()
    cursor = cnx.cursor()
    # commit_query(
    #     "insert into products(file_id, caption, categories, cost, default_bucket) values(%s, %s, %s, %s, true);",
    #     (fow[0], fow[1], fow[2], fow[3]))
    print("udacha")
    cursor.execute("insert into products(file_id, caption, categories, cost, default_bucket) values(%s, %s, %s, %s, true);", (data["file_id"], data['caption'], data['categ'], data["cost"]))
    cnx.commit()
    await state.set_state(States.default_buckets)
    await bot.send_message(callback_query.from_user.id,
                               "букет добавлен\nфото->короткое описание->состав букета(наименования цветов через запятую)->цена")

@dp.callback_query_handler(lambda c: c.data == 'bad', state=States.default_buckets_prove)
async def process_callback_add(callback_query: types.CallbackQuery):
    print(callback_query.message)
    await callback_query.answer("proving")
    state = dp.current_state(user=callback_query.from_user.id)

    await bot.send_message(callback_query.from_user.id, "начните заново \nфото->короткое описание->состав букета(наименования цветов через запятую)->цена")
    await state.set_state(States.default_buckets)
