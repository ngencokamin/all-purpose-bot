import discord
from discord.ext import commands
from discord.ext.commands import has_permissions

intents = discord.Intents().all()

class DebuggingTools(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="reload", pass_context=True, intents=intents, hidden=True)
    @commands.is_owner()
    async def reload_ext(self,ctx, arg):
        await self.bot.reload_extension(f'plugins.{arg}')
    
    @reload_ext.error
    async def test_error(self, ctx):
        await ctx.send('You are not owner')

    @commands.command(name="load", pass_context=True, intents=intents, hidden=True)
    @commands.is_owner()
    async def load_ext(self,ctx, arg):
        await self.bot.load_extension(f'plugins.{arg}')
    
    @load_ext.error
    async def test_error(self, ctx):
        await ctx.send('You are not owner')

    @commands.command(name="unload", pass_context=True, intents=intents, hidden=True)
    @commands.is_owner()
    async def unload_ext(self,ctx, arg):
        await self.bot.unload_extension(f'plugins.{arg}')
    
    @unload_ext.error
    async def test_error(self, ctx):
        await ctx.send('You are not owner')


async def setup(bot):
    await bot.add_cog(DebuggingTools(bot))