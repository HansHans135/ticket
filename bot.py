from discord_components import *
import discord
from datetime import datetime,timezone,timedelta
import os
import threading
from flask import Flask, request
from flask import render_template

######
#設定#
#####

bot = ComponentsBot(command_prefix="1",help_command=None)
ULR = "http://hbot.fun/"
#線上看網址





def startweb():
    app = Flask(__name__)
    @app.route("/", methods=['GET'])
    def hello():
        id = request.args.get('id')
        r=open(f"web/{id}.txt","r")
        s = r.read()
        new_s = s.replace('\n','<br>')
        print(new_s)
        return new_s
    app.run(host="0.0.0.0",port=25596)
t = threading.Thread(target=startweb)  #建立執行緒
t.start()


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}!")


@bot.command()
async def ticket(ctx):
    await ctx.send("有問題?\n創建一個私人頻道來聯繫管理員吧!",components = [Button(label = "開啟客服單", custom_id = "open",style=ButtonStyle.green)])
    
@bot.event
async def on_button_click(interaction):
    def check(m):
        return m.author == interaction.author and m.channel == interaction.channel
    if interaction.component.custom_id == "open":
      overwrites = {
          interaction.author: discord.PermissionOverwrite(read_messages=True),
          interaction.guild.me: discord.PermissionOverwrite(read_messages=True),
          interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False)
  }
      channel = discord.utils.get(interaction.guild.categories, name='客服單')
      客服單 = await interaction.guild.create_text_channel(name=f"ticket-{interaction.author.name}-hbot", category=channel, overwrites=overwrites)
      dt1 = datetime.utcnow().replace(tzinfo=timezone.utc)
      dt2 = dt1.astimezone(timezone(timedelta(hours=8)))
      now = dt2.strftime("%Y-%m-%d %H:%M:%S")
      with open(f"data/{客服單.id}.txt", 'a') as filt:
        filt.write(f'客服單系統by Hbot\n\n創建時間:{now}\n頻道名稱:{客服單.name}\n創建人:{interaction.author}\n以下為詳細的對話紀錄:\n\n\n')
      await interaction.send(f'開了一張ticket在 <#{客服單.id}>')
      await 客服單.send(f'<@{interaction.author.id}>\n歡迎來到你的客服單\n請說明你的問題以便我們處理',components = [Button(label = "關閉客服單", custom_id = "close",style=ButtonStyle.red)])

    if interaction.component.custom_id == "close":
        if "ticket" in interaction.channel.name:
          dt1 = datetime.utcnow().replace(tzinfo=timezone.utc)
          dt2 = dt1.astimezone(timezone(timedelta(hours=8)))
          now = dt2.strftime("%Y-%m-%d %H:%M:%S")
          txt =f"data/{interaction.channel.id}.txt"
          webid=interaction.channel.id
          with open(f"data/{interaction.channel.id}.txt", 'a') as filt:
            filt.write(f'\n\n關閉人:{interaction.author}\n關閉時間:{now}')
          await interaction.channel.delete()
          await interaction.author.send(f'你在**{interaction.guild.name}**的客服單已經關閉摟\n以下是對話紀錄:\n或是你要線上看? {ULR}?id={webid}', file=discord.File(txt))
          src=f'data/{webid}.txt'
          des=f'web/{webid}.txt'
          os.rename(src,des)

@bot.event
async def on_message(message):
  filepath = f"data/{message.channel.id}.txt"
  if os.path.isfile(filepath):
     with open(f"data/{message.channel.id}.txt", 'a') as filt:
      dt1 = datetime.utcnow().replace(tzinfo=timezone.utc)
      dt2 = dt1.astimezone(timezone(timedelta(hours=8)))
      now = dt2.strftime("%Y-%m-%d %H:%M:%S")
      filt.write(f'{now}|{message.author}:{message.content}\n')

  if message.content == 'h!ticket':
    if message.author.guild_permissions.manage_messages:
        await message.channel.send("有問題?\n創建一個私人頻道來聯繫管理員吧!",components = [Button(label = "開啟客服單", custom_id = "open",style=ButtonStyle.green)])
    else:
      await message.channel.send("你沒有權限欸,要不要在你自己的伺服器試試看")

bot.run("TOKEN在這")
