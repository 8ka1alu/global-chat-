import discord 
import os

# トークン
TOKEN = os.environ['DISCORD_BOT_TOKEN']

CHANNEL_ID = 673191477412757554 # 起動メッセージチャンネル
ksi_ver = '6.0.1'
discord_py_ver = '3.7.3'

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
    embed.set_thumbnail(url=AppInfo.icon_url)
    embed.add_field(name="名前",value=f"{client.user.name}")
    embed.add_field(name="ID",value=f"{client.user.id}")
    embed.add_field(name="Discord ver",value=f"{discord.__version__}")
    embed.add_field(name="----------------",value=" ")
    embed.add_field(name="状態",value="BOT再起動しました。")
    await channel.send(embed=embed) 
    await client.change_presence(status=discord.Status.idle,activity=discord.Game(name='Global Chat'))
    

@client.event
async def on_message(message):

    if message.author.bot:
        # もし、送信者がbotなら無視する
        return

# ------以下グローバルチャット------

    GLOBAL_CH_NAME1 = "operation-global-old" # グローバルチャット(embed)のチャンネル名
    GLOBAL_CH_NAME2 = "operation-global" # グローバルチャット(webhooks)のチャンネル名
    GLOBAL_WEBHOOK_NAME = "operation-global-wh" # グローバルチャットのWebhook名

    if message.channel.name == GLOBAL_CH_NAME1 or message.channel.name == GLOBAL_CH_NAME2:
        # hoge-globalの名前をもつチャンネルに投稿されたので、メッセージを転送する

        await message.delete() # 元のメッセージは削除しておく

        if 'discord.gg' in message.content:
            await message.channel.send("ここで招待は送れません。")
            return # 招待は送れません

        channels = client.get_all_channels()
        # channelsはbotの取得できるチャンネルのイテレーター
        
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
        global_channels2 = [ch for ch in channels if ch.name == GLOBAL_CH_NAME2]

        for channel in global_channels2:
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
