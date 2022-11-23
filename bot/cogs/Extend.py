import discord
from discord.ext import commands
from discord import app_commands
import sql_methods as sql_methods
import validators
import random
import lorem


class Extend(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot


    @app_commands.command(name= 'extend', description = 'Extends your link!')
    async def extend(self, interaction: discord.Interaction, link: str) -> None:
        length = 0
        await interaction.response.send_message('Processing...', ephemeral=True)
        if not validators.url(link):
            await interaction.edit_original_message(content='Invalid URL!')
            return
        extended = ""
        for _ in range(5):
            extended += lorem.paragraph()
        extended = extended.replace(' ', '-')
        extended = extended.replace('.', '')
        extended = extended.replace(',', '')
        sql_methods.insertLink(link, extended)
        await interaction.edit_original_message(content=f'Done!, your link is http://127.0.0.1:5000/{extended}')


async def setup(bot: commands.Bot):
    await bot.add_cog(Extend(bot))