import discord 
import os
from datetime import datetime

#トークン
TOKEN = os.environ['DISCORD_BOT_TOKEN']

CHANNEL_ID = 0 #起動メッセージチャンネル
ksi_ver = '6.0.1'
discord_py_ver = '3.7.3'

# 接続に必要なオブジェクトを生成
client = discord.Client()

#起動メッセージ
@client.event
async def on_ready():
    print(client.user.name)  # ボットの名前
    print(client.user.id)  # ボットのID
    print(discord.__version__)  # discord.pyのバージョン
    print('----------------')
    print('Hello World,リマインドbotプログラム「project-RRN」、起動しました')
    channel = client.get_channel(CHANNEL_ID)
    await channel.purge()
    await channel.send(f'名前:{client.user.name}')  # ボットの名前
    await channel.send(f'ID:{client.user.id}')  # ボットのID
    await channel.send(f'Discord ver:{discord.__version__}')  # discord.pyのバージョン
    await channel.send('----------------')
    await channel.send('状態：BOT再起動しました。')   
    await client.change_presence(status=discord.Status.idle,activity=discord.Game(name='創成の女神'))
    

@client.event
async def on_message(message):

    if message.author.bot:  # ボットを弾く。
        return 

client.run(TOKEN)
