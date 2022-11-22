import discord
from discord import embeds
from discord.ext import commands
import random

class Other(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # Commands
    @commands.command(pass_context=True, help='Shows my ping.')
    async def ping(self, ctx):
        embed = discord.Embed(
            title='Pong!', description=f'My ping is {round(self.bot.latency * 1000)}ms.', color=0x0363ff)
        await ctx.send(embed=embed)
        
    @commands.command(pass_context=True, help='Shows relevant informations about the user.')
    # @commands.has_any_role('Burnik', 893275489832140830)
    async def userinfo(self, ctx, *, user: discord.Member = None): # b'\xfc'
        if user is None:
            user = ctx.author      
        date_format = "%a, %d %b %Y %I:%M %p"
        embed = discord.Embed(color=0xdfa3ff, description=user.mention)
        embed.set_author(name=str(user), icon_url=user.avatar_url)
        embed.set_thumbnail(url=user.avatar_url)
        embed.add_field(name="Joined", value=user.joined_at.strftime(date_format))
        members = sorted(ctx.guild.members, key=lambda m: m.joined_at)
        embed.add_field(name="Join position", value=str(members.index(user)+1))
        embed.add_field(name="Registered", value=user.created_at.strftime(date_format))
        if isinstance(ctx.channel, discord.DMChannel):
            return
        if len(user.roles) > 1:
            role_string = ' '.join([r.mention for r in user.roles][1:])
            embed.add_field(name="Roles [{}]".format(len(user.roles)-1), value=role_string, inline=False)
        perm_string = ', '.join([str(p[0]).replace("_", " ").title() for p in user.guild_permissions if p[1]])
        embed.add_field(name="Guild permissions", value=perm_string, inline=False)
        embed.set_footer(text='ID: ' + str(user.id))
        return await ctx.send(embed=embed)

    @commands.command(pass_context=True, help='Number guessing game. From 1 to 100.')
    async def game(self, ctx):
        number = random.randint(0, 100)
        for i in range(0, 5):
            await ctx.send('Guess')
            response = await self.bot.wait_for('message', check=lambda message: message.author == ctx.author)
            guess = int(response.content)
            if guess > number:
                await ctx.send('Smaller')
            elif guess < number:
                await ctx.send('Bigger')
            elif guess == number:
                await ctx.send(f'You guessed it! The answer is {number}.')
                
    @commands.command(pass_context=True, help='Verifies a member.')
    @commands.has_any_role('Burnik', int(893275489832140830))
    async def verify(self, ctx, user: discord.Member):
        roles = discord.utils.find(
            lambda r: r.name == 'Verified', ctx.message.guild.roles)
        role = discord.utils.get(ctx.message.guild.roles, name="Verified")
        if ctx.author == user:
            await ctx.send("You can't verify yourself.")
            await ctx.message.delete()
            return
        elif ctx.channel.id != 898078983038599218:
            await ctx.send('You can only verify in <#898078983038599218> channel.')
            await ctx.message.delete()
            return
        elif roles in user.roles:
            await ctx.send(f'{ctx.author.mention}, {user.mention} is already verified.')
            await ctx.message.delete()
        else:
            await discord.Member.add_roles(user, role)
            await ctx.send(f'{user.mention} has been verified by {ctx.author.mention}.')
            await ctx.message.delete()
                
def setup(bot):
    bot.add_cog(Other(bot))
