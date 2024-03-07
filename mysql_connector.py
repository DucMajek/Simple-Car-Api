import mysql.connector


class MySQLConnector:
    def __init__(self):
        self.mydb = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            port='3306',
            database='car_api'
        )

