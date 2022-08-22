import create_db
import random
import datetime

class Portfolio(create_db.DB):
    #name of table
    table_name = "stocks"

    #name of column
    column_full_info = ["代號 varchar(4)", "公司 varchar(10)", "持有人 varchar(10)", "`張數(股)` INT", "持有價格 FLOAT", "現在價格 FLOAT", "損益 FLOAT", "`損益(%)` varchar(20)", "持有日期 DATE"]
    column_name = ["代號", "公司", "持有人", "`張數(股)`", "持有價格", "現在價格", "損益", "`損益(%)`", "持有日期"]

    @classmethod
    def Create_Portfolio_table(cls):
        com = True
        connect = create_db.DB.connect_database()

        try:
            cursor = connect.cursor()

            sqlStatement = "USE %s;" %(create_db.DB.database_name)
            cursor.execute(sqlStatement)

            string = ', '.join(cls.column_full_info)
            sqlStatement = "CREATE TABLE IF NOT EXISTS " +  cls.table_name + " (%s);" %string
            # print(sqlStatement)
            cursor.execute(sqlStatement)

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
        connect = create_db.DB.connect_database()

        code = data[0]
        firm = data[1]
        holder_name = data[2]
        buy_date = data[3]
        shares = data[4]
        buy_price = data[5]
        curr_price = random.uniform(buy_price * 0.25, buy_price * 2)
        pnl = (curr_price - buy_price) * shares
        pnl_percentage = '{0:.0f}%'.format(pnl / (buy_price * shares) * 100) 
        
        try:
            cursor = connect.cursor()

            sqlStatement = "USE %s;" %(create_db.DB.database_name)
            cursor.execute(sqlStatement)
   
            sqlStatement = """INSERT INTO %s VALUES (%s, "%s", "%s", %s, %s, %s, %s, "%s", "%s")""" %(cls.table_name, code, firm, holder_name, shares, buy_price, curr_price
            , pnl, pnl_percentage, buy_date)
            sqlStatement += """ ON DUPLICATE KEY UPDATE %s=%s, %s="%s", %s="%s", %s=%s, %s=%s, %s=%s, %s=%s, %s="%s", %s="%s";""" %(cls.column_name[0], code, cls.column_name[1]
            , firm, cls.column_name[2], holder_name, cls.column_name[3], shares, cls.column_name[4], buy_price, cls.column_name[5], curr_price, cls.column_name[6], pnl
            , cls.column_name[7], pnl_percentage, cls.column_name[8], buy_date)
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
    def Select_Portfolio_table(cls, name):
        com = True
        data = []
        connect = create_db.DB.connect_database()
        
        try:
            cursor = connect.cursor()

            sqlStatement = "USE %s;" %(create_db.DB.database_name)
            cursor.execute(sqlStatement)
   
            sqlStatement = """SELECT * FROM %s WHERE `持有人` = "%s" ORDER BY `代號`;""" %(cls.table_name, str(name))
            # print(sqlStatement)
            cursor.execute(sqlStatement)
            data = cursor.fetchall()

            print('table is fetched successfully')

        except Exception as e:
            print(e)
            com = False

        finally:
            cursor.close()
            connect.close()

        return com, data

    @classmethod
    def Drop_Portfolio_table(cls):
        com = True
        connect = create_db.DB.connect_database()

        try:
            cursor = connect.cursor()

            sqlStatement = "USE %s;" %(create_db.DB.database_name)
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