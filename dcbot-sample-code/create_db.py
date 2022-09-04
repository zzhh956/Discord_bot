import pymysql

class DB:
    server_name = ''
    server_host = '127.0.0.2'
    server_user_name = 'root'
    server_password = ''
    server_IP = '127.0.0.1'
    server_port = 3306

    #name of database
    database_name = {'personal_info': "personal_info", 'stocks': "stocks_info"}

    @classmethod
    def connect_database(cls):
        return pymysql.connect(host=cls.server_host, user=cls.server_user_name, password=cls.server_password,
                                port=cls.server_port, cursorclass=pymysql.cursors.DictCursor)

    @classmethod
    def create_database(cls):
        connect = cls.connect_database()

        try:
            cursor = connect.cursor()

            for key, name in cls.database_name.items():
                sqlStatement = "CREATE DATABASE IF NOT EXISTS " + name
                cursor.execute(sqlStatement)

            print("database is created successfully!")

        except Exception as e:
            print(e)

        finally:
            cursor.close()
            connect.close()
        
        return