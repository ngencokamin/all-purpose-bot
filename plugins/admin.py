import discord
from discord.ext import commands
from discord.ext.commands import has_permissions

from discord import app_commands

from sqlitedict import SqliteDict as DB

intents = discord.Intents().all()

class AdminStuff(commands.GroupCog, name="plugin"):
    def __init__(self, bot):
        self.bot = bot
        self.db = DB('db/db.sqlite', tablename='plugins')

    @app_commands.command(name="enable")
    @has_permissions(administrator=True)
    async def enable(self, interaction: discord.Interaction, plugin: str):
        plugins = self.db[interaction.guild.id]
        plugins[plugin] = True
        self.db[interaction.guild.id] = plugins
        self.db.commit()
        await interaction.response.send_message(f'Plugin {plugin} enabled', ephemeral=True)

    @app_commands.command(name="disable")
    @has_permissions(administrator=True)
    async def disable(self, interaction: discord.Interaction, plugin: str):
        plugins = self.db[interaction.guild.id]
        plugins[plugin] = False
        self.db[interaction.guild.id] = plugins
        self.db.commit()
        await interaction.response.send_message(f'Plugin {plugin} disabled', ephemeral=True)


    @disable.error
    @enable.error
    async def admin_error(self, interaction, error):
        await interaction.response.send_message(f'Error {error}', ephemeral=True)


async def setup(bot):
    await bot.add_cog(AdminStuff(bot))