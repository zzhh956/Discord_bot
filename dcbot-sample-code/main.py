import discord as dc
import discord.ext.commands as cmds
import create_db

channel_id = 10059344637     # Change it
token = 'MTAwNj'    # Change it
cmd_prefix = '!'            # Change it
bot = cmds.Bot(command_prefix=cmd_prefix, intents=dc.Intents.all())  

@bot.event
async def on_ready():
    await bot.wait_until_ready()
    print('>> Bot is on ready <<')
    c = bot.get_channel(channel_id)
    create_db.Portfolio.create_database()
    create_db.Portfolio.Create_Portfolio_table()
    await c.send('>> 您的股票小幫手已上線 <<')
    print('listening to commands...')

@bot.command()
async def hi(ctx: cmds.Context):
    await ctx.send('您好')    # change it

@bot.command()
async def drop(ctx: cmds.Context):
    if create_db.Portfolio.Drop_Portfolio_table():
        await ctx.send('已刪除表格')
    else:
        await ctx.send('刪除表格失敗')

    print('listening to commands...')

@bot.command()
async def create(ctx: cmds.Context):
    if create_db.Portfolio.Create_Portfolio_table():
        await ctx.send('已新增表格')
    else:
        await ctx.send('新增表格失敗')

    print('listening to commands...')

@bot.command()
async def buy(ctx: cmds.context, code: int, firm: str, holder_name: str, date: str, price: float, shares: int):
    data = [code, firm, holder_name, date, price, shares]
    if create_db.Portfolio.Insert_Portfolio_table(data):
        await ctx.send('已更新表格')
    else:
        await ctx.send('資料格式輸入有誤')

    print('listening to commands...')

# @bot.command()
# async def sell(ctx: cmds.context, code: int, firm: str, holder_name: str, shares: int):

# @bot.command()
# async def show(ctx: cmds.context):



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
