import discord 
import os
from datetime import datetime
import random

# トークン
TOKEN = os.environ['DISCORD_BOT_TOKEN']

CHANNEL_ID = 673191477412757554 # 起動メッセージチャンネル
CHANNEL_ID2 = 676132871257194497
great_owner_id = 459936557432963103# 作者ID
great_subowner_id = 675574345992634417
baner_count = 0
msg_count = 0
color_code = random.choice((0,0x1abc9c,0x11806a,0x2ecc71,0x1f8b4c,0x3498db,0x206694,0x9b59b6,0x71368a,0xe91e63,0xad1457,0xf1c40f,0xc27c0e,0xe67e22,0x95a5a6,0x607d8b,0x979c9f,0x546e7a,0x7289da,0x99aab5))
    
# 接続に必要なオブジェクトを生成
client = discord.Client()

# 起動メッセージ
@client.event
async def on_ready():
    print(client.user.name)  # ボットの名前
    print(client.user.id)  # ボットのID
    print(discord.__version__)  # discord.pyのバージョン
    print('----------------')
    print('Hello World,リマインドbotプログラム「project-RRN」、起動しました')
    channel = client.get_channel(CHANNEL_ID)
    await channel.purge()
    embed = discord.Embed(title="起動情報",description=" ",color=0xff0000)
    embed.set_image(url=client.user.avatar_url)
    await channel.send(embed=embed)
    await channel.send(f"名前:{client.user.name}\nID:{client.user.id}\nDiscord ver:{discord.__version__}\n--------------------------------\n状態:正常起動 ")
    await client.change_presence(status=discord.Status.idle,activity=discord.Game(name='Global Chat'))  

@client.event
async def on_message(message):

    global baner_count
    
    if message.content == "!baner":
        if message.author.id == great_owner_id or message.author.id == great_subowner_id:
            if baner_count == 2:
                baner_count = 0
                await message.channel.send(f"モード変更：" + str(baner_count))

            elif baner_count < 2:
                baner_count += 1
                await message.channel.send(f"モード変更：" + str(baner_count))

        if not message.author.id == great_owner_id or message.author.id == great_subowner_id:
            await message.channel.send("貴方は使えません。")

    elif message.content == "!check":
        if baner_count == 0:
            embed = discord.Embed(title=f"モード確認",description="じゃんけん(改)",color=color_code)
            await message.channel.send(embed=embed)
        elif baner_count == 1:
            embed = discord.Embed(title=f"モード確認",description="じゃんけん(理)",color=color_code)
            await message.channel.send(embed=embed)
        elif baner_count == 2:
            embed = discord.Embed(title=f"モード確認",description="お喋り",color=color_code)
            await message.channel.send(embed=embed)

    if message.author.bot:
        # もし、送信者がbotなら無視する
        return

    if message.content == "じゃんけん":

        if baner_count == 0:

            await message.channel.send( "最初はグー、じゃんけん" )
        
            def jankencheck(m):
                return m.content == "グー" or "チョキ" or "パー" and m.author == message.author
            try:
                reply = await client.wait_for( "message" , check = jankencheck , timeout = 10.0 )
            except asyncio.TimeoutError:
                await message.channel.send( "後出しはいけませんよ！\nあなたの負け！" )
            else:
                if reply.content == "チョキ":
                    prob = random.random()
    
                    if prob < 0.2:
                        await message.channel.send('パーを出しました。\nあなたの勝ち！')
                    elif prob < 0.6:
                        await message.channel.send('チョキを出しました。\nあいこです！')
                    else:
                        await message.channel.send('グーを出しました。\nあなたの負け！')

                elif reply.content == "パー":
                    prob = random.random()
    
                    if prob < 0.2:
                        await message.channel.send('グーを出しました。\nあなたの勝ち！')
                    elif prob < 0.6:
                        await message.channel.send('パーを出しました。\nあいこです！')
                    else:
                        await message.channel.send('チョキを出しました。\nあなたの負け！')

                elif reply.content == "グー":
                    prob = random.random()
    
                    if prob < 0.2:
                        await message.channel.send('チョキを出しました。\nあなたの勝ち！')
                    elif prob < 0.6:
                        await message.channel.send('グーを出しました。\nあいこです！')
                    else:
                        await message.channel.send('パーを出しました。\nあなたの負け！')

                elif not reply.content == "グー" or reply.content == "チョキ" or reply.content == "パー":
                    await message.channel.send("不適切な返事です。\nあなたの負け！")
                    return
                return

        elif baner_count == 1:

            await message.channel.send( "最初はグー、じゃんけん" )
        
            def jankencheck(m):
                return m.content == "グー" or "チョキ" or "パー" and m.author == message.author
            try:
                reply = await client.wait_for( "message" , check = jankencheck , timeout = 10.0 )
            except asyncio.TimeoutError:
                await message.channel.send( "後出しはいけませんよ！\nあなたの負け！" )
            else:
                if reply.content == "チョキ":
                    result = "グー"

                elif reply.content == "パー":
                    result = "チョキ"

                elif reply.content == "グー":
                    result = "パー"
     
                elif not reply.content == "グー" or reply.content == "チョキ" or reply.content == "パー":
                    await message.channel.send("不適切な返事です。\nあなたの負け！")
                    return

                await message.channel.send( result + "を出しました \nあなたの負け！" )
                return


client.run(TOKEN)
