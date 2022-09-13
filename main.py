import discord
from discord.ext import commands
import logging, json, platform, os, random
from pathlib import Path
import datetime


#current working directory
cwd = str(Path(__file__).parents[0])
print(f"{cwd}\n-----")

#defining stuff
cmd_prefix = "k!" #cmd_prefix = ["k!", "K!"]
secret_file = json.load(open(cwd+'/bot_config/secret.json'))
intents = discord.Intents.all()
kurisu = commands.Bot(command_prefix=["k!", "K!"], case_insensitive=True, intents=intents, owner_id=294325550330413056) #note the prefix
kurisu.config_token = secret_file['token']
logging.basicConfig(level=logging.INFO)
kurisu.blacklisted_users = []
kurisu.cwd = cwd

pythonVersion = platform.python_version()
discordpyVersion = discord.__version__
kurisu.version = '1.0.0'

kurisu.colors = {
  'WHITE': 0xFFFFFF,
  'AQUA': 0x1ABC9C,
  'GREEN': 0x2ECC71,
  'BLUE': 0x3498DB,
  'PURPLE': 0x9B59B6,
  'LUMINOUS_VIVID_PINK': 0xE91E63,
  'GOLD': 0xF1C40F,
  'ORANGE': 0xE67E22,
  'RED': 0xE74C3C,
  'NAVY': 0x34495E,
  'DARK_AQUA': 0x11806A,
  'DARK_GREEN': 0x1F8B4C,
  'DARK_BLUE': 0x206694,
  'DARK_PURPLE': 0x71368A,
  'DARK_VIVID_PINK': 0xAD1457,
  'DARK_GOLD': 0xC27C0E,
  'DARK_ORANGE': 0xA84300,
  'DARK_RED': 0x992D22,
  'DARK_NAVY': 0x2C3E50
}
kurisu.colour_list = [c for c in kurisu.colours.values()] #if error, because of colour != color


#random images
imgExtension = ["png", "jpeg", "jpg"] #Image Extensions to be chosen from
allImages = list()

def chooseRandomImage(directory="images"):
    for img in os.listdir(directory): #Lists all files
        ext = img.split(".")[len(img.split(".")) - 1]
        if (ext in imgExtension):
            allImages.append(img)
    choice = random.randint(0, len(allImages) - 1)
    chosenImage = allImages[choice] #Do Whatever you want with the image file
    return chosenImage

#dealing with json files
def read_json(filename):
    with open(f"{cwd}/bot_config/{filename}.json", "r") as file:
        data = json.load(file)
    return data

def write_json(data, filename):
    with open(f"{cwd}/bot_config/{filename}.json", "w") as file:
        json.dump(data, file, indent=4)


#Bot loading
@kurisu.event
async def on_ready():
    print("""
--------------------------------------------------------------------------------------------------------------------------
  _  __                 _                   ____            _       _            ___            _   _                  _ 
 | |/ /  _   _   _ __  (_)  ___   _   _    | __ )    ___   | |_    (_)  ___     / _ \   _ __   | | (_)  _ __     ___  | |
 | ' /  | | | | | '__| | | / __| | | | |   |  _ \   / _ \  | __|   | | / __|   | | | | | '_ \  | | | | | '_ \   / _ \ | |
 | . \  | |_| | | |    | | \__ \ | |_| |   | |_) | | (_) | | |_    | | \__ \   | |_| | | | | | | | | | | | | | |  __/ |_|
 |_|\_\  \__,_| |_|    |_| |___/  \__,_|   |____/   \___/   \__|   |_| |___/    \___/  |_| |_| |_| |_| |_| |_|  \___| (_)
                                                                                                                         
--------------------------------------------------------------------------------------------------------------------------
    """)
    
    print(f"Running version {discordpyVersion} of Discord.py\n-----\nLogged in as: {kurisu.user.name} : {kurisu.user.id}\n-----\nMy current prefix is {cmd_prefix}\n-----")
    print(f'{kurisu.user} is connected to the following guilds:')
    for guild in kurisu.guilds:
        print(f'{guild.name}(id: {guild.id})')

    data = read_json("blacklist")
    kurisu.blacklisted_users = data["blacklistedUsers"]

    await kurisu.change_presence(activity=discord.Activity(type=3, name=f" over {len(kurisu.guilds)} servers | Use {cmd_prefix}"))

