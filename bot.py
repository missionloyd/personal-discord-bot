import discord, time, json, os, subprocess, aiocron
from discord.ext import commands, tasks
from dotenv import load_dotenv
from heartbeat_listener import latest_heartbeat
from lights_listener import toggle_group
from eth_price_stats import eth_price_stats
from unsplash_listener import unsplash_listener
from whattomine_listener import whattomine_listener
from genesis_listener import genesis_status, check_ping
from dogapi_listener import dogapi
from convo_listener import reply

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
MY_ID = "520856458414522378"
channel_id = os.getenv('CHANNEL_ID')
MINER = ''
client = commands.Bot(command_prefix='', case_insensitive=True)

# lights
themes = list()
f = open('/home/pi/dev/python/personal-discord-bot/scene_manifest.json', 'r')
data = json.load(f)

for scene in data['scenes']:
    themes.append(scene['emoji'])

reactions = ["💡", "❓"]

# load cogs
for folder in os.listdir("/home/pi/dev/python/personal-discord-bot/modules"):
    if os.path.exists(os.path.join("/home/pi/dev/python/personal-discord-bot/modules", folder, "cog.py")):
        client.load_extension(f"modules.{folder}.cog")

@aiocron.crontab('0 9 * * *')
async def cronjob():
    channel = await client.fetch_channel(channel_id)
    ping, response = latest_heartbeat('Student Union')

    if ping:
        await channel.send(response)
        await channel.send(f"<@{MY_ID}>, heartbeat is having issues!")
    else:
        await channel.send(response)

@tasks.loop(hours=0.5)
async def genesis():
    channel = await client.fetch_channel(channel_id)
    coa, wrapped_message = check_ping(genesis_status())

    if(coa == 'ping'):
        await channel.send(f"<@{MY_ID}> {wrapped_message}")
    else:
        await channel.send(wrapped_message)

@tasks.loop(hours=6)
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
async def heartbeat(ctx):
    channel = await client.fetch_channel(channel_id)
    ping, response = latest_heartbeat('Student Union')

    if ping:
        await channel.send(response)
        await channel.send(f"<@{MY_ID}>, heartbeat might be having issues!")
    else:
        await channel.send(response)

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
    channel = await client.fetch_channel(channel_id)
    coa, wrapped_message = check_ping(genesis_status())

    if(coa == 'ping'):
        await channel.send(f"<@{MY_ID}> {wrapped_message}")
    else:
        await channel.send(wrapped_message)

@client.command()
async def on(ctx):
    channel = await client.fetch_channel(channel_id)
    await channel.send(toggle_group("Living Room"))

@client.command()
async def off(ctx):
    channel = await client.fetch_channel(channel_id)
    await channel.send(toggle_group("Living Room"))

@client.command()
async def lights(ctx):
    channel = await client.fetch_channel(channel_id)
    reactions.extend(themes)
    separator = ', '
    menu = "**Living Room** Light Options:\nOn/Off: 💡\nStatus: ❓\nThemes: " + separator.join(themes) + "\n"

    message = await channel.send(menu)

    for reaction in reactions:
        await message.add_reaction(reaction)

@client.command()
async def luke(ctx):
    channel = await client.fetch_channel(channel_id)
    reactions.extend(themes)
    separator = ', '
    menu = "**Luke's Room** Light Options:\nOn/Off: 💡\nStatus: ❓\nThemes: " + separator.join(themes) + "\n"

    message = await channel.send(menu)

    for r in reactions:
        await message.add_reaction(r)
    

@client.command()
async def alarm(ctx):
    channel = await client.fetch_channel(channel_id)
    message = await channel.send("Alarm Options:\nOn: ✅\nOff: ❌\nTime: ⏰\nStatus: ❔")
    alarm_reactions = ["✅", "❌", "⏰", "❔"]

    for r in alarm_reactions:
        await message.add_reaction(r)

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
async def top(ctx):
    channel = await client.fetch_channel(channel_id)
    filename = 'top.txt'
    cpu_command = """sudo top -bn2 | grep '%Cpu' | tail -1 | grep -P '(....|...) id,'|awk '{print "CPU Utilization: " 100-$8 "%"}'"""
    output = subprocess.run(cpu_command, shell=True, stdout=subprocess.PIPE).stdout.decode('utf-8')
    await channel.send(str(output))

@client.command()
async def mine(ctx):
    channel = await client.fetch_channel(channel_id)
    command = '/home/pi/monero/xmrig/build/xmrig -o solo-xmr.2miners.com:4444 -u 452PwiwBT4r9FP81pY7uY9dYi1XEEqM4cV4eajAsJoxpg55DzM2cC685Vqh73LmJwg1p66aBzwy4XT7D2H3vK7BFVBn9Yad -p pi'
    miner = subprocess.Popen(command, shell=True)
    await channel.send('**Starting Miner...**')

@client.command()
async def stop(ctx):
    channel = await client.fetch_channel(channel_id)
    if(miner != ''):
        miner.terminate()
        await channel.send('**Stopping Miner...**')
        miner = ''
    else:
        await channel.send('**Cannot Stop Miner...**')

@client.command()
async def xmr(ctx):
    channel = await client.fetch_channel(channel_id)
    await channel.send('https://solo-xmr.2miners.com/account/452PwiwBT4r9FP81pY7uY9dYi1XEEqM4cV4eajAsJoxpg55DzM2cC685Vqh73LmJwg1p66aBzwy4XT7D2H3vK7BFVBn9Yad')

@client.command()
async def rvn(ctx):
    channel = await client.fetch_channel(channel_id)
    await channel.send('https://rvn.2miners.com/account/RPU5Nq3jvRhCKNrrEcpNkccDuapjRJGP9t')

@client.command()
async def reboot(ctx):
    channel = await client.fetch_channel(channel_id)
    await channel.send("Goodbye!")
    command = "sudo reboot"
    subprocess.Popen(command, shell=True)

@client.event
async def my_id(message):
    print(message.author.id)

@client.event
async def on_ready():
    channel = await client.fetch_channel(channel_id)
    await channel.send(f"<@{MY_ID}>, I'm awake!")
    print(f'{client.user} has Awoken!')

@client.event
async def logout():
    await client.logout()

# genesis.start()
wmine.start()
ethereum.start()
dogs.start()
client.run(TOKEN)