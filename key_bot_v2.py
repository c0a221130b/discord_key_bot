import discord
from discord import app_commands

import os
from dotenv import load_dotenv
load_dotenv()

import time
from datetime import datetime
from tzlocal import get_localzone

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

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
        description=datetime.now().strftime('%m/%d %H:%M'),
        color = 0x0000ff,
        description = '操作を選択してください'
    )
    
    button = discord.ui.Button(
        label='借りる',
        style=discord.ButtonStyle.primary,
        custom_id='key_rent',
        color=0x00ff00
    )
    view = discord.ui.View()
    view.add_item(button)
    
    await channel.send(embed=embed, view=view)
    
    await tree.sync()
    

@client.event
async def on_interaction(inter:discord.Interaction):
    try:
        if inter.data['component_type'] == 2:
            await on_button_click(inter)
            
    except KeyError:
        pass
    
async def on_button_click(inter:discord.Interaction):
    custom_id = inter.data['custom_id']
    if custom_id == 'key_rent':
        embed = discord.Embed(
            title= '借りました',
            description=datetime.now().strftime('%m/%d %H:%M'),
            color=0x0000ff
        )
        embed.set_author(name=inter.user.name, icon_url=inter.user.avatar)
        
        button_open = discord.ui.Button(
            label='開ける',
            style=discord.ButtonStyle.primary,
            color=0xff0000,
            custom_id='room_open'
        )
        view = discord.ui.View()
        view.add_item(button_open)
        
        button_return = discord.ui.Button(
            label='返す',
            style=discord.ButtonStyle.primary,
            color=0x00ff00,
            custom_id='key_return'
        )
        await inter.response.send_message(embed=embed, view=view)
    
client.run(os.getenv('TOKEN'))