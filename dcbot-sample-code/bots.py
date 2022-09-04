from calendar import leapdays
from ctypes import alignment
import datetime
from sqlite3 import Timestamp
import discord as dc
import discord.ext.commands as cmds
from create_db import DB
from prediction import Prediction
from leaderboard import Leaderboard
from stocks_info import Daily_Stock_Information
from table2ascii import table2ascii as t2a, PresetStyle, Alignment

channel_id = 111     # Change it
token = '.GsPIPX.'    # Change it
cmd_prefix = '$'            # Change it
bot = cmds.Bot(command_prefix = cmd_prefix, intents = dc.Intents.all())  

@bot.event
async def on_ready():
    await bot.wait_until_ready()
    print('>> Bot is on ready <<')
    c = bot.get_channel(channel_id)

    DB.create_database()
    Prediction.Create_Prediction_table()
    Leaderboard.Create_Leaderboard_table()
    Daily_Stock_Information.Create_Stock_Info_table()
    Daily_Stock_Information.Update_Stock_Info_table()

    await c.send('>> 您的股價預測小幫手已上線 <<')
    print('listening to commands...')

@bot.command()
async def hi(ctx: cmds.Context):
    await ctx.send('您好')    # change it

@bot.command()
async def predict(ctx: cmds.context, stock_id, date: str, predict_price: int, leverage: int):
    holder_name = ctx.message.author.name
    data = [holder_name, stock_id, date, predict_price, leverage]

    if Prediction.Insert_Prediction_table(data):
        await ctx.send('已更新表格')
    else:
        await ctx.send('資料格式輸入有誤')

    print('listening to commands...')

@bot.command()
async def show(ctx: cmds.context):
    holder_name = holder_name = ctx.message.author.name
    succeed, data = Prediction.Show_Personal_Prediction(holder_name)

    if succeed:
        # # 1.
        embed = dc.Embed(
            title = '持有人: ' + holder_name,
            color = dc.Color.green(),
            timestamp = datetime.datetime.utcnow()
        )
        embed.add_field(name = "代號", value = data[0], inline = True)
        embed.add_field(name = "公司", value = data[1], inline = True)
        embed.add_field(name = "槓桿", value = data[2], inline = True)
        embed.add_field(name = "現在價格", value = data[3], inline = True)
        embed.add_field(name = "預測價格", value = data[4], inline = True)
        embed.add_field(name = "準確度", value = data[5], inline = True)
        embed.add_field(name = "預測日期", value = data[6], inline = True)

        await ctx.send(embed = embed)

        # 2.
        # s = ['代號     公司   張數(股)   持有價格  現在價格  損益  損益(%)  持有日期']
        # # This needs to be adjusted based on expected range of values or   calculated dynamically
        # for row in data:
        #     s.append('   '.join([str(item).center(5, ' ') for item in row]))
        #     # Joining up scores into a line
        # d = '```'+'\n'.join(s) + '```'
        # # Joining all lines togethor! 
        # embed = dc.Embed(title = '持有人: ' + holder_name, description = d, timestamp = datetime.datetime.utcnow())
        # await ctx.send(embed = embed)

        # 3.
        # output = t2a(
        #     header = ["id", "shares", "predicted price", "current price", "pnl", "pnl(%)", "expired date"],
        #     body = [[str(row['代號']), str(row['張數(股)']), str(row['持有價格']), str(row['現在價格']),
        #      str(row['損益']), str(row['損益(%)']), str(row['持有日期'])] for row in data],
        #     alignments = [Alignment.CENTER, Alignment.CENTER, Alignment.CENTER, Alignment.CENTER, Alignment.CENTER,
        #      Alignment.CENTER, Alignment.CENTER],
        #     style = PresetStyle.thin_compact
        # )
        # await ctx.send(f"```\n{output}\n```")

        print('personal data is showed successfully')

    else:
        await ctx.send('擷取個人資料失敗')

    print('listening to commands...')

@bot.command()
async def count(ctx: cmds.Context):
    succeed, data = Leaderboard.Calculate_All_Prediction_PnL()

    if succeed:
        if Leaderboard.Insert_Leaderboard_table(data):
            await ctx.send('分數上傳成功')

        else:
            await ctx.send('分數上傳失敗')
    else:
        await ctx.send('分數計算失敗')

    print('listening to commands...')

@bot.command()
async def all_rank(ctx: cmds.Context):
    succeed, data = Leaderboard.Show_Leaderboard()
    # print(data[0])

    if succeed:
        # 1.
        embed = dc.Embed(
            color = dc.Color.green(),
            timestamp = datetime.datetime.utcnow()
        )
        embed.add_field(name = "名稱", value = data[0], inline = True)
        embed.add_field(name = "分數", value = data[1], inline = True)

        await ctx.send(embed = embed)

        print('leaderboard is showed successfully')
    else:
        await ctx.send('擷取排行榜資料失敗')
    
    print('listening to commands...')

@bot.command()
async def create(ctx: cmds.Context):
    if Prediction.Create_Prediction_table():
        await ctx.send('已新增表格')
    else:
        await ctx.send('新增表格失敗')

    print('listening to commands...')

@bot.command(name = "drop", pass_context = True)
@cmds.has_permissions(administrator = True)
async def drop(ctx: cmds.Context):
    if Prediction.Drop_Prediction_table():
        await ctx.send('已刪除表格')
    else:
        await ctx.send('刪除表格失敗')

    print('listening to commands...')

@drop.error
async def drop_error(ctx, error):
    if isinstance(error, cmds.MissingPermissions):
        await ctx.send('您沒有權限刪除表格')

# img_path = ['./imgs/a.PNG', './imgs/b.PNG']    # Change it

# @bot.command()
# async def img(ctx: cmds.Context, id: int):
#     pic = dc.File(img_path[id])
#     await ctx.send(file = pic)

# captions = ['i didn''t try so hard', 'and got so close']     # Change it

# @bot.command()
# async def img_with_caption(ctx: cmds.Context, id: int):   # Finish it
#     pic = dc.File(img_path[id])   # 選擇圖片
#     await ctx.send(file = pic)   # 印出圖片
#     cap = captions[id]               # 選擇文字
#     await ctx.send(cap)           # 印出文字
#     pass