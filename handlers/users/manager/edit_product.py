from loader import dp, bot, auctions, ADMIN_CHAT_ID, current_products
from config import *
import re
from keyboards import MAIL, INIT_KEYBOARD, manager_mode_keys, manager_mode_edit_keys, FLOWER_KEYS
from video_instruction import mailing
from utils import States
from aiogram import types
from dbcm import connect, commit_query, get_query

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

