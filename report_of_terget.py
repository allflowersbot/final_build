import asyncio
import dbcm
from aiogram import Bot, types
from aiogram.utils import executor
from aiogram.dispatcher import Dispatcher
from config import BOT_TOKEN
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from dbcm import commit_query, get_query, connect, get_query_all
import mysql.connector
loop = asyncio.get_event_loop()
bot = Bot(token=BOT_TOKEN)
# TEST_
dp = Dispatcher(bot=bot, loop=loop, storage=MemoryStorage())


async def foo():

    await bot.send_message(392875761, "hello there general kenobi, here's your report")



def collect_data():
    file = open('report_config', 'r')
    str = file.read()
    print(str)
    client = str.find(' = ')
    cl_id = str[client + 3:]
    print(cl_id)
    sql = " select * from clients where client_id >  {} ; ".format(cl_id)
    cnx = mysql.connector.connect(user='root', password='0000',
                                  host='127.0.0.1',
                                  database='flobot')

    cursor = cnx.cursor()
    cursor.execute(sql)
    row = cursor.fetchall()
    for it in row:
        print(it)
    cnx.close()


collect_data()
loop.run_until_complete(foo())
loop.close()
