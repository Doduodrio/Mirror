# LazyUnacceptableObjects

from dotenv import load_dotenv
import datetime
import os
import typing

import discord
from discord import app_commands

load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.typing = True
client = discord.Client(
  activity = discord.Game(name='Pokémon Blue', start=datetime.datetime.now()),
  intents=intents
)
tree = app_commands.CommandTree(client)

class Node():
  # want: node accepts channel object
  # want: node has name, guild, isDM, and channel attributes
  def __init__(self, channel):
    if channel is None: # for the on_typing before on_ready case
      self.name = ''
      self.id = None
      self.guild = None
      self.isDM = False
      self.channel = None
    elif isinstance(channel, (discord.User, discord.Member)):
      self.name = channel.name
      self.id = None
      self.guild = None
      self.isDM = True
      self.channel = channel
    else:
      self.name = channel.name
      self.id = channel.id
      self.guild = channel.guild
      self.isDM = False
      self.channel = channel
nodeA: Node = Node(None)
nodeB: Node = Node(None)
logging, logtime = True, ''
public = True

# override the default print function!
print_copy = print
def print(*args, **kwargs):
  print_copy(*args, **kwargs)
  if not logging:
    return
  # log 2024-01-01 00.00.00.txt
  with open(f'logs/log {logtime}.txt', 'a') as log:
    print_copy(*args, file=log, **kwargs)

# other functions
async def connected():
  print()
  print(f'🪞  Connection established with user {nodeA.name} 🪞' if nodeA.isDM else f'🪞  Connection established with channel {nodeA.name} in server {nodeA.guild} 🪞')
  await nodeA.channel.send(f'🪞 Connection established with user `{nodeB.name}` 🪞' if nodeB.isDM else f'🪞 Connection established with channel `{nodeB.name}` in server `{nodeB.guild}` 🪞')
  print(f'🪞  Connection established with user {nodeB.name} 🪞' if nodeB.isDM else f'🪞  Connection established with channel {nodeB.name} in server {nodeB.guild} 🪞')
  await nodeB.channel.send(f'🪞 Connection established with user `{nodeA.name}` 🪞' if nodeA.isDM else f'🪞 Connection established with channel `{nodeA.name}` in server `{nodeA.guild}` 🪞')
def fromNode(channel, user) -> str:
  if isinstance(channel, discord.channel.DMChannel): # from DMChannel
    if user.name == nodeA.name:
      return 'A'
    elif user.name == nodeB.name:
      return 'B'
    else:
      return ''
  else: # from TextChannel
    if channel.id == nodeA.id:
      return 'A'
    elif channel.id == nodeB.id:
      return 'B'
    else:
      return ''
def now() -> str: #returns current timestamp in [hh:mm:ss] format
  time = datetime.datetime.now()
  date = [time.hour%24, time.minute, time.second]
  for i in range(len(date)):
    date[i] = str(date[i])
    if len(date[i])==1: date[i] = '0' + date[i]
  return f'[{date[0]}:{date[1]}:{date[2]}]'
def validate(i: discord.Interaction) -> bool:
  if i.user.id in [i.guild_owner.id, 587040390603866122]:
    return True
  return False
def get_logtime() -> str:
  time = datetime.datetime.now()
  date = [time.year, time.month, time.day + (-1 if (time.hour-7)%24 > time.hour else 0), (time.hour-7)%24, time.minute, time.second]
  for i in range(len(date)):
    date[i] = str(date[i])
    if len(date[i])==1: date[i] = '0' + date[i]
  return f'{date[0]}-{date[1]}-{date[2]} {date[3]}.{date[4]}.{date[5]}'

@client.event
async def on_ready():
  global me, logtime, nodeA, nodeB
  logtime = get_logtime()
  # to clear commands from global CommandTree
  # tree.clear_commands(guild=None)
  # await tree.sync(guild=None)
  for guild in client.guilds:
    tree.copy_global_to(guild=guild)
    await tree.sync(guild=guild)
  # await tree.sync(guild=None)
  guilds = '\n - '.join([f'{guild.name} (id: {guild.id})' for guild in client.guilds])
  print('\n' + f'{client.user} is active in the following guilds:')
  print(f' - {guilds}\n')
  # to default connect to a DMChannel, use Node(client.get_user(id))
  # to default connect to a TextChannel, use Node(client.get_channel(id))
  if not public: # connect to these channels for testing
    nodeA = Node(client.get_user(587040390603866122)) # doduodrio
    nodeB = Node(client.get_channel(1265494340248272949)) # mirror-testing, Cold Storage
  else: # connect to these channels when public
    nodeA = Node(client.get_channel(1276015059608535135)) # 🪱-long-distance, The Yellow Goats
    nodeB = Node(client.get_channel(1275471439675396230)) # telephony, BiffCord
  me = client.get_user(587040390603866122) # doduodrio
  await me.send('Mirror, mirror on the wall, who\'s the fairest one of all?')
  print('Mirror sent a DM to doduodrio (id: 587040390603866122) upon activating!')
  await connected()

