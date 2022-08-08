from discord.ext import commands
import time, json, os
from lights_listener import check_time, strobe_alarm
from threading import Thread, Timer, Event

class Alarm(commands.Cog, name="Alarm"):  
    """Recieves Alarm Reactions"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.timer = False
        self.alarm = '99:99'

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

        # flag = Event()
        c = CountingTask()
        t = Thread(target=c.run, args=(self.alarm, 21))

        if user != reaction.message.author:
            if reaction.emoji == "✅":
                await channel.send("Alarm On: " + self.alarm)
                t.start()

            elif reaction.emoji == "❌":
                await channel.send("Alarm Off: " + self.alarm)
                c.terminate()
                # t.join()

            elif reaction.emoji == "⏰":
                await channel.send("Set time with the exact format:\nAlarm: HH:MM")

            elif reaction.emoji == "❔":
                await channel.send("Status: " + self.alarm + " (" + str(c.running()) + ")")

def setup(bot: commands.Bot):
    bot.add_cog(Alarm(bot))

class CountingTask:

    def __init__(self):
        self._running = True
        self._target = True

    def run(self, t, count):
        while self._running and self._target:
            self._target = check_time(t)
            time.sleep(5)

        if(self._running and self._target == False):
            print("Alarm Triggered")
            index = 0
            while index < count:
                strobe_alarm(count)
                index+=1
        else:
            print("Alarm Cancelled")

        return 0

    def terminate(self):
        print("Alarm Terminated")
        self._running = False
        self._target == False

    def running(self):
        return self._running
            