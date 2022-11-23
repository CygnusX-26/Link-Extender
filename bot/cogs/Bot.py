import discord
from discord.ext import commands
from discord import app_commands


class Bot(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.change_presence(
            status=discord.Status.online,
            activity=discord.Game(f"Extending your links!"))
        print('This bot is online!')


async def setup(bot: commands.Bot):
    await bot.add_cog(Bot(bot))