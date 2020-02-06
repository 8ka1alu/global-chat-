import discord 
import os
from datetime import datetime

# トークン
TOKEN = os.environ['DISCORD_BOT_TOKEN']

CHANNEL_ID = 673191477412757554 # 起動メッセージチャンネル
great_owner_id = 459936557432963103 # 作者ID
baner_count = 0

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
    
    #if message.author.bot:
        # もし、送信者がbotなら無視する
        #return

    if message.content == "!baner":
        if baner_count == 1:
            baner_count = 0
        elif baner_count == 0:
            baner_count = 1
    elif message.content == "!check":
        await message.channel.send(baner_count)
    
client.run(TOKEN)
