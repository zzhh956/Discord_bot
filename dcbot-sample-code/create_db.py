import random
import pymysql
import datetime

class DB:
    server_name = 'discord'
    database_host = '127.0.0.2'
    database_user_name = 'root'
    database_password = 'M06'
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

            # sqlQuery = "SHOW DATABASES"
            # cursor.execute(sqlQuery)
            # print(cursor.fetchall())
            # print('database creating succeed')
            print("database is created successfully!")

        except Exception as e:
            print(e)

        finally:
            cursor.close()
            connect.close()
        
        return

class Portfolio(DB):
    #name of table
    table_name = "stocks"

    #name of column
    column_full_info = ["代號 varchar(4)", "公司名稱 varchar(10)", "持有人 varchar(10)", "持有日期 DATE", "持有價格 FLOAT", "`持有量(股)` INT", "損益 FLOAT", "`損益(%)` varchar(20)", "現在日期 DATE", "現在價格 FLOAT"]
    column_name = ["代號", "公司名稱", "持有人", "持有日期", "持有價格", "`持有量(股)`", "損益", "`損益(%)`", "現在日期", "現在價格"]

    @classmethod
    def Create_Portfolio_table(cls):
        com = True
        connect = DB.connect_database()

        try:
            cursor = connect.cursor()

            sqlStatement = "USE %s;" %(DB.database_name)
            cursor.execute(sqlStatement)
            # print(sqlStatement)

            string = ', '.join(cls.column_full_info)
            # print(string)
            sqlStatement = "CREATE TABLE IF NOT EXISTS " +  cls.table_name + " (%s);" %string
            # print(sqlStatement)
            cursor.execute(sqlStatement)

            # sqlQuery = "SHOW TABLES"
            # cursor.execute(sqlQuery)
            # print(cursor.fetchall())
            print('table is created successfully')

        except Exception as e:
            print(e)
            com = False

        finally:
            cursor.close()
            connect.close()
        
        return com

    @classmethod
    def Insert_Portfolio_table(cls, data):
        com = True
        connect = DB.connect_database()

        code = data[0]
        firm = data[1]
        holder_name = data[2]
        buy_date = data[3]
        buy_price = data[4]
        shares = data[5]
        curr_date = datetime.date.today()
        curr_price = random.randint(200, 1000)
        pnl = (curr_price - buy_price) * shares
        pnl_percentage = '{0:.0f}%'.format(pnl / (buy_price * shares) * 100) 
        
        try:
            cursor = connect.cursor()

            sqlStatement = "USE %s;" %(DB.database_name)
            cursor.execute(sqlStatement)
   
            sqlStatement = """INSERT INTO %s VALUES (%s, "%s", "%s", "%s", %s, %s, %s, "%s", "%s", %s)""" %(cls.table_name, code, firm, holder_name, buy_date, buy_price, shares
            , pnl, pnl_percentage, curr_date, curr_price)
            sqlStatement += """ ON DUPLICATE KEY UPDATE %s=%s, %s="%s", %s="%s", %s="%s", %s=%s, %s=%s, %s=%s, %s="%s", %s="%s", %s=%s;""" %(cls.column_name[0], code, cls.column_name[1]
            , firm, cls.column_name[2], holder_name, cls.column_name[3], buy_date, cls.column_name[4], buy_price, cls.column_name[5], shares, cls.column_name[6], pnl
            , cls.column_name[7], pnl_percentage, cls.column_name[8], curr_date, cls.column_name[9], curr_price)
            # print(sqlStatement)
            cursor.execute(sqlStatement)
            connect.commit()

            print('table is updated successfully')

        except Exception as e:
            print(e)
            com = False

        finally:
            cursor.close()
            connect.close()

        return com

    @classmethod
    def Drop_Portfolio_table(cls):
        com = True
        connect = DB.connect_database()

        try:
            cursor = connect.cursor()

            sqlStatement = "USE %s;" %(DB.database_name)
            cursor.execute(sqlStatement)

            sqlStatement = "DROP TABLE %s;" %(cls.table_name)
            cursor.execute(sqlStatement) 
        
            print("table is dropped successfully")

        except Exception as e:
            print(e)
            com = False

        finally:
            cursor.close()
            connect.close()

        return com