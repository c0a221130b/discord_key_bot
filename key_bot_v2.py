# discord.pyをインポート
import discord
from discord import app_commands

#トークンが入ったevnファイルを読み込むためのモジュール
import os
from dotenv import load_dotenv
load_dotenv()

#借りた時間を表示させるためのモジュール
import time
from datetime import datetime
from tzlocal import get_localzone

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

#起動時に実行される関数
@client.event
async def on_ready():
    print('-------------------')
    print('on_ready')
    print(client.user.name)
    print(discord.__version__)
    print('-------------------')
    print(f'waiting {60 - datetime.now(get_localzone()).second} sec for loop to start')
    time.sleep(60 - datetime.now(get_localzone()).second)
    channel = client.get_channel(1100228900501594179)
    
    embed = discord.Embed(
        title = 'on ready',
        #description=datetime.now().strftime('%m/%d %H:%M'),
        color = 0x0000ff,
        description = '操作を選択してください'
    )
    
    button = discord.ui.Button(
        label='借りる',
        style=discord.ButtonStyle.success,
        custom_id='key_rent',
    )
    view = discord.ui.View()
    view.add_item(button)
    
    await channel.send(embed=embed, view=view)
    
    await tree.sync()
    

#イントラクションを読み込むための関数
@client.event
async def on_interaction(inter:discord.Interaction):
    try:
        if inter.data['component_type'] == 2:
            await on_button_click(inter)
            
    except KeyError:
        pass

#ボタンが押された時の関数
async def on_button_click(inter:discord.Interaction):
    custom_id = inter.data['custom_id']
    
    #鍵を借りた時
    if custom_id == 'key_rent':
        embed = discord.Embed(
            title= '借りました',
            description=datetime.now().strftime('%m/%d %H:%M'),
            color=0x0000ff
        )
        embed.set_author(name=inter.user.name, icon_url=inter.user.avatar)
        
        #部屋を開けるボタン
        button_open = discord.ui.Button(
            label='開ける',
            style=discord.ButtonStyle.success,
            custom_id='room_open'
        )
        view = discord.ui.View()
        view.add_item(button_open)
        
        #鍵を返すボタン
        button_return = discord.ui.Button(
            label='返す',
            style=discord.ButtonStyle.danger,
            custom_id='key_return'
        )
        view.add_item(button_return)
        await inter.response.send_message(embed=embed, view=view)
    
    #部屋を開けた時
    elif custom_id == 'room_open':
        embed = discord.Embed(
            title = '開けました',
            description = datetime.now().strftime('%m/%d %H:%M'),
            color=0x0000ff
        )
        
        embed.set_author(name=inter.user.name, icon_url=inter.user.avatar)
        
        #部屋を閉めるボタン
        button_close = discord.ui.Button(
            label = '閉める',
            style = discord.ButtonStyle.success,
            custom_id='room_close'
        )
        
        view = discord.ui.View()
        view.add_item(button_close)
        
        await inter.response.send_message(embed=embed, view=view)

#ボット起動のためのコード
client.run(os.getenv('TOKEN'))