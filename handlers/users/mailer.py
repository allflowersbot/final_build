from loader import dp, bot, auctions, ADMIN_CHAT_ID, array
from keyboards import MAIL, INIT_KEYBOARD
from video_instruction import mailing
from utils import States
from aiogram import types
from dbcm import connect


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
