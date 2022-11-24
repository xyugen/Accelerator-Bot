from datetime import datetime
from discord.flags import Intents
import random
from discord.ext.commands import bot, Bot
from discord.ext import commands
from discord import activity
from discord import message
from discord import user
import discord
import os
from dotenv import load_dotenv
load_dotenv()


intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(description="Yugen's creation. Current version: 1.0.", command_prefix='al;',
                   intents=intents, allowed_mentions=discord.AllowedMentions(everyone=True))


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    print(f'ID: {bot.user.id}')
    print(datetime.now().strftime('%m/%d/%Y'))
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

    serBur = 892995233564987432
    serEwa = 1014765917038714901

    channel = bot.get_channel(1014766900154224751)

    if member.guild.id == serBur:
        channel = bot.get_channel(893315195831713803)
    elif member.guild.id == serEwa:
        channel = bot.get_channel(1014766900154224751)

    embed = discord.Embed(
        title="Welcome!", description=f"{member.mention} just joined the server. Let us welcome them, @everyone!")
    embed.set_author(name=f'{username} had joined!', icon_url=userAvatar)
    await channel.send(embed=embed)


@bot.event
async def on_member_remove(member):
    username = member.name.split('#')[0]
    userAvatar = member.avatar_url

    serBur = bot.get_guild(892995233564987432)
    serEwa = bot.get_guild(1014765917038714901)

    if member.guild.id == serBur:
        channel = bot.get_channel(893315195831713803)
    elif member.guild.id == serEwa:
        channel = bot.get_channel(1014766900154224751)

    embed = discord.Embed(
        title="Goodbye!", description=f"{member.mention} just left the server. Let us say our goodbyes, @everyone.")
    embed.set_author(name=f'{username} had left!', icon_url=userAvatar)
    await channel.send(embed=embed)

badwords = ['fuck', 'shit', 'bitch', 'puta', 'gago', 'deputa', 'tangina', 'ulol', 'ulul', 'tanga', 'inutil',
            'gunggong', 'gunggung', 'hunghang', 'tang ina', 'putangina', 'pota', 'potangina', 'putang ina', 'kingina', 'king ina']
link = ['https://', 'http://']
curses = True


@bot.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def curses(ctx, allow: bool = None):
    global curses
    if (allow == None):
        await ctx.send("Please pass in a proper argument.")
        return

    if (allow == True):
        if curses != True:
            curses = True
            await ctx.send("Curses are now allowed.")
        else:
            await ctx.send("Curses are already allowed.")
    elif (allow == False):
        if curses != False:
            curses = False
            await ctx.send("Curses are now disallowed.")
        else:
            await ctx.send("Curses are already disabled.")
    else:
        await ctx.send("Invalid argument")


@bot.event
async def on_message(message):
    msg = message.content.lower()
    global curses
    if message.author.bot:
        return
    else:
        if curses == True:
            for j in link:  # look for links in the message
                if j in msg:
                    return

            for i in badwords:  # look for profanities in the message
                if i in msg:
                    await message.delete()
                    await message.channel.send(f"{message.author.mention}, please avoid using profanity.\n**Message deleted:** ||{message.content}||")
                    bot.dispatch('profanity', message, i)
                    # So that it doesn't try to delete the message again, which will cause an error.
                    return

    await bot.process_commands(message)


@bot.event
# sends an error message when the entered command is not found
async def on_command_error(ctx, error):
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
async def joined(ctx, member: discord.Member = None):
    if member == None:
      member = ctx.message.author
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
    embed = discord.Embed(title=f"{arg}", color=0xFF5733)
    await ctx.send(embed=embed)
    await del_msg(ctx)

bot.run(os.getenv('DISCORD_TOKEN'))
