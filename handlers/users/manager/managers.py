from handlers.reg_shop import regshop
from loader import dp, bot, auctions, ADMIN_CHAT_ID, current_products
from config import *
import re
from keyboards import MAIL, INIT_KEYBOARD, manager_mode_keys1, manager_mode_keys2, manager_mode_keys
from video_instruction import mailing
from utils import States
from aiogram import types
from dbcm import connect, commit_query, get_query, get_query_all

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
        """ select is_open, shops.shop_id from shops left join managers on managers.shop_id = shops.shop_id where managers.manager_chat_id = %s """)
    val = (callback_query.from_user.id,)
    data = get_query_all(req, val)
    print(data)
    st = data[0]
    shop_id = data[1]
    print("visual_ability", st)

    if st == 'yes':
        st = 'no'
        await bot.edit_message_reply_markup(callback_query.from_user.id, msg_id, i_msg_id,
                                            reply_markup=manager_mode_keys2)
    elif st == 'no':
        st = 'yes'
        await bot.edit_message_reply_markup(callback_query.from_user.id, msg_id, i_msg_id,
                                            reply_markup=manager_mode_keys1)

    req = (
        """ update shops set is_open = %s where shop_id = %s; """)
    val = (st, shop_id,)
    st = commit_query(req, val)


@dp.callback_query_handler(lambda c: c.data == 'payment_registration', state=States.manager_mode) #todo payment_reg
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


@dp.callback_query_handler(lambda c: c.data == 'add_product', state=States.manager_mode)  # done
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


@dp.callback_query_handler(lambda c: c.data == 'add_sale', state=States.manager_mode)  # done
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


@dp.callback_query_handler(lambda c: c.data == 'show_product', state=States.manager_mode)  # done
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


@dp.callback_query_handler(lambda c: c.data == 'edit_product', state=States.manager_mode)  # done
async def edit_product(callback_query: types.CallbackQuery):
    await callback_query.answer("edit_product")
    state = dp.current_state(user=callback_query.from_user.id)
    kb = types.ReplyKeyboardMarkup(True, True)
    kb.row("назад")
    kb.row("★ ⬆️ В начало ⬆️ ★")
    await bot.send_message(callback_query.from_user.id, "введите с клавиатуры id продукта в боте", reply_markup=kb)
    await state.set_state(States.manager_mode_edit_product)


@dp.callback_query_handler(lambda c: c.data == 'add_manager', state=States.manager_mode)  # done
async def add_manager(callback_query: types.CallbackQuery):
    await callback_query.answer("add_manager")
    state = dp.current_state(user=callback_query.from_user.id)
    kb = types.ReplyKeyboardMarkup(True, True)
    kb.row("назад")
    kb.row("★ ⬆️ В начало ⬆️ ★")
    await bot.send_message(callback_query.from_user.id, "перешлите любое сообщение от нового менеджера",
                           reply_markup=kb)
    await state.set_state(States.manager_mode8)
