from dbcm import *


shit = [
    {'file_id': 'AgACAgIAAxkBAAEBxf1hKThj955s36eyqRy_3x7ZRl5nCgAC7LMxG_RnUUkusMKtQPdKLQEAAwIAA3gAAyAE', 'caption': 'Букет из 15 красных роз Ред Наоми \n60 см', 'categ': 'Розы', 'cost': 1050},
    {'file_id': 'AgACAgIAAxkBAAEBxf1hKThj955s36eyqRy_3x7ZRl5nCgAC7LMxG_RnUUkusMKtQPdKLQEAAwIAA3gAAyAE', 'caption': 'Букет из 15 красных роз Ред Наоми \n60 см', 'categ': 'Розы', 'cost': 1050},
{'file_id': 'AgACAgIAAxkBAAEBxRZhKRg2HrjmaLeiIyREIyGrOdif1QACg7MxG_RnUUmVdIlePj67PQEAAwIAA3gAAyAE', 'caption': 'Букет из 25 нежно-белых роз', 'categ': 'Розы', 'cost': 1800},
{'file_id': 'AgACAgIAAxkBAAEBxSFhKRidp_joNDp23jaLg7_u9AOF8AAChLMxG_RnUUlG5BH4czWwywEAAwIAA3gAAyAE', 'caption': '19 штук красных роз\n50 см', 'categ': '1550', 'cost': 1000},
{'file_id': 'AgACAgIAAxkBAAEBxSxhKRkAAQnXZ4Y1rrCJtjqeu2p-_h0AAoWzMRv0Z1FJXN62JiUEN4QBAAMCAAN4AAMgBA', 'caption': '19 штук красных роз\n50 см', 'categ': 'Розы', 'cost': 1550},
{'file_id': 'AgACAgIAAxkBAAEBxTdhKRlet_zzfmmH1aNZdns7J_S_lQAChrMxG_RnUUnHxIeg2RJA5gEAAwIAA3gAAyAE', 'caption': 'Потрясающий букет из 21 нежной розы', 'categ': 'Розы', 'cost': 1750},
{'file_id': 'AgACAgIAAxkBAAEBxUJhKRnJzDLwf54zD6AucBTUg_rx8QACiLMxG_RnUUmEFC62TbAUOwEAAwIAA3gAAyAE', 'caption': '21 белая роза 60 см', 'categ': 'Розы', 'cost': 1800},
{'file_id': 'AgACAgIAAxkBAAEBxU1hKRo_XaoSzl9OeH5p6fzL7mtrPQACibMxG_RnUUk9kpeGoquwMgEAAwIAA3gAAyAE', 'caption': 'Букет из розовых кустовых роз', 'categ': 'Розы', 'cost': 2100},
{'file_id': 'AgACAgIAAxkBAAEBxVhhKRsItuCaNqmvP0Xa7sqHHVDlCgACjbMxG_RnUUlwGvmo4zn8YwEAAwIAA3gAAyAE', 'caption': 'Букет из белых кустовых роз 50 см', 'categ': 'Розы', 'cost': 1750},
{'file_id': 'AgACAgIAAxkBAAEBxWNhKRtAVSCgyoTfScT1JyKSuE6hVQACjrMxG_RnUUnejHtojN5lEQEAAwIAA3gAAyAE', 'caption': 'Букет из кустовых роз и статицы', 'categ': 'Розы', 'cost': 1600},
{'file_id': 'AgACAgIAAxkBAAEBxW5hKR1ONK8fnyoEutAuXjR9LHGBMQAClLMxG_RnUUmjIEfByIOptAEAAwIAA3gAAyAE', 'caption': 'Букет из 19 розовых роз', 'categ': 'Розы', 'cost': 1549},
{'file_id': 'AgACAgIAAxkBAAEBxXlhKR2nlpZwnLHbtXsbLtSm8_k1tAAClbMxG_RnUUmVRoMxX2V8VgEAAwIAA3gAAyAE', 'caption': 'Букет «Коралловый риф»\nИз 9 нежных роз', 'categ': 'Розы', 'cost': 1599},
{'file_id': 'AgACAgIAAxkBAAEBxYRhKR4JDYi9_7hE8e8TWpua_0Q6RgAClrMxG_RnUUkuh7o_XmSWaQEAAwIAA3gAAyAE', 'caption': '35 красных роз 40-50 см', 'categ': 'Розы', 'cost': 2100},
{'file_id': 'AgACAgIAAxkBAAEBxY9hKR6-j753-Go3EMPWmpD_kFTEtgACobMxG_RnUUmaLZJpRCxHPQEAAwIAA3gAAyAE', 'caption': '51 красная Роза 40-50 см', 'categ': 'Розы', 'cost': 2900},
{'file_id': 'AgACAgIAAxkBAAEBxZphKR9OtDTNyqXA58ZccBjqU0S4dQACorMxG_RnUUn9xmi1SR0bQgEAAwIAA3gAAyAE', 'caption': 'Букет из 25 роз 40 см\nБелые и розовые', 'categ': 'Розы', 'cost': 1599},
{'file_id': 'AgACAgIAAxkBAAEBxaVhKR-1cmI-nIah3AsriYxg9jet0AACo7MxG_RnUUnCQN6EI3FuaAEAAwIAA3gAAyAE', 'caption': 'Букет из 29 роз аква \n40-50 см', 'categ': 'Розы', 'cost': 2200},
{'file_id': 'AgACAgIAAxkBAAEBxbBhKSAYkm6o-QQQiJeNbSfbkx2m4QACpbMxG_RnUUlX6Xp9Z_nA7gEAAwIAA3gAAyAE', 'caption': 'Букет из 19 красных роз 50 см', 'categ': 'Розы', 'cost': 1499},
{'file_id': 'AgACAgIAAxkBAAEBxbthKTYpSg_nDlpwbgEuRnHjRSBS4wAC47MxG_RnUUlokShYUPcoggEAAwIAA3gAAyAE', 'caption': 'Букет из 11 красных роз 50 см', 'categ': 'Розы', 'cost': 880},
{'file_id': 'AgACAgIAAxkBAAEBxcZhKTZ58D4vBSFGPSGh8BzAz9F6kwAC5LMxG_RnUUmLkFtd5xmrGAEAAwIAA3gAAyAE', 'caption': 'Букет из 9 роз Джулия \n50 см', 'categ': 'Розы', 'cost': 650},
{'file_id': 'AgACAgIAAxkBAAEBxdFhKTbjEfN-kic9xbq7j3g1VkpXzgAC5rMxG_RnUUm2oTKhgeQYmwEAAwIAA3gAAyAE', 'caption': 'Букет из 15 красных роз\n40 см', 'categ': 'Розы', 'cost': 990},
{'file_id': 'AgACAgIAAxkBAAEBxdxhKTcnxEhfhupF9O6e7s3okLAT9AAC6bMxG_RnUUmwq--21pu39AEAAwIAA3gAAyAE', 'caption': 'Букет из 15 нежных роз\nРозового цвета\n40 см', 'categ': 'Розы', 'cost': 1100},
{'file_id': 'AgACAgIAAxkBAAEBxedhKTePbekGm8bZmVXxG2dLJGfPRgAC6rMxG_RnUUlo4-mKqANfRAEAAwIAA3gAAyAE', 'caption': '11 белых роз 40 см', 'categ': 'Розы', 'cost': 900},
{'file_id': 'AgACAgIAAxkBAAEBxfJhKTfenkbGlPAUSLsyM6dA1_WEuQAC67MxG_RnUUkFa38QnVKG6AEAAwIAA3gAAyAE', 'caption': 'Букет «Тёплый вечер» из 11 роз 40-50 см', 'categ': 'Розы', 'cost': 899}


]

