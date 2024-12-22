import mysql.connector
from mysql.connector import Error

def create_connect(host, user, password, database):
    try:
        conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        if conn.is_connected():
            print("Connection successful!")
            return conn
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        return None


def execute_query(conn, query):
    linhas = []
    try:
        cursor = conn.cursor()
        cursor.execute(query)
        linhas = cursor.fetchall()
        cursor.close()
    except mysql.connector.Error as error:
        print(f"Erro ao executar a consulta: {error}")
        
    return linhas


def execute_insert(conn, query):
    linhas = 0
    try:
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()
        linhas = cursor.rowcount
        cursor.close()
    except mysql.connector.Error as error:
        print(f"Erro ao executar a operação: {error}")
        
    return linhas

