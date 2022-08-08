import discord
from discord.ext import commands
from lights_listener import display_status, toggle_group, set_scene
from bot import themes, data

client = commands.Bot(command_prefix='')

class Lights(commands.Cog, name="Lights"):  
    """Recieves Lights Reactions"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        channel = reaction.message.channel
        message = reaction.message.content

        if user != reaction.message.author:
            if reaction.emoji == "💡":
                await channel.send(toggle_group(message))
                
            elif reaction.emoji == "❓":
                await channel.send(display_status())

            elif reaction.emoji in themes:
                set_scene(message, reaction.emoji, themes, data, 4)
            

        
    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):

        channel = discord.utils.get(self.bot.get_all_channels(), id=payload.channel_id)
        if payload.emoji.name == "💡":
            message = await channel.fetch_message(payload.message_id)
            await channel.send(toggle_group(message.content))



def setup(bot: commands.Bot):
    bot.add_cog(Lights(bot))