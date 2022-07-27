from discord.ext import commands

class Lights(commands.Cog, name="Lights"):  
    """Recieves Lights Reactions"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        channel = reaction.message.channel

        if user != reaction.message.author:
            if reaction.emoji == "🌞":
                await channel.send("Lights On")
            elif reaction.emoji == "🌚":
                await channel.send("Lights Off")
            elif reaction.emoji == "❓":
                await channel.send("Status: Unknown")

def setup(bot: commands.Bot):
    bot.add_cog(Lights(bot))