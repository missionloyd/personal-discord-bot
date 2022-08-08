from discord.ext import commands
import time, json, os
from lights_listener import check_time, strobe_alarm
from threading import Thread, Lock, Timer, Event

class Alarm(commands.Cog, name="Alarm"):  
    """Recieves Alarm Reactions"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.timer = False
        self.alarm = '99:99'
        self.lock = Lock()

    @commands.Cog.listener()
    async def on_message(self, message):
        channel = message.channel

        if (":") in message.content and message.author.bot == False and len(message.content) == 5:
            alarm = message.content
            await channel.send("Setting alarm for " + alarm)
            self.alarm = alarm

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        channel = reaction.message.channel

        stopFlag = Event()
        timer = MyThread(self.alarm, stopFlag, count=10)

        if user != reaction.message.author:
            if reaction.emoji == "✅":
                await channel.send("Alarm On: " + self.alarm)
                timer.start()

            elif reaction.emoji == "❌":
                await channel.send("Alarm Off: " + self.alarm)
                stopFlag.set()

            elif reaction.emoji == "⏰":
                await channel.send("Set time with the exact format:\nAlarm: HH:MM")

            elif reaction.emoji == "❔":
                await channel.send("Status: " + self.alarm + " (" + str(self.timer) + ")")

def setup(bot: commands.Bot):
    bot.add_cog(Alarm(bot))

class MyThread(Thread):
    def __init__(self, time, event, count):
        Thread.__init__(self)
        self.time = time
        self.stopped = event
        self.count = count

    def run(self):
        while not self.stopped.wait(1):
            check_time(self.time, self.count)
            