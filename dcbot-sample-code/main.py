import datetime
import discord as dc
import discord.ext.commands as cmds
import portfolio

channel_id =      # Change it
token = ''    # Change it
cmd_prefix = '!'            # Change it
bot = cmds.Bot(command_prefix=cmd_prefix, intents=dc.Intents.all())  

@bot.event
async def on_ready():
    await bot.wait_until_ready()
    print('>> Bot is on ready <<')
    c = bot.get_channel(channel_id)
    portfolio.Portfolio.create_database()
    portfolio.Portfolio.Create_Portfolio_table()
    await c.send('>> 您的股票小幫手已上線 <<')
    print('listening to commands...')

@bot.command()
async def hi(ctx: cmds.Context):
    await ctx.send('您好')    # change it

@bot.command(name = "drop", pass_context = True)
@cmds.has_permissions(administrator = True)
async def drop(ctx: cmds.Context):
    if portfolio.Portfolio.Drop_Portfolio_table():
        await ctx.send('已刪除表格')
    else:
        await ctx.send('刪除表格失敗')

    print('listening to commands...')

@drop.error
async def drop_error(ctx, error):
    if isinstance(error, cmds.MissingPermissions):
        await ctx.send('您沒有權限刪除表格')

@bot.command()
async def create(ctx: cmds.Context):
    if portfolio.Portfolio.Create_Portfolio_table():
        await ctx.send('已新增表格')
    else:
        await ctx.send('新增表格失敗')

    print('listening to commands...')

@bot.command()
async def buy(ctx: cmds.context, code: int, firm: str, holder_name: str, date: str, price: float, shares: int):
    data = [code, firm, holder_name, date, price, shares]
    if portfolio.Portfolio.Insert_Portfolio_table(data):
        await ctx.send('已更新表格')
    else:
        await ctx.send('資料格式輸入有誤')

    print('listening to commands...')

# @bot.command()
# async def sell(ctx: cmds.context, code: int, firm: str, holder_name: str, shares: int):

@bot.command()
async def show(ctx: cmds.context, name: str):
    data = []
    check, data = portfolio.Portfolio.Select_Portfolio_table(name)

    if check:
        await ctx.send('今天日期: ' + str(datetime.date.today()))
        await ctx.send('持有人: ' + name)
        await ctx.send('代號       公司        持有日期       持有價格       持有量(股)       損益       損益(%)       現在價格')
        for row in data:
            await ctx.send(row['代號'] + '     ' + row['公司名稱'] + '     ' + str(row['持有日期']) + '       ' + str(row['持有價格']) + '            ' + str(row['持有量(股)']) 
            + '                 ' + str(row['損益']) + '             ' + str(row['損益(%)']) + '             ' + str(row['現在價格']))
    else:
        await ctx.send('擷取資料失敗')

    print('listening to commands...')

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

bot.run(token)
