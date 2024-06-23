import sqlite3


def inita_test_db ():
    conn = sqlite3.connect('sqlite_test.db')
    c = conn.cursor()

    c.execute('''
    CREATE TABLE IF NOT EXISTS tests (
              test_name TEXT,
              test_summoner TEXT,
    )
    ''')

    conn.commit()
    conn.close()