from discord.ext import commands

class Alarm(commands.Cog, name="Alarm"):  
    """Recieves Alarm Reactions"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        channel = message.channel
        split_message = message.content.split(" ")

        if ("Alarm: ") in message.content and message.author.bot == False:
            await channel.send("Setting alarm for " + split_message[1] + " " + split_message[2])

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        channel = reaction.message.channel

        if user != reaction.message.author:
            if reaction.emoji == "✅":
                await channel.send("Alarm On")
            elif reaction.emoji == "❌":
                await channel.send("Alarm Off")
            elif reaction.emoji == "⏰":
                await channel.send("Set time with the exact format:\nAlarm: HH:MM AM/PM")
            elif reaction.emoji == "❔":
                await channel.send("Status: Unknown")

def setup(bot: commands.Bot):
    bot.add_cog(Alarm(bot))