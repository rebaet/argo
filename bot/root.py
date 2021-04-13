import discord
import os

from configparser import ConfigParser
import os

client = discord.Client()


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
      return

    call = message.content



client.run(os.environ.get('DISCORD_TOKEN'))  
