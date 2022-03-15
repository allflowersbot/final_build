import logging
import asyncio

import typing
from aiogram.dispatcher import Dispatcher
from aiogram import Bot, types
from config import TEST_BOT_TOKEN, APP_ID, APP_SECRET, REDIRECT_URL, BOT_TOKEN
from instagram_basic_display.InstagramBasicDisplay import InstagramBasicDisplay
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from order_product import order

array = []
current_products = []
auctions = []
list_of_orders: typing.List[order]
list_of_orders = []

list_of_confirmed_orders: typing.List[order]
list_of_confirmed_orders = []



ADMIN_CHAT_ID = 392875761
logging.basicConfig(format=u'%(filename)+13s [ LINE:%(lineno)-4s] %(levelname)-8s [%(asctime)s] %(message)s',
                    level=logging.INFO)
loop = asyncio.get_event_loop()
ID = ""
ID2 = ""
bot = Bot(token=BOT_TOKEN)
# TEST_
dp = Dispatcher(bot=bot, loop=loop, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())

instagram_basic_display = InstagramBasicDisplay(app_id=APP_ID,
                                                app_secret=APP_SECRET,
                                                redirect_url=REDIRECT_URL)
