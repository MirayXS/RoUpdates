import requests
import discord
import time
from discord.ext import tasks, commands
import json
from datetime import date
from discord.utils import get
from discord.ext.commands import check, MissingRole, CommandError
intents = discord.Intents.all()
bot_config = json.loads(open("./config/config.json", "r").read())
client = commands.Bot(command_prefix=bot_config["bot_prefix"],intents=intents)
POST_CHANNEL = bot_config["channelId"]

@client.event
async def on_ready():
	await client.change_presence(activity=discord.Game(name="Checks \"Roblox Version Status\" every 10mins - RobloxGameClient"))
	print('<----------- NEW SESSION ----------->')
	print('[SUCCESS] : Logged in as ' + format(client.user))
	print('-------------------------------------\n\n')
	await robloxgameclient_loop.start()

# Use this command to ping the bot, or to know if the bot crashed.
@client.command(pass_context=True)
async def ping(ctx):
	await ctx.send("> `Pong! " + str(round(client.latency * 1000)) + "ms`")

# RobloxGameClient
@tasks.loop(seconds=600) # Delay For 10 Minutes (600 seconds).
async def robloxgameclient_loop():
	oldData = requests.get('https://pastebin.com/raw/zKYiWUkg') # I Use This Pastebin To Use and Update Versions. This is old data.
	time.sleep(10)
	newData = requests.get('http://setup.roblox.com/version') # This is the endpoint where Roblox updates their version number. This is new data.
	if newData.text in oldData.text: # if the new data is the same as the old data...
		print("[ERROR] ( [X] ) No New RobloxGameClient Version!")
	if newData.text not in oldData.text: # if the new data is **not** the same as the old data...
		print("[SUCCESS] ( [OK] ) New RobloxGameClient Version!\n")
		print("\n<----------------------------------->\nNew RobloxGameClient Version: "+newData.text)
		print("-------------------------------------")
		print("\n<----------------------------------->\nOld RobloxGameClient Version: "+oldData.text)
		print("-------------------------------------")
		channel = client.get_channel(POST_CHANNEL)
		embed = discord.Embed(title="RobloxGameClient", description="RobloxGameClient\n`"+oldData.text+"` -> `" + newData.text + "`\n\n~~"+oldData.text+"~~\n"+newData.text, color=0x43B581)
		embed.add_field(name="RobloxGameClient Version", value="```\n" + newData.text + "\n```", inline=False)
		embed.add_field(name="Old RobloxGameClient Version", value="```\n"+oldData.text+"\n```", inline=True)
		embed.add_field(name="New RobloxGameClient Version", value="```\n" + newData.text+"\n```", inline=True)
		await channel.send("RobloxGameClient has been updated", embed=embed)

# RobloxGameClient - before_loop
@robloxgameclient_loop.before_loop
async def before_some_task():
  await client.wait_until_ready()



client.run(bot_config["bot_token"])