def inserting():
    cnx = mysql.connector.connect(user='root', password='0000',
                                  host='127.0.0.1',
                                  database='testflobot')

    cursor = cnx.cursor()
    sql = """ select * from testflobot.shops; """
    cursor.execute(sql)
    all_shops = cursor.fetchall()
    print(all_shops)
    cnx.close()
    # cnx = mysql.connector.connect(user='root', password='0000',
    #                               host='127.0.0.1',
    #                               database='flobot')
    #
    #
    # test_curs = cnx.cursor()


    shop_code = 0

    for shop in all_shops:

        sql = ("select tink_shop_code from flobot.shops where shop_id = '%s';")
        value = (shop[0],)
        cnx = mysql.connector.connect(user='root', password='0000',
                                      host='127.0.0.1',
                                      database='testflobot')
        cursor = cnx.cursor()
        cursor.execute(sql, value)
        row = cursor.fetchone()
        if row is None:
            continue
        shop_code = row[0]
        cnx.close()

        sql = "update testflobot.shops set tink_shop_code = {} where shop_id = {} ;".format(shop_code, shop[0])

        cnx = mysql.connector.connect(user='root', password='0000',
                                      host='127.0.0.1',
                                      database='testflobot')
        try:
            cursor = cnx.cursor()
            cursor.execute(sql)
            cnx.commit()
            cnx.close()
        except:
            print("none")
    # cnx.commit()



def default_buckets():
    cnx = connect()
    cursor = cnx.cursor()

    cursor.execute("select photo_id, caption, categ, cost from default_buckets where id > ;")

    flowers = cursor.fetchall()

    for fow in flowers:
        print(fow)
        commit_query("insert into products(file_id, caption, categories, cost, default_bucket) values(%s, %s, %s, %s, true);", (fow[0], fow[1], fow[2], fow[3]))
        print("udacha")



