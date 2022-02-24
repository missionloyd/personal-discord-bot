import os
import discord, time
from discord.ext import commands, tasks
from dotenv import load_dotenv
from eth_price_stats import eth_price_stats
from unsplash_listener import unsplash
from whattomine_listener import coin_rankings
from genesis_listener import genesis_status, check_ping
from affirmations_listener import affirmation
from convo_listener import reply

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
channel_id = os.getenv('CHANNEL_ID')
client = commands.Bot(command_prefix='')

@tasks.loop(hours=0.5)
async def genesis():
    my_id = "520856458414522378"
    channel = await client.fetch_channel(channel_id)
    coa, wrapped_message = check_ping(genesis_status())

    if(coa == 'ping'):
        await channel.send(f"<@{my_id}> {wrapped_message}")
    else:
        await channel.send(wrapped_message)

@tasks.loop(hours=1)
async def ethereum():
    channel = await client.fetch_channel(channel_id)
    await channel.send(eth_price_stats())

@tasks.loop(hours=6)
async def wmine():
    channel = await client.fetch_channel(channel_id)
    await channel.send(coin_rankings(3))

@tasks.loop(hours=8)
async def affirmations():
    channel = await client.fetch_channel(channel_id)
    await channel.send(affirmation())

@client.command()
async def wtm(ctx):
    channel = await client.fetch_channel(channel_id)
    await channel.send(coin_rankings(3))

@client.command()
async def eth(ctx):
    channel = await client.fetch_channel(channel_id)
    await channel.send(eth_price_stats())

@client.command()
async def gene(ctx):
    my_id = "520856458414522378"
    channel = await client.fetch_channel(channel_id)
    coa, wrapped_message = check_ping(genesis_status())

    if(coa == 'ping'):
        await channel.send(f"<@{my_id}> {wrapped_message}")
    else:
        await channel.send(wrapped_message)

@client.command()
async def aff(ctx):
    channel = await client.fetch_channel(channel_id)
    await channel.send(affirmation())

@client.command()
async def c2(ctx):
    channel = await client.fetch_channel(channel_id)
    await channel.send(reply())

@client.command()
async def hello(ctx):
    await ctx.send(f"hello, {ctx.author.mention}")

@client.command()
async def usplash(ctx):
    channel = await client.fetch_channel(channel_id)
    await channel.send(unsplash())

@client.event
async def my_id(message):
    print(message.author.id)

@client.event
async def on_ready():
    channel = await client.fetch_channel(channel_id)
    await channel.send(f'{client.user} has Awoken!')
    print(f'{client.user} has Awoken!')

@client.event
async def logout():
    await client.logout()

genesis.start()
wmine.start()
ethereum.start()
affirmations.start()
client.run(TOKEN)