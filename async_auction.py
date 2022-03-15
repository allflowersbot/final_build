import asyncio

from aiogram import types

from loader import auctions, dp, bot, list_of_orders, list_of_confirmed_orders
from utils import States
from dbcm import *
auctin_order = {
    "client_id": 0,
    "product_id": [],
    "shop_ids": [],
    "curr_shop": 0,
    "curr_manager": 0,
    "curr_cost": 0,
    "first_cost": 0,
    "offer": "",
    "managers": [],
    "delivery_cost": 0,
    "photos": []
}



async def auction(order_id):
    await asyncio.sleep(60)
    print("async auction(order_id= {})".format(order_id))
    for ordr in list_of_orders:
        if ordr.get_order_id() == order_id:
            state = dp.current_state(user=ordr.get_curr_manager(), chat=ordr.get_curr_manager())
            ordr.update_curr_shop()
            offer, array_of_images = ordr.make_offer()
            mngr = ordr.get_curr_manager()

            if len(array_of_images) > 1:
                media = types.MediaGroup()
                for file_id in array_of_images:
                    media.attach_photo(file_id, "букет")
                await bot.send_media_group(mngr, media)
            else:
                await bot.send_photo(mngr, array_of_images[0], offer)  #
            await bot.send_message(mngr, "вы выйграли аукцион, укажите стоимость доставки до {}".format(ordr.delivery_addr))
            print(mngr, "вы выйграли аукцион, укажите стоимость доставки до {}".format(ordr.delivery_addr))
            await state.set_state(States.auctions1)





async def payment_cooldown(provider_order_id):
    await asyncio.sleep(3600)
    print("async def payment_cooldown pr_id = {}".format(provider_order_id))
    for order in list_of_confirmed_orders:
        if order.payment_order_id == provider_order_id:
            if order.pay:
                print("{} status=true".format(provider_order_id))
            else:
                list_of_confirmed_orders.remove(order)
                print("{} status=false".format(provider_order_id))