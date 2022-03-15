import mysql.connector


conf = {'user': 'root',
        'password': '0000',
        'host': '127.0.0.1',
        'database': 'flobot'}


def commit_query(sqlin: str, value: tuple):

    cnx = mysql.connector.connect(user='root', password='0000',
                                      host='127.0.0.1',
                                      database='flobot')

    cursor = cnx.cursor()
    print(cursor.execute(sqlin, value))
    cnx.commit()

    cnx.close()


def get_query(sqlin: str, value: tuple):

    cnx = mysql.connector.connect(user='root', password='0000',
                                  host='127.0.0.1',
                                  database='flobot')

    cursor = cnx.cursor()
    cursor.execute(sqlin, value)
    row = cursor.fetchone()
    cnx.close()
    return row[0]


def get_query_all(sqlin: str, value: tuple):

    cnx = mysql.connector.connect(user='root', password='0000',
                                  host='127.0.0.1',
                                  database='flobot')

    cursor = cnx.cursor()
    cursor.execute(sqlin, value)
    row = cursor.fetchone()
    cnx.close()
    return row


def connect():
    return mysql.connector.connect(user='root', password='0000',
                                  host='127.0.0.1',
                                  database='flobot')