from aiogram import Bot, types


button_phone = types.KeyboardButton(text="◦✶ ⬆️ Отправить номер телефона ⬆️ ✶◦", request_contact=True)
button_geo = types.KeyboardButton(text="◦✶ ⬆️ Отправить местоположение ⬆️ ✶◦", request_location=True)
button_prove = types.KeyboardButton(text="✅ Все верно ✅")
button_nope = types.KeyboardButton(text="🟥↩️ Не верно, вернуться назад ↩️🟥")

# общая рассылка? или напоминание о незаконченном заказе?
MAIL = types.ReplyKeyboardMarkup(True, True)
INIT_KEYBOARD = types.ReplyKeyboardMarkup(True, True)
TO_ME = types.ReplyKeyboardMarkup(True, True)
KEYBOARD2 = types.ReplyKeyboardMarkup(True, True)
KEYBOARD3 = types.ReplyKeyboardMarkup(True, True)
COST = types.ReplyKeyboardMarkup(True, True)
FLOWER_KEYS = types.ReplyKeyboardMarkup(True, True)
KEYBOARD6 = types.ReplyKeyboardMarkup(True, True)
TMP = types.ReplyKeyboardMarkup(True, True)
REP_KEY_WHEN_INLINE = types.ReplyKeyboardMarkup(True, True)
CART = types.ReplyKeyboardMarkup(True, True)

CART.row("корзина")
CART.row("☆ ↩️ Назад ↩️ ☆")

MAIL.row('общая рассылка', 'напоминание о незаконченном заказе')
# INIT_KEYBOARD.row('💐ХОЧУ ДОСТАВКУ БЕСПЛАТНО ЗА 40 МИНУТ🚚', '💐ХОЧУ ЗАКАЗАТЬ НА АДРЕС🚚')
INIT_KEYBOARD.row('/start','💐АКЦИИ💐')
INIT_KEYBOARD.row('💐НАЙТИ КОНКРЕТНЫЙ МАГАЗИН🔎')
INIT_KEYBOARD.row('очистить корзину','мои заказы')
INIT_KEYBOARD.row('стать магазином')
INIT_KEYBOARD.row('помощь')

TO_ME.add(button_geo)
TO_ME.row("☆ ↩️ Вернуться назад ↩️ ☆")

TMP.row("☆ ↩️ Вернуться назад ↩️ ☆")

KEYBOARD2 = types.reply_keyboard.ReplyKeyboardMarkup(True, True)
KEYBOARD2.row('/help')
KEYBOARD3.add(button_prove, button_nope)
KEYBOARD3.row('/start')


COST.row("до 1500р.", "до 2000р.")
COST.row("до 3000р.", "до 6000р.")
COST.row("☆ ↩️ Назад ↩️ ☆")

FLOWER_KEYS.row("Розы", "Гортензии", "Тюльпаны")
FLOWER_KEYS.row("Пионы", "Хризантемы", "Гвоздики")
FLOWER_KEYS.row("Орхидеи", "Альстромерии", "Лилии")
FLOWER_KEYS.row("Ранункулюсы", "Герберы", "Гипсофилы")
FLOWER_KEYS.row("корзины", "фрукты", "сладости")
FLOWER_KEYS.row("☆ ↩️ Назад ↩️ ☆")


KEYBOARD6.row("☆ ↩️ Назад ↩️ ☆", "★ ⬆️ В начало ⬆️ ★")

regex_dict = {"Розы": '[Рр]оз', "Гортензии": '[Гг]ортенз', "Тюльпаны": '[Тт]юльпан',
              "Пионы": '[Пп]ион', "Хризантемы": '[Хх]ризантем', "Гвоздики": '[Гг]воздик',
              "Орхидеи": '[Оо]рхиде', "Альстромерии": '[Аа]льстромер', "Лилии": '[Лл]ил',
              "Ранункулюсы": '[Рр]анункулюс', "Герберы": '[Гг]ербер', "Гипсофилы": '[Гг]ипсофил',
              "корзины": '[Кк]орзин', "фрукты": '[Фф]рукт', "сладости": '[Ссладост]', "ромашки": '[Рр]омашк'
              }


REP_KEY_WHEN_INLINE.row("🔥 корзина 💰", "★ ⬆️ В начало ⬆️ ★")
REP_KEY_WHEN_INLINE.row("мои заказы")
REP_KEY_WHEN_INLINE.row("☆ ↩️ Назад ↩️ ☆")



manager_mode_keys = types.InlineKeyboardMarkup()
bn1 = types.InlineKeyboardButton("добавить товар", callback_data='add_product')
bn2 = types.InlineKeyboardButton("посмотреть список товаров", callback_data='show_product')
bn3 = types.InlineKeyboardButton("редактировать товар", callback_data='edit_product')
bn4 = types.InlineKeyboardButton("добавить менеджера", callback_data='add_manager')
manager_mode_keys.add(bn1, bn3)
manager_mode_keys.add(bn2)
manager_mode_keys.add(bn4)




manager_mode_keys1 = types.InlineKeyboardMarkup()
bn1 = types.InlineKeyboardButton("добавить товар", callback_data='add_product')
bnn = types.InlineKeyboardButton("добавить акционный товар", callback_data='add_sale')
bn2 = types.InlineKeyboardButton("посмотреть список товаров", callback_data='show_product')
bn3 = types.InlineKeyboardButton("редактировать товар", callback_data='edit_product')
bn4 = types.InlineKeyboardButton("добавить менеджера", callback_data='add_manager')
bn5 = types.InlineKeyboardButton("скрыть", callback_data='visual_ability')
manager_mode_keys1.add(bn1, bn3)
manager_mode_keys1.add(bnn, bn2)
manager_mode_keys1.add(bn4)
manager_mode_keys1.add(bn5)


manager_mode_keys2 = types.InlineKeyboardMarkup()
bn11 = types.InlineKeyboardButton("добавить товар", callback_data='add_product')
bn21 = types.InlineKeyboardButton("посмотреть список товаров", callback_data='show_product')
bn31 = types.InlineKeyboardButton("редактировать товар", callback_data='edit_product')
bn41 = types.InlineKeyboardButton("добавить менеджера", callback_data='add_manager')
bn51 = types.InlineKeyboardButton("показать", callback_data='visual_ability')
manager_mode_keys2.add(bn11, bn31)
manager_mode_keys2.add(bnn, bn21)
manager_mode_keys2.add(bn41)
manager_mode_keys2.add(bn51)



manager_mode_edit_keys = types.InlineKeyboardMarkup()
bnn1 = types.InlineKeyboardButton("описание", callback_data='edit_caption')
bnn2 = types.InlineKeyboardButton("категории", callback_data='edit_categories')
bnn3 = types.InlineKeyboardButton("цену", callback_data='edit_cost')
bnn5 = types.InlineKeyboardButton("предыдущий", callback_data='edit_prev')
bnn6 = types.InlineKeyboardButton("след.", callback_data='edit_next')
bnn4 = types.InlineKeyboardButton("удалить товар", callback_data='delete_product')

manager_mode_edit_keys.add(bnn1, bnn3)
manager_mode_edit_keys.add(bnn2)
manager_mode_edit_keys.add(bnn5, bnn6)
manager_mode_edit_keys.add(bnn4)


tink_reg_keys = types.ReplyKeyboardMarkup(True, True)
tink_reg_keys.row("★ ⬆️ В начало ⬆️ ★")
tink_reg_keys.row("назад")