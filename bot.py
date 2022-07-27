import os
import discord, time
from discord.ext import commands, tasks
from dotenv import load_dotenv
from eth_price_stats import eth_price_stats
from unsplash_listener import unsplash_listener
from whattomine_listener import whattomine_listener
from genesis_listener import genesis_status, check_ping
from dogapi_listener import dogapi
from convo_listener import reply
from lights_listener import checkTime

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
channel_id = os.getenv('CHANNEL_ID')
client = commands.Bot(command_prefix='')

# load cogs
for folder in os.listdir("modules"):
    if os.path.exists(os.path.join("modules", folder, "cog.py")):
        client.load_extension(f"modules.{folder}.cog")

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
    await channel.send(whattomine_listener(3))

@tasks.loop(hours=8)
async def dogs():
    channel = await client.fetch_channel(channel_id)
    await channel.send(dogapi())

@client.command()
async def wtm(ctx):
    channel = await client.fetch_channel(channel_id)
    await channel.send(whattomine_listener(3))

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
async def lights(ctx):
    channel = await client.fetch_channel(channel_id)
    message = await channel.send("Light Options:\nOn: 🌞\nOff: 🌚\nStatus: ❓")
    await message.add_reaction("🌞")
    await message.add_reaction("🌚")
    await message.add_reaction("❓")

@client.command()
async def alarm(ctx):
    channel = await client.fetch_channel(channel_id)
    message = await channel.send("Alarm Options:\nOn: ✅\nOff: ❌\nTime: ⏰\nStatus: ❔")
    await message.add_reaction("✅")
    await message.add_reaction("❌")
    await message.add_reaction("⏰")
    await message.add_reaction("❔")

@client.command()
async def aff(ctx):
    channel = await client.fetch_channel(channel_id)
    await channel.send(dogapi())

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
    await channel.send(unsplash_listener())

@client.command()
async def reboot(ctx):
    channel = await client.fetch_channel(channel_id)
    await channel.send("Goodbye!")
    os.system("sudo reboot")

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
dogs.start()
client.run(TOKEN)