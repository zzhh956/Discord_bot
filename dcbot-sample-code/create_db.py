import pymysql

class DB:
    server_name = 'SocialFi_discord'
    database_host = '127.0.0.2'
    database_user_name = 'root'
    database_password = ''
    database_server_IP = '127.0.0.1'
    database_port = 3306

    #name of database
    database_name = "portfolio"

    @classmethod
    def connect_database(cls):
        return pymysql.connect(host=cls.database_host, user=cls.database_user_name, password=cls.database_password,
                                port=cls.database_port, cursorclass=pymysql.cursors.DictCursor)

    @classmethod
    def create_database(cls):
        connect = cls.connect_database()

        try:
            cursor = connect.cursor()

            sqlStatement = "CREATE DATABASE IF NOT EXISTS " + cls.database_name
            cursor.execute(sqlStatement)

            print("database is created successfully!")

        except Exception as e:
            print(e)

        finally:
            cursor.close()
            connect.close()
        
        return