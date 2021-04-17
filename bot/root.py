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
          await message.channel.send("account exists. id: " + str(user.id))
        else:
          await message.channel.send("account not found. \nenter 'argo newacc' to create one")

      # DELETE ACCOUNT
      if command == 'delacc':
        if user.id in dat:
          dat.pop(user.id)
          await message.channel.send('account deleted')
          save_changes_to_dat()
        else:
          await message.channel.send('first create an account to delete it dumass!')  

      # CHECK WALLET
      if command == 'wallet':
        if user.id in dat:
          await message.channel.send("you own " + str(dat[user.id]['wallet']) + ' coins')
        else:
          await message.channel.send("account not found. \nenter 'argo newacc' to create one")

      # ADD MONEY TO WALLET
      if command == 'add':
        if user.id in dat:
          dat[user.id]['wallet'] += int(call.strip().split()[2])
          await message.channel.send(str(call.strip().split()[2]) + ' coins deposited to your account')
          await message.channel.send("your new balance is " + str(dat[user.id]['wallet']) + ' coins')
          save_changes_to_dat()
        else:
          await message.channel.send("account not found. \nenter 'argo newacc' to create one") 

      # TAKEOUT
      if command == 'takeout':
            
        #CHECK IF USER HAS SUFFICIENT FUNDS    
        if dat[user.id]['wallet'] >= int(call.strip().split()[2]): 

          if user.id in dat:
            dat[user.id]['wallet'] -= int(call.strip().split()[2])
            await message.channel.send(str(call.strip().split()[2]) + ' coins deducted to your account')
            await message.channel.send("your new balance is " + str(dat[user.id]['wallet']) + ' coins')
            save_changes_to_dat()
          else:
            await message.channel.send("account not found. \nenter 'argo newacc' to create one")     

        else:
          await message.channel.send("insufficient funds")

      # GIVE/TRANSFER
      if command == 'transfer' or command == 'give':
            
        if  '!' in str(call.strip().split()[3]) or '&' in str(call.strip().split()[3]):
          reciever = int(str(call.strip().split()[3])[3:-1])
        else:
          reciever = int(str(call.strip().split()[3])[2:-1])

        # CHECK IF USER EXISTS
        if user.id in dat: 

          #CHECK IF USER HAS SUFFICIENT FUNDS    
          if dat[user.id]['wallet'] >= int(call.strip().split()[2]):

            # CHECK IF RECIEVER EXISTS  
            if reciever in dat:
                
              # ADD TO RECIEVER    
              dat[reciever]['wallet'] += int(call.strip().split()[2])
              # DEDUCT FROM USER
              dat[user.id]['wallet'] -= int(call.strip().split()[2])

              await message.channel.send(str(call.strip().split()[2]) + ' coins transfered to' + str(call.strip().split()[3]) + "'s account")
              await message.channel.send("your new balance is " + str(dat[user.id]['wallet']) + ' coins')
              save_changes_to_dat()
            else:
              await message.channel.send("reciever argo account not found")

          else:    
            await message.channel.send("insufficient funds")

        else:
          await message.channel.send("account not found. \nenter 'argo newacc' to create one") 
        
      # CHECK OTHER'S WALLET
      if command == 'sneak':
          
        if  '!' in str(call.strip().split()[3]) or '&' in str(call.strip().split()[3]):
              reciever = int(str(call.strip().split()[3])[3:-1])
        else:
          reciever = int(str(call.strip().split()[3])[2:-1])

        # CHECK IF USER EXISTS
        if user.id in dat: 

          # CHECK IF RECIEVER EXISTS  
          if reciever in dat:
            await message.channel.send(str(call.strip().split()[2]) + ' has ' + str(dat[reciever]['wallet']) + ' coins in his wallet')
          else:
            await message.channel.send("reciever argo account not found")

        else:
          await message.channel.send("account not found. \nenter 'argo newacc' to create one") 
    

client.run(os.environ.get('DISCORD_TOKEN'))