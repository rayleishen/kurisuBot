import discord
from discord.ext import commands
import logging, json, platform, os, asyncio
from pathlib import Path



# Current working directory
cwd = str(Path(__file__).parents[0])

# Defining stuff
cmd_prefix = "k!" #cmd_prefix = ["k!", "K!"]
secret_file = json.load(open(cwd+'/bot_config/secret.json'))
intents = discord.Intents.all()
kurisu = commands.Bot(command_prefix=["k!", "K!"], case_insensitive=True, intents=intents, owner_id=294325550330413056) #note the prefix
kurisu.config_token = secret_file['token']
logging.basicConfig(level=logging.INFO)

kurisu.blacklisted_users = []
kurisu.cwd = cwd
kurisu.pythonVersion = platform.python_version()
kurisu.discordpyVersion = discord.__version__
kurisu.version = '3.0.0'
kurisu.lineBreak = "~~~~~~~~~~~~~~~~~~~~"

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
kurisu.colour_list = [c for c in kurisu.colors.values()]


# Bot loading
print(f"{kurisu.lineBreak * 4}\n{kurisu.lineBreak * 4}\n{cwd}\n{kurisu.lineBreak}")

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
    
    print(f"Running version {kurisu.discordpyVersion} of Discord.py\n{kurisu.lineBreak}\nLogged in as: {kurisu.user.name} : {kurisu.user.id}\n{kurisu.lineBreak}\nMy current prefix is {cmd_prefix}\n{kurisu.lineBreak}")
    print(f'{kurisu.user} is connected to the following guilds:')
    for guild in kurisu.guilds:
        print(f'{guild.name}(id: {guild.id})')
    print(kurisu.lineBreak)

    await kurisu.change_presence(activity=discord.Activity(type=3, name=f" over {len(kurisu.guilds)} servers | Use {cmd_prefix}"))


# Blacklist handler
@kurisu.event
async def on_message(message):
    # Ignore ourselves
    if message.author.id == kurisu.user.id:
        return

    #blacklist system
    if message.author.id in kurisu.blacklisted_users:
        return

    if message.content.lower().startswith("help"):
        await message.channel.send("Hey! Why don't you run the help command with `k!help`")

    await kurisu.process_commands(message)


# Doing cool cog things
if __name__ == '__main__':
    # When running this file as the 'main' file
    # Not being imported by another python file


    async def load_extensions():
        for file in os.listdir(f"{cwd}/cogs"):
            if file.endswith(".py") and not file.startswith("_"):
                await kurisu.load_extension(f"cogs.{file[:-3]}")

    async def main():
        async with kurisu:
            # Loads events and orders
            await load_extensions()

            # Runs bot
            await kurisu.start(kurisu.config_token)

    asyncio.run(main()) 
    
#kurisu.run(kurisu.config_token)
