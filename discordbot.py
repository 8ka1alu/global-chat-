import discord 
import os
from datetime import datetime

# トークン
TOKEN = os.environ['DISCORD_BOT_TOKEN']

CHANNEL_ID = 673191477412757554 # 起動メッセージチャンネル
great_owner_id = 459936557432963103 # 作者ID

GLOBAL_CH_NAME1 = "operation-global-old" # グローバルチャット(embed)のチャンネル名
GLOBAL_CH_NAME2 = "operation-global" # グローバルチャット(webhooks)のチャンネル名
GLOBAL_WEBHOOK_NAME = "operation-global-wh" # グローバルチャットのWebhook名

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
    
    if message.author.bot:
        # もし、送信者がbotなら無視する
        return

    if message.content == '!restart': 
        if message.author.id == great_owner_id:
            await message.channel.send('再起動します')
            await asyncio.sleep(0.5)
            await client.logout()  
            os.execv(sys.executable,[sys.executable, os.path.join(sys.path[0], __file__)] + sys.argv[1:])  
        if not message.author.id == great_owner_id:
            await message.channel.send('貴方にこのコマンドの使用権限はありません')   

    if message.content == '!webhook':
        await message.delete()
        if message.author.id == great_owner_id:
            webhooks = await message.channel.webhooks() # 既存のwebhookの取得
    
            if not webhooks:
                await message.channel.send("Webhookがないので作成します。")
                try:
                    await message.channel.create_webhook(name=GLOBAL_WEBHOOK_NAME)
                except:
                    await message.channel.send("Webhookの作成に失敗しました。")
                else:
                    await message.channel.send("作成しました(name="+GLOBAL_WEBHOOK_NAME+")")
            else:
                await message.channel.send("既に作成されています。")
        else:
            await message.channel.send("貴方はこのコマンドを扱えません")
        return

# ------以下グローバルチャット------

    if message.channel.name == GLOBAL_CH_NAME1 or message.channel.name == GLOBAL_CH_NAME2:
        # hoge-globalの名前をもつチャンネルに投稿されたので、メッセージを転送する

        await message.delete() # 元のメッセージは削除しておく

        if 'discord.gg' in message.content:
            await message.channel.send("ここで招待は送れません。")
            return # 招待は送れません

        channels = client.get_all_channels()
        # channelsはbotの取得できるチャンネルのイテレーター

    if message.channel.name == GLOBAL_CH_NAME2 or message.channel.name == GLOBAL_CH_NAME1:
            
        # embed式
        global_channels = [ch for ch in channels if ch.name == GLOBAL_CH_NAME1]
        # global_channelsは hoge-global の名前を持つチャンネルのリスト

        embed = discord.Embed(title="hoge-global",
            description=message.content, color=0x00bfff)

        embed.set_author(name=message.author.display_name, 
            icon_url=message.author.avatar_url_as(format="png"))
        embed.set_footer(text=f"{message.guild.name} / {message.channel.name}",
            icon_url=message.guild.icon_url_as(format="png"))
        # Embedインスタンスを生成、投稿者、投稿場所などの設定

        for channel in global_channels:
            # メッセージを埋め込み形式で転送
            await channel.send(embed=embed)

        # webhooks式
        global_channels = [ch for ch in channels if ch.name == GLOBAL_CH_NAME2]

        for channel in global_channels:
            ch_webhooks = await channel.webhooks()
            webhook = discord.utils.get(ch_webhooks, name=GLOBAL_WEBHOOK_NAME)

            if webhook is None:
                # そのチャンネルに hoge-webhook というWebhookは無かったので無視
                continue
            await webhook.send(content=message.content,
                username=message.author.name,
                avatar_url=message.author.avatar_url_as(format="png"))

# ------ここまでグローバルチャット------

client.run(TOKEN)