@client.event
async def on_message(message):
  global nodeA, nodeB
  # don't respond to own messages
  if message.author == client.user:
    return

  node = fromNode(message.channel, message.author)
  if node == '':
    return

  prev_msg_2 = None
  if message.reference and message.reference.resolved:
    # 1 = message.channel, 2 = other channel
    prev_msg_1 = await message.channel.fetch_message(message.reference.message_id)
    channel1 = nodeA.channel if node == 'A' else nodeB.channel
    history1 = [message async for message in channel1.history(limit=50)]
    channel2 = nodeB.channel if node == 'A' else nodeA.channel
    history2 = [message async for message in channel2.history(limit=49)]
    history2.insert(0, history1[0])
    index1 = -1
    for i in range(50):
      if history1[i].id == prev_msg_1.id:
        index1 = i
    if history2[index1].content == prev_msg_1.content:
      prev_msg_2 = history2[index1]
    
  if node == 'A':
    if message:
      if prev_msg_2 is None:
        print('\n' + f'{now()} [A] {message.author}: {message.content}')
        await nodeB.channel.send(message.content)
      else:
        print('\n' + f'{now()} [A] Reply to {message.author}: {prev_msg_2.content}\n               {message.author}: {message.content}')
        await prev_msg_2.reply(message.content)
    else:
      print('\n' + f'{now()} [A] {message.author}: *(Message couldn\'t be displayed)*')
      await nodeB.channel.send('*(Message couldn\'t be displayed)*')
  elif node == 'B':
    if message:
      if prev_msg_2 is None:
        print('\n' + f'{now()} [B] {message.author}: {message.content}')
        await nodeA.channel.send(message.content)
      else:
        print('\n' + f'{now()} [A] Reply to {message.author}: {prev_msg_2.content}\n               {message.author}: {message.content}')
        await prev_msg_2.reply(message.content)
    else:
      print('\n' + f'{now()} [B] {message.author}: *(Message couldn\'t be displayed)*')
      await nodeA.channel.send('*(Message couldn\'t be displayed)*')

@client.event
async def on_typing(channel, user, when):
  global nodeA, nodeB
  # do not respond to self typing
  if user.discriminator != '0':
    return

  # send typing indicator to channel
  node = fromNode(channel, user)
  if node == 'A':
    print('\n' + f'{now()} [A] {user} is typing...')
    await nodeB.channel.typing()
  elif node == 'B':
    print('\n' + f'{now()} [B] {user} is typing...')
    await nodeA.channel.typing()

@tree.command(description='Set this location as a node')
@app_commands.describe(node='The node to replace')
@app_commands.rename(node='node_to_replace')
@app_commands.check(validate)
async def set_as_node(i: discord.Interaction, node: str):
  global nodeA, nodeB
  if node == nodeA.name and i.channel.name not in [nodeA.name, nodeB.name]:
    nodeA = Node(i.user) if isinstance(i.channel, discord.channel.DMChannel) else Node(i.channel)
  elif node == nodeB.name and i.channel.name not in [nodeA.name, nodeB.name]:
    nodeB = Node(i.user) if isinstance(i.channel, discord.channel.DMChannel) else Node(i.channel)
  else:
    print('\n' + f'{now()} [{i.user.name}] Could not set {node} as a node')
    await i.response.send_message(f'**[ERROR]** Could not set `{node}` as a node.', ephemeral=True)
    return
  await i.response.send_message('This channel was successfully set as a node!', ephemeral=True)
  await connected()
@set_as_node.autocomplete('node')
async def set_as_node_autocomplete(i: discord.Interaction, current: str) -> typing.List[app_commands.Choice[str]]:
  return [
    app_commands.Choice(name=nodeA.name, value=nodeA.name),
    app_commands.Choice(name=nodeB.name, value=nodeB.name)
  ]
@set_as_node.error
async def set_as_node_error(i: discord.Interaction, error):
  print('\n' + f'{now()} [{i.user.name}] Tried to set node without permission.')
  await i.response.send_message('**[ERROR]** You don\'t have permission to set nodes!', ephemeral=True)

# @tree.context_menu(name='Replace Node A as a node')
# async def set_as_node_A(i: discord.Interaction, user: discord.Member):
#   global nodeA, nodeB
#   if not (user.name == nodeA.name and nodeA.isDM):
#     nodeA = Node(user)
#     await i.response.send_message(f'{user} was successfully set as a node!')
#     await connected()
#   else:
#     print('\n' + f'{now()} [{i.user.name}] Could not set {user} as a node.')
#     await i.response.send_message(f'**[ERROR]** Could not set `{user}` as a node.', ephemeral=True)

client.run(TOKEN)