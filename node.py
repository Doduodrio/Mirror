import discord

class Node():
  # want: node accepts channel object
  # want: node has name, guild, isDM, and channel attributes
  def __init__(self, channel=None):
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