import discord
from discord import embeds
from discord.ext import commands

class Other(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # Commands
    @commands.command()
    async def ping(self, ctx):
        embed = discord.Embed(
            title='Pong!', description=f'My ping is {round(self.bot.latency * 1000)}ms.', color=0x0363ff)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Other(bot))
