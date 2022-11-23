import discord
import os
from discord.ext import commands
import sqlite3
from os.path import join, dirname, abspath


db_path = join(dirname(dirname(abspath(__file__))), 'bot/data/links.db')
conn = sqlite3.connect(db_path, check_same_thread=False)
c = conn.cursor()

class SkyBlockBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=commands.when_mentioned_or(os.getenv("PREFIX")),
            description='SkyBlock Bot',
            intents=discord.Intents.all(),
            application_id = 1017634463221567488)
    
    async def load_extensions(self):
        for filename in os.listdir("bot/cogs"):
            if filename.endswith(".py"):
                await self.load_extension(f"cogs.{filename[:-3]}")

    async def setup_hook(self):
        self.remove_command('help')
        await self.load_extensions()
        await bot.tree.sync()
        

# creates a new user table if one doesn't currently exist
try:
    c.execute("""CREATE TABLE links (
            url text,
            extended text
            )""")
    c.close()
except:
    pass



bot = SkyBlockBot()
bot.run(os.getenv("DISCORD_BOT_TOKEN"))
