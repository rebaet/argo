import os
import discord
import pickle

client = discord.Client()
with open('bot/dat.txt', 'rb') as file:
  dat = pickle.load(file)

def save_changes_to_dat():
  with open('bot/dat.txt', 'wb') as file:
    pickle.dump(dat, file)


@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  call = message.content
  user = message.author


  # BOT PREFIX
  if call.startswith("argo"):  
    
    # LOOK FOR COMMAND
    if len(call.strip().split()) >> 1:    
      command = call.strip().split()[1]


    # OPEN A NEW ACCOUNT
    if command == 'newacc':
      if user.id not in dat:    
        dat[user.id] = {'wallet':0}
        await message.channel.send("account created")
        save_changes_to_dat()
      else:
        await message.channel.send("account already exits")

    # CHECK ACCOUNT
    if command == 'check':      
      if user.id in dat:
        await message.channel.send("account exists")
      else:
        await message.channel.send("account not found. \nenter 'argo newacc' to create one")

    # CHECK WALLET
    if command == 'wallet':
      if user.id in dat:
            await message.channel.send("you own " + str(dat[user.id]['wallet']) + ' coins')
      else:
        await message.channel.send("account not found. \nenter 'argo newacc' to create one")
          

client.run(os.environ.get('DISCORD_TOKEN'))  