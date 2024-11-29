from mirror import nodeA, nodeB

import discord
import schedule
import threading
import time

async def disconnect_message():
    print()
    print(f'🪞  Severing connection with user {nodeA.name} 🪞' if nodeA.isDM else f'🪞  Severing connection with channel {nodeA.name} in server {nodeA.guild} 🪞')
    await nodeA.channel.send(f'🪞  Severing connection with user {nodeA.name} 🪞' if nodeA.isDM else f'🪞  Severing connection with channel {nodeA.name} in server {nodeA.guild} 🪞')
    print(f'🪞  Severing connection with user {nodeB.name} 🪞' if nodeB.isDM else f'🪞  Severing connection with channel {nodeB.name} in server {nodeB.guild} 🪞')
    await nodeB.channel.send(f'🪞 Severing connection with user `{nodeA.name}` 🪞' if nodeA.isDM else f'🪞 Severing connection with channel `{nodeA.name}` in server `{nodeA.guild}` 🪞')
    await nodeA.set_permissions(nodeA.guild.default_role, send_messages=False)
    await nodeB.set_permissions(nodeB.guild.default_role, send_messages=False)