import datetime
from create_db import DB
from stocks_info import Daily_Stock_Information
from prediction import Prediction

class Leaderboard:
    #name of table
    table_name = "leaderboard"

    #name of column
    column_full_info = ["名稱 varchar(30) PRIMARY KEY", "代幣 BIGINT"]
    column_name = ["名稱", "代幣"]

    @classmethod
    def Create_Leaderboard_table(cls):
        connect = DB.connect_database()

        try:
            cursor = connect.cursor()

            sqlStatement = "USE %s;" %(DB.database_name['personal_info'])
            cursor.execute(sqlStatement)

            string = ', '.join(cls.column_full_info)
            sqlStatement = "CREATE TABLE IF NOT EXISTS " +  cls.table_name + " (%s);" %string
            # print(sqlStatement)
            cursor.execute(sqlStatement)

            print('leaderboard table is created successfully')

        except Exception as e:
            print(e)
            succeed = False

        finally:
            cursor.close()
            connect.close()

    @classmethod
    def Insert_Leaderboard_table(cls, data):
        succeed = True
        connect = DB.connect_database()
        data1 = []

        for i, j in zip(data[0], data[1]):
            data1.append((i, j, j))

        try:
            cursor = connect.cursor()

            sqlStatement = "USE %s;" %(DB.database_name['personal_info'])
            cursor.execute(sqlStatement)
   
            sqlStatement = """INSERT INTO leaderboard VALUES ("%s", %s)"""
            sqlStatement += """ ON DUPLICATE KEY UPDATE `代幣` = `代幣` + (%s);"""
            # print(sqlStatement)
            cursor.executemany(sqlStatement, data1)
            connect.commit()

            sqlStatement = """UPDATE leaderboard SET `名稱` = replace(`名稱`, "'", '');"""
            cursor.execute(sqlStatement)
            connect.commit()

            print('leaderboard table is updated successfully')

        except Exception as e:
            print(e)
            succeed = False

        finally:
            cursor.close()
            connect.close()

        return succeed

    @classmethod
    def Calculate_All_Prediction_PnL(cls):
        succeed = True
        connect = DB.connect_database()
        date = datetime.date.today()

        data = []
        id = []
        name = []
        leverage = []
        predict_price = []
        curr_price = []
        points = []

        try:
            cursor = connect.cursor()

            sqlStatement = "USE %s;" %(DB.database_name['personal_info'])
            cursor.execute(sqlStatement)

            sqlStatement = """SELECT %s, %s, %s, %s FROM predictions WHERE `預測日期` = "%s" ORDER BY `持有人`;""" %("持有人", "代號"
            , "預測價格", "槓桿", date)
            # print(sqlStatement)
            cursor.execute(sqlStatement)

            for row in cursor.fetchall():
                name.append(row['持有人'])
                id.append(row['代號'])
                predict_price.append(row['預測價格'])
                leverage.append(row['槓桿'])
            
            succeed, curr_price = Daily_Stock_Information.Select_Multiple_Price_From_Stocks_Info_table(id)

            if succeed is False:
                raise ValueError('can\'t get the current price for calculating PnL')

            for predict, curr, lev in zip(predict_price, curr_price, leverage):
                if abs((curr - predict) / predict) > 0.001:
                    points.append(1 / ((curr - predict) / predict) * lev)
                elif abs((curr - predict) / predict) <= 0.001:
                    points.append(1000 * lev)

            data = [name, points]

            print("personal PnL is calculated successfully")

        except Exception as e:
            print(e)
            succeed = False

        finally:
            cursor.close()
            connect.close()

        return succeed, data

    @classmethod
    def Show_Leaderboard(cls):
        succeed = True
        connect = DB.connect_database()

        data = []
        name = []
        points = []

        try:
            cursor = connect.cursor()

            sqlStatement = "USE %s;" %(DB.database_name['personal_info'])
            cursor.execute(sqlStatement)
   
            sqlStatement = """SELECT %s, %s FROM %s ORDER BY `代幣`;""" %("名稱", "代幣", cls.table_name)
            # print(sqlStatement)
            cursor.execute(sqlStatement)

            for row in cursor.fetchall():
                name.append(row['名稱'])
                points.append(row['代幣'])

            data = [name, points]

            print('leaderboard table is fetched successfully')

        except Exception as e:
            print(e)
            succeed = False

        finally:
            cursor.close()
            connect.close()

        return succeed, data

    @classmethod
    def Drop_Leaderboard_table(cls):
        succeed = True
        connect = DB.connect_database()

        try:
            cursor = connect.cursor()

            sqlStatement = "USE %s;" %(DB.database_name['personal_info'])
            cursor.execute(sqlStatement)

            sqlStatement = "DROP TABLE %s;" %(cls.table_name)
            cursor.execute(sqlStatement) 
        
            print("predictions table is dropped successfully")

        except Exception as e:
            print(e)
            succeed = False

        finally:
            cursor.close()
            connect.close()

        return succeed