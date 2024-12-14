import sqlite3
from sqlite3 import Error

def create_connect(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as error:
        print(error)
        
    return conn 

def execute_query(conn, query):
    linhas = []
    try:
        cursor = conn.cursor()
        cursor.execute(query)
        linhas = cursor.fetchall()
        cursor.close()
    except Error as error:
        print(error)
        
    return linhas

def execute_insert(conn, query):
    linhas = 0
    try:
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()
        linhas = cursor.rowcount
        cursor.close()
    except Error as error:
        print(error)
        
    return linhas