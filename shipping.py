from aiogram import Bot, types
from aiogram.utils import executor
from aiogram.dispatcher import Dispatcher
from aiogram.types.message import ContentType


PRICES = [
    types.LabeledPrice(label='Настоящая Машина Времени', amount=4200000),
    types.LabeledPrice(label='Подарочная упаковка', amount=30000)
]

#setup shipping_

TELEPORTER_SHIPPING_OPTION = types.ShippingOption(
    id='teleporter',
    title='Всемирный* телепорт'
).add(types.LabeledPrice('Телепорт', 1000000))

RUSSIAN_POST_SHIPPING_OPTION = types.ShippingOption(
    id='ru_post', title='Почтой России')
RUSSIAN_POST_SHIPPING_OPTION.add(
    types.LabeledPrice(
        'Деревянный ящик с амортизирующей подвеской внутри', 100000)
)
RUSSIAN_POST_SHIPPING_OPTION.add(
    types.LabeledPrice('Срочное отправление (5-10 дней)', 500000)
)

PICKUP_SHIPPING_OPTION = types.ShippingOption(id='pickup', title='Самовывоз')
PICKUP_SHIPPING_OPTION.add(types.LabeledPrice('Самовывоз в Москве', 50000))
