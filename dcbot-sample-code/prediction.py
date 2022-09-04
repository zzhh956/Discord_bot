from create_db import DB
from stocks_info import Daily_Stock_Information

class Prediction:
    #name of table
    table_name = "predictions"

    #name of column
    column_full_info = ["持有人 varchar(30)", "代號 varchar(10)", "公司 varchar(30)", "槓桿 INT", "預測價格 FLOAT", "預測日期 DATE"]
    column_name = ["持有人", "代號", "公司", "槓桿", "預測價格", "預測日期"]

    @classmethod
    def Create_Prediction_table(cls):
        connect = DB.connect_database()

        try:
            cursor = connect.cursor()

            sqlStatement = "USE %s;" %(DB.database_name['personal_info'])
            cursor.execute(sqlStatement)

            string = ', '.join(cls.column_full_info)
            sqlStatement = "CREATE TABLE IF NOT EXISTS " +  cls.table_name + " (%s);" %string
            # print(sqlStatement)
            cursor.execute(sqlStatement)

            print('predictions table is created successfully')

        except Exception as e:
            print(e)

        finally:
            cursor.close()
            connect.close()

    @classmethod
    def Insert_Prediction_table(cls, data):
        succeed = True
        connect = DB.connect_database()

        holder_name = data[0]
        id = data[1]
        predict_date = data[2]
        predict_price = data[3]
        leverage = data[4]
        succeed, firm = Daily_Stock_Information.Select_Single_Firm_From_Stocks_Info_table(id)

        try:
            cursor = connect.cursor()

            if succeed is False:
                raise ValueError('input the wrong stock id')

            sqlStatement = "USE %s;" %(DB.database_name['personal_info'])
            cursor.execute(sqlStatement)
   
            sqlStatement = """INSERT INTO %s VALUES ("%s", "%s", "%s", %s, %s, "%s")""" %(cls.table_name, holder_name, id
            , firm, leverage, predict_price, predict_date)
            # print(sqlStatement)
            cursor.execute(sqlStatement)
            connect.commit()

            print('predictions table is updated successfully')

        except Exception as e:
            print(e)
            succeed = False

        finally:
            cursor.close()
            connect.close()

        return succeed

    @classmethod
    def Show_Personal_Prediction(cls, name):
        succeed = True
        connect = DB.connect_database()

        data = []
        id = []
        firm = []
        leverage = []
        predict_price = []
        predict_date = []
        curr_price = []
        accuracy = []

        try:
            cursor = connect.cursor()

            sqlStatement = "USE %s;" %(DB.database_name['personal_info'])
            cursor.execute(sqlStatement)
   
            sqlStatement = """SELECT %s, %s, %s, %s, %s FROM %s WHERE `持有人` = "%s" ORDER BY `代號`;""" %("代號", "公司",
             "槓桿", "預測價格", "預測日期", cls.table_name,  str(name))
            # print(sqlStatement)
            cursor.execute(sqlStatement)

            for row in cursor.fetchall():
                id.append(row['代號'])
                firm.append(row['公司'])
                leverage.append(row['槓桿'])
                predict_price.append(row['預測價格'])
                predict_date.append(str(row['預測日期']))

            succeed, curr_price = Daily_Stock_Information.Select_Multiple_Price_From_Stocks_Info_table(id)

            if succeed is False:
                raise ValueError('User haven\'t predict yet')

            for predict, curr in zip(predict_price, curr_price):
                if curr:
                    accuracy.append('{0:.0f}%'.format(100 - (curr - predict) / predict * 100))
                else:
                    accuracy.append('0%')

            data = [id, firm, leverage, curr_price, predict_price, accuracy, predict_date]

            print('predictions table is fetched successfully')

        except Exception as e:
            print(e)
            succeed = False

        finally:
            cursor.close()
            connect.close()

        return succeed, data

    @classmethod
    def Drop_Prediction_table(cls):
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