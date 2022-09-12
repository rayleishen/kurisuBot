import discord
from discord.ext import commands
import logging
from pathlib import Path
import json

#current working directory
cwd = str(Path(__file__).parents[0])
print(f"{cwd}\n-----")

#defining stuff
cmd_prefix = "k!"
secret_file = json.load(open(cwd+'/bot_config/secret.json'))
intents = discord.Intents.all()
kurisu = commands.Bot(command_prefix=cmd_prefix, case_insensitive=True, intents=intents)
kurisu.config_token = secret_file['token']
logging.basicConfig(level=logging.INFO)


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

    print(f"Running version {discord.__version__} of Discord.py\n-----\nLogged in as: {kurisu.user.name} : {kurisu.user.id}\n-----\nMy current prefix is {cmd_prefix}\n-----")
    print(f'{kurisu.user} is connected to the following guilds:')
    for guild in kurisu.guilds:
        print(f'{guild.name}(id: {guild.id})')

    await kurisu.change_presence(activity=discord.Activity(type=3, name=f" over {len(kurisu.guilds)} servers | Use {cmd_prefix}"))


#Bot commands
@kurisu.command(name='hello', aliases=['hi'], help='Says hello!')
async def _hello(ctx):
    await ctx.send(f"Hello {ctx.author.mention}!")
    #await ctx.send(f"Hi <@{ctx.author.id}>!")

@kurisu.command(name='echo', help="Repeats message")
async def _echo(ctx, *, message=None):
    message = message or "Please provide the message to be repeated."

    await ctx.message.delete()
    await ctx.send(message)

#Runs bot
kurisu.run(kurisu.config_token)




