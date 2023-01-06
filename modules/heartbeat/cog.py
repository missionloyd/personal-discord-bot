import discord
from discord.ext import commands

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

class Scheduler(commands.Cog):
    """Schedule commands."""
    def __init__(self, bot):
        self.bot = bot

    # Scheduled events
    async def schedule_jobs(self):

      print('hello world')

    def schedule(self):
        # Initialize scheduler

        job_defaults = {
            "coalesce": True,
            "max_instances": 5,
            "misfire_grace_time": 15,
            "replace_existing": True,
        }

        scheduler = AsyncIOScheduler(job_defaults = job_defaults)

        # Add jobs to scheduler
        scheduler.add_job(self.schedule_func, CronTrigger.from_crontab("*/10 * * * * *")) 
        # Every hour