#Error handling
@kurisu.event
async def on_command_error(ctx, error):
    #Ignore these errors
    ignored = (commands.CommandNotFound, commands.UserInputError)
    if isinstance(error, ignored):
        return

    #Begin error handling
    if isinstance(error, commands.CommandOnCooldown):
        m, s = divmod(error.retry_after, 60)
        h, m = divmod(m, 60)
        if int(h) == 0 and int(m) == 0:
            await ctx.send(f' You must wait {int(s)} seconds to use this command!')
        elif int(h) == 0 and int(m) != 0:
            await ctx.send(f' You must wait {int(m)} minutes and {int(s)} seconds to use this command!')
        else:
            await ctx.send(f' You must wait {int(h)} hours, {int(m)} minutes and {int(s)} seconds to use this command!')
    elif isinstance(error, commands.CheckFailure):
        await ctx.send("Hey! You lack permission to use this command.")
    raise error #error handling to show in terminal

#Blacklist handler
@kurisu.event
async def on_message(message):
    #ignore ourselves
    if message.author.id == kurisu.user.id:
        return

    #blacklist system
    if message.author.id in kurisu.blacklisted_users:
        return

    if message.content.lower().startswith("help"):
        await message.channel.send("Hey! Why don't you run the help command with `k!help`")

    #await bot.process_commands(message)

#Blacklist manager
@kurisu.command()
@commands.is_owner()
async def blacklist(ctx, user: discord.Member):
    if ctx.message.author.id == user.id:
        await ctx.send("You cannot blacklist yourself!")
        return

    kurisu.blacklisted_users.append(user.id)
    data = read_json("blacklist")
    data["blacklistedUsers"].append(user.id)
    write_json(data, "blacklist")
    await ctx.send(f"{user.name} has been blacklisted.")

@kurisu.command()
@commands.is_owner()
async def unblacklist(ctx, user: discord.Member):
    kurisu.blacklisted_users.remove(user.id)
    data = read_json("blacklist")
    data["blacklistedUsers"].remove(user.id)
    write_json(data, "blacklist")
    await ctx.send(f"{user.name} has been unblacklisted.")

#Bot commands
@kurisu.command(name='hello', aliases=['hi'], help='Says hello!')
async def _hello(ctx):
    await ctx.send(f"Hello {ctx.author.mention}!")
    #await ctx.send(f"Hi <@{ctx.author.id}>!")

@kurisu.command(name='stats', help='Embeded bot stats.')
async def stats(ctx):
    serverCount = len(kurisu.guilds)
    memberCount = len(kurisu.get_all_members()) #len(set(kurisu.get_all_members())) unique members

    #\uFEFF is a blank space character, author.colour is highest role in server
    embed = discord.Embed(title=f'{kurisu.user.name} Stats', description='\uFEFF', colour=ctx.author.colour, timestamp=ctx.message.created_at)

    #defaults to inline = True
    embed.add_field(name='Bot Version:', value=kurisu.version)
    embed.add_field(name='Python Version:', value=pythonVersion)
    embed.add_field(name='Discord.Py Version', value=discordpyVersion)
    embed.add_field(name='Total Servers:', value=serverCount)
    embed.add_field(name='Total Members:', value=memberCount)
    embed.add_field(name='Bot Developer:', value="<@294325550330413056>")

    embed.set_footer(text=f"Steins;Gate | {kurisu.user.name}")
    embed.set_author(name=kurisu.user.name, icon_url=kurisu.user.avatar)

    await ctx.send(embed=embed)
    
@kurisu.command(name='echo', help="Repeats message")
async def _echo(ctx, *, message=None):
    message = message or "Please provide the message to be repeated."

    await ctx.message.delete()
    await ctx.send(message)

@kurisu.command(name='test', help="For Dev")
async def _test(ctx):

    randomImage = chooseRandomImage()

    file = discord.File(f"images/{randomImage}", filename=randomImage)
    embed = discord.Embed(title=f'Mommy', colour=ctx.author.colour, timestamp=ctx.message.created_at)
    embed.set_image(url=f"attachment://{randomImage}")
    await ctx.send(file=file, embed=embed)


@kurisu.command(name='logout', aliases=['disconnect', 'close', 'stopbot'], help='Disconnects bot')
@commands.is_owner()
async def _logout(ctx):
    await ctx.send(f"{ctx.author.mention} has requested the bot to be disconnected.")
    await kurisu.close()

#Runs bot
kurisu.run(kurisu.config_token)




