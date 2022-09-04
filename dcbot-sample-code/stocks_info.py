import requests
import pandas as pd
from io import StringIO
import datetime
from create_db import DB

class Daily_Stock_Information:
    #name of table
    table_name = "stocks"

    #name of column
    column_full_info = ["代號 varchar(10) PRIMARY KEY", "公司 varchar(30)", "現在價格 Float", "日期 DATE"]
    column_name = ["代號", "公司", "現在價格", "日期"]

    @classmethod
    def Create_Stock_Info_table(cls):
        connect = DB.connect_database()

        try:
            cursor = connect.cursor()

            sqlStatement = "USE %s;" %(DB.database_name['stocks'])
            cursor.execute(sqlStatement)

            string = ', '.join(cls.column_full_info)
            sqlStatement = "CREATE TABLE IF NOT EXISTS " +  cls.table_name + " (%s);" %string
            # print(sqlStatement)
            cursor.execute(sqlStatement)

            print('stocks info table is created successfully')

        except Exception as e:
            print(e)

        finally:
            cursor.close()
            connect.close()

    @classmethod
    def Update_Stock_Info_table(cls):
        succeed = True
        data = []
        connect = DB.connect_database()

        try:
            cursor = connect.cursor()

            sqlStatement = "USE %s;" %(DB.database_name['stocks'])
            cursor.execute(sqlStatement)
            
            # check whether table has the newest data
            sqlStatement = "SELECT 日期 FROM " + cls.table_name + " WHERE `代號` = 0050;"
            cursor.execute(sqlStatement)
            date = cursor.fetchall()

            # if we don't have the newest data, then we crawl again
            if date != datetime.date.today():
                date = datetime.date.today()
                data = cls.crawl_price(date)

                sqlStatement = """INSERT IGNORE INTO stocks (`代號`, `公司`, `現在價格`, `日期`) VALUES (%s, "%s", %s, %s)""" 
                sqlStatement += """ ON DUPLICATE KEY UPDATE `現在價格` = (%s), `日期` = (%s);"""
                # df['代號'], df['公司'], df['現在價格'], df['日期']
                cursor.executemany(sqlStatement, data)
                connect.commit()
                sqlStatement = """UPDATE stocks SET `公司` = replace(`公司`, "'", '');"""
                cursor.execute(sqlStatement)
                connect.commit()

            print('stocks info table is updated successfully')

        except Exception as e:
            print(e)
            succeed = False

        finally:
            cursor.close()
            connect.close()

        return succeed

    @classmethod
    def crawl_price(cls, date):
        # 將 date 變成字串 舉例：'20180525'
        datestr = date.strftime('%Y%m%d')

        # 從網站上依照 datestr 將指定日期的股價抓下來
        r = requests.post('http://www.twse.com.tw/exchangeReport/MI_INDEX?response=csv&date=' + datestr + '&type=ALLBUT0999')

        # 將抓下來的資料（r.text），其中的等號給刪除
        content = r.text.replace('=', '')

        # 將 column 數量小於等於 10 的行數都刪除
        lines = content.split('\n')
        lines = list(filter(lambda l:len(l.split('",')) > 10, lines))

        # 將每一行再合成同一行，並用肉眼看不到的換行符號'\n'分開
        content = "\n".join(lines)

        # 假如沒下載到，則回傳None（代表抓不到資料）
        if content == '':
            return

        # 將content變成檔案：StringIO，並且用pd.read_csv將表格讀取進來
        df = pd.read_csv(StringIO(content))

        # 將表格中的元素都換成字串，並把其中的逗號刪除
        df = df.astype(str)
        df = df.apply(lambda s: s.str.replace(',', ''))

        # 將爬取的日期存入 dataframe
        df['日期'] = pd.to_datetime(date)

        # 將欄位改名
        df = df.rename(columns = {'證券代號':'代號'})
        df = df.rename(columns = {'證券名稱':'公司'})
        df = df.rename(columns = {'收盤價':'現在價格'})
        
        data = []
        for i, j, k, l in zip(df['代號'].tolist(), df['公司'].tolist(), df['現在價格'].tolist(), df['日期'].tolist()):
            data.append((i, j, k, l, k, l))

        # 將 「stock_id」與「date」設定成index 
        # df = df.set_index(['stock_id', 'date'])

        # 將所有的表格元素都轉換成數字，error='coerce'的意思是說，假如無法轉成數字，則用 NaN 取代
        # df = df.apply(lambda s:pd.to_numeric(s, errors='coerce'))

        # 刪除不必要的欄位
        # df = df[df.columns[df.isnull().all() == False]]

        return data

    @classmethod
    def Select_Single_Firm_From_Stocks_Info_table(cls, id):
        connect = DB.connect_database()
        succeed = True
        firm = []
        
        try:
            cursor = connect.cursor()

            sqlStatement = "USE %s;" %(DB.database_name['stocks'])
            cursor.execute(sqlStatement)
            sqlStatement = """SELECT `公司` FROM stocks WHERE `代號` = "%s";""" %(str(id))
            # print(sqlStatement)
            cursor.execute(sqlStatement)

            for item in cursor.fetchall():
                firm = item['公司']

            if firm == []:
                raise ValueError('input the wrong stock id')

            print('stocks_info table is fetched successfully')

        except Exception as e:
            print(e)
            succeed = False

        finally:
            cursor.close()
            connect.close()

        return succeed, firm
    
    @classmethod
    def Select_Single_Price_From_Stocks_Info_table(cls, id):
        connect = DB.connect_database()
        succeed = True
        price = -1
        
        try:
            cursor = connect.cursor()

            sqlStatement = "USE %s;" %(DB.database_name['stocks'])
            cursor.execute(sqlStatement)

            sqlStatement = """SELECT `現在價格` FROM stocks WHERE `代號` = "%s";""" %(str(id))
            # print(sqlStatement)
            cursor.execute(sqlStatement)

            for row in cursor.fetchall():
                price = row['現在價格']

            if price == -1:
                raise ValueError("didn't fetch right data from stocks_info table")

            print('stocks_info table is fetched successfully')

        except Exception as e:
            print(e)
            succeed = False

        finally:
            cursor.close()
            connect.close()

        return succeed, price

    @classmethod
    def Select_Multiple_Price_From_Stocks_Info_table(cls, ids):
        connect = DB.connect_database()
        succeed = True
        price = []
        
        try:
            cursor = connect.cursor()

            sqlStatement = "USE %s;" %(DB.database_name['stocks'])
            cursor.execute(sqlStatement)

            for id in ids:
                sqlStatement = """SELECT `現在價格` FROM stocks WHERE `代號` = "%s";""" %(str(id))
                # print(sqlStatement)
                cursor.execute(sqlStatement)

                for row in cursor.fetchall():
                    price.append(row['現在價格'])

            if price == []:
                raise ValueError("didn't fetch right data from stocks_info table")

            print('stocks_info table is fetched successfully')

        except Exception as e:
            print(e)
            succeed = False

        finally:
            cursor.close()
            connect.close()

        return succeed, price

    @classmethod
    def Drop_Stocks_Info_table(cls):
        succeed = True
        connect = DB.connect_database()

        try:
            cursor = connect.cursor()

            sqlStatement = "USE %s;" %(DB.database_name['stocks'])
            cursor.execute(sqlStatement)

            sqlStatement = "DROP TABLE %s;" %(cls.table_name)
            cursor.execute(sqlStatement) 
        
            print("stocks_info table is dropped successfully")

        except Exception as e:
            print(e)
            succeed = False

        finally:
            cursor.close()
            connect.close()

        return succeed

d = Daily_Stock_Information()
# d.Create_Stock_Info_table()
# d.crawl_price(datetime.datetime(2022,8,29))
d.Update_Stock_Info_table()