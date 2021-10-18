import os
import discord
from discord import user
from discord import message
from discord import activity
from discord.ext import commands
from discord.ext.commands import bot, Bot
import random
from discord.flags import Intents

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(description="Yugen's creation. Current version: 1.0.", command_prefix='al;',
                   intents=intents, allowed_mentions=discord.AllowedMentions(everyone=True))

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    print(f'ID: {bot.user.id}')
    print('-----------')
    await bot.change_presence(activity=discord.Game('with your feelings.'))

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
    
badwords = ['fuck', 'shit', 'bitch', 'puta', 'gago', 'deputa', 'tangina', 'ulol', 'ulul', 'tanga', 'inutil', 'gunggong', 'gunggung', 'hunghang', 'tang ina', 'putangina', 'pota', 'potangina', 'putang ina', 'kingina', 'king ina']

@bot.event
async def on_message(message):
  if message.author.bot:
        return
  else:
   for i in badwords: # Go through the list of bad words;
      if i in (message.content.lower()):
         await message.delete()
         await message.channel.send(f"{message.author.mention}, please avoid using profanity.\n**Message deleted:** ||{message.content}||")
         bot.dispatch('profanity', message, i)
         return # So that it doesn't try to delete the message again, which will cause an error.
   await bot.process_commands(message)

@bot.event
async def on_command_error(ctx, error): #sends an error message when the entered command is not found
    if isinstance(error, commands.CommandNotFound):
        await ctx.channel.send(f"**ERROR:** Sorry {ctx.author.mention}, but this command either doesn't exist or it's disabled. Contact <@560612243012845578> for more info.")
    else:
        raise error
        
@bot.command(pass_context=True)
async def load(ctx, extension):
    bot.load_extension(f'cogs.{extension}')

@bot.command(pass_context=True)
async def unload(ctx, extension):
    bot.unload_extension(f'cogs.{extension}')

for filename in os.listdir('cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')
    else:
      print(f'Unable to load {filename[:-3]}')
        
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
@commands.has_any_role('Burnik', 893275489832140830)
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
