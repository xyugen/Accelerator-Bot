import discord
from discord import user
from discord import message
from discord import activity
from discord.ext import commands
from discord.ext.commands import bot, Bot
import random
from discord.flags import Intents

client = discord.Client(activity=discord.Game(name='al;help'))

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(description="Yugen's creation. Current version: 1.0.", command_prefix='al;',
                   intents=intents, allowed_mentions=discord.AllowedMentions(everyone=True))

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.event
async def on_ready(msg):
    channel = bot.get_channel(893003734924271616)
    embed = discord.Embed(title=f"Accel is Online!", description='Type "al;help to see more of my commands."', color=0xFF5733)
    await channel.send(embed=embed)

global username
global user_id
global member
global userAvatar

@bot.event
async def on_member_join(member):
    username = member.name.split('#')[0]
    userAvatar = member.avatar_url
    channel = bot.get_channel(893315195831713803)
    embed = discord.Embed(
        title="Welcome!", description=f"{member.mention} just joined the server. Let us welcome them, @everyone!")
    embed.set_author(name=f'{username} had joined!', icon_url=userAvatar)
    await channel.send(embed=embed)

@bot.event
async def on_member_remove(member):
    username = member.name.split('#')[0]
    userAvatar = member.avatar_url
    channel = bot.get_channel(893315195831713803)
    embed = discord.Embed(
        title="Goodbye!", description=f"{member.mention} just left the server. Let us say our goodbyes, @everyone.")
    embed.set_author(name=f'{username} had left!', icon_url=userAvatar)
    await channel.send(embed=embed)

async def del_msg(msg):
    await msg.message.delete()

@bot.command(pass_context=True, name='add', help="Adds two numbers")
async def add(ctx, left: int, right: int):
    await ctx.send(left + right)


@bot.command(pass_context=True, name='subt', help="Substracts two numbers")
async def subt(ctx, left: int, right: int):
    await ctx.send(left - right)


@bot.command(pass_context=True, name='mult', help="Multiplies two numbers")
async def mult(ctx, left: int, right: int):
    await ctx.send(left * right)


@bot.command(pass_context=True, name='div', help="Divides two numbers")
async def div(ctx, left: int, right: int):
    await ctx.send(left / right)


@bot.command(pass_context=True, name='choose', help="Choose between given choices.")
async def choose(ctx, *choices: str):
    await ctx.send(random.choice(choices))


@bot.command(pass_context=True, name='joined', help="Checks the members date and time of joining the server.")
async def joined(ctx, member: discord.Member):
    await ctx.send('{0.name} joined in {0.joined_at}'.format(member))


@bot.command(pass_context=True, name='repeat', help="Repeats and deletes your message.")
async def repeat(ctx, *, arg):
    user_id = ctx.author.id
    channel = bot.get_channel(ctx.channel.id)
    await ctx.send(f'<@{user_id}>: {arg}')
    await del_msg(ctx)


@bot.command(pass_context=True, name='announce', help="Send your message to announcement channel.")
async def announce(ctx, title, *, arg):
    username = ctx.author.name.split('#')[0]
    user_id = ctx.author.id
    member = ctx.message.author
    userAvatar = member.avatar_url
    channel = bot.get_channel(893003734924271616)
    embed = discord.Embed(title=title, description=arg, color=0xFF5733)
    embed.set_author(name=username, icon_url=userAvatar)
    await channel.send(embed=embed)


@bot.command(pass_context=True, name='tell', help='I will retell what you told me.')
async def tell(ctx, *, arg):
    user_id = ctx.author.id
    embed=discord.Embed(title=f"{arg}", color=0xFF5733)
    await ctx.send(embed=embed)
    await del_msg(ctx)

bot.run(os.getenv('DISCORD_TOKEN'))
