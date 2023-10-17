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


class Views:
    def Embed(self, title):
        self.embed = discord.Embed(
            title= title,
            timestamp= datetime.now(),
            color=0x0000ff
        )
        return self.embed
    
    @classmethod
    def button_open(cls):
        cls.button_open = discord.ui.Button(
            label='開ける',
            style=discord.ButtonStyle.success,
            custom_id='room_open'
        )
        return cls.button_open
    
    @classmethod
    def button_rent(cls):
        cls.button_rent = discord.ui.Button(
            label='借りる',
            style=discord.ButtonStyle.success,
            custom_id='key_rent',
        )
        return cls.button_rent
    
    @classmethod
    def button_close(cls):
        cls.button_close = discord.ui.Button(
            label = '閉める',
            style = discord.ButtonStyle.success,
            custom_id='room_close'
        )
        return cls.button_close
    
    @classmethod
    def button_return(cls):
        cls.button_return = discord.ui.Button(
            label='返す',
            style=discord.ButtonStyle.danger,
            custom_id='key_return'
        )
        return cls.button_return
    
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
    button_rent = Views().button_rent()
    view = discord.ui.View()
    view.add_item(button_rent)
    
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
    view = discord.ui.View()
    
    #鍵を借りた時
    if custom_id == 'key_rent':
        em = Views()
        embed = em.Embed("借りました")
        embed.set_author(name=inter.user.name, icon_url=inter.user.avatar)
        
        #部屋を開けるボタン
        key_open = discord.ui.Button(
            label='開ける',
            style=discord.ButtonStyle.success,
            custom_id='room_open'
        )
        #view = discord.ui.View()
        view.add_item(key_open)
        
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
        em = Views()
        embed = em.Embed('開けました')
        embed.set_author(name=inter.user.display_name, icon_url=inter.user.avatar)
        
        #部屋を閉めるボタン
        key_close = discord.ui.Button(
            label='閉める',
            style=discord.ButtonStyle.success,
            custom_id='room_close'
        )
        #view = discord.ui.View()
        view.add_item(key_close)
        
        await inter.response.send_message(embed=embed, view=view)
    
    #部屋を閉めた時
    elif custom_id == 'room_close':
        em = Views()
        embed = em.Embed('閉めました')
        embed.set_author(name=inter.user.display_name, icon_url=inter.user.avatar)
        
        #鍵を返すボタン
        key_return = discord.ui.Button(
            label='返す',
            style=discord.ButtonStyle.danger,
            custom_id='key_return'
        )
        #view = discord.ui.View()
        view.add_item(key_return)
        
        #部屋を開けるボタン
        key_open = discord.ui.Button(
            label='開ける',
            style=discord.ButtonStyle.success,
            custom_id='room_open'
        )
        view.add_item(key_open)
        
        await inter.response.send_message(embed=embed, view=view)
    
    #鍵を返す時
    elif custom_id == 'key_return':
        em = Views()
        embed = em.Embed('返しました')
        embed.set_author(name=inter.user.display_name, icon_url=inter.user.avatar)
        
        #鍵を借りるボ
        key_rent = discord.ui.Button(
            label='借りる',
            style=discord.ButtonStyle.success,
            custom_id='key_rent'
        )
        view.add_item(key_rent)
        
        await inter.response.send_message(embed=embed, view=view)


#ボット起動のためのコード
client.run(os.getenv('TOKEN'))