import discord, requests, json
from discord.ext import commands

import cogs._json, cogs._functions

# Main Commands Cog
class ordersCog(commands.Cog):
    def __init__(self, kurisu):
        self.kurisu = kurisu

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"Orders Cog has been loaded\n{self.kurisu.lineBreak}")

    # Hello command
    @commands.command(name='hello', aliases=['hi'], help='Says hello!')
    async def _hello(self, ctx): #ctx: commands.Context
        await ctx.send(f"Hello {ctx.author.mention}!")
        #await ctx.send(f"Hi <@{ctx.author.id}>!")  

    # Stats command
    @commands.command(name='stats', help='Embeded bot stats.')
    async def _stats(self, ctx):
        serverCount = len(self.kurisu.guilds)
        memberCount = len(set(self.kurisu.get_all_members()))

        # \uFEFF is a blank space character, author.colour is highest role in server
        embed = discord.Embed(title=f'{self.kurisu.user.name} Stats', description='\uFEFF', colour=ctx.author.colour, timestamp=ctx.message.created_at)

        # defaults to inline = True
        embed.add_field(name='Bot Version:', value=self.kurisu.version)
        embed.add_field(name='Python Version:', value=self.kurisu.pythonVersion)
        embed.add_field(name='Discord.Py Version', value=self.kurisu.discordpyVersion)
        embed.add_field(name='Total Servers:', value=serverCount)
        embed.add_field(name='Total Members:', value=memberCount)
        embed.add_field(name='Bot Developer:', value="<@294325550330413056>")

        embed.set_footer(text=f"Steins;Gate | {self.kurisu.user.name}")
        embed.set_author(name=self.kurisu.user.name, icon_url=self.kurisu.user.avatar)

        await ctx.send(embed=embed)

    # Ping command
    @commands.command(name='ping', help='Latency test')
    async def ping(self, ctx): # This was inside '__init__' before
        await ctx.send(f'pong!: {round(self.kurisu.latency * 1000)}ms')

    # General commands
    @commands.command(name='echo', help="Repeats message")
    async def _echo(self, ctx, *, message=None):
        message = message or "Please provide the message to be repeated."

        await ctx.message.delete()
        await ctx.send(message)

    @commands.command(name='quote', help='Inspiration')
    async def _quote(self, ctx):
        response = requests.get("https://zenquotes.io/api/random")
        json_data = json.loads(response.text)
        quote = json_data[0]['q'] + " -" + json_data[0]['a']
        await ctx.send(quote)

    @commands.command(name='coinflip', aliases=['flipcoin'], help="Heads or tails")
    async def _coin(self, ctx):
        await ctx.send(cogs._functions.getCoinFlip())

    @commands.command(name='rolldice', aliases=['diceroll'], help="randint(1, 6)")
    async def _dice(self, ctx):
        await ctx.send(str(cogs._functions.getDiceRoll()))

    @commands.command(name='joe', help="joe")
    async def _joe(self, ctx):
        await ctx.send("Hello <@234121525521940480>!")

    @commands.command(name='join')
    async def _join(self, ctx):
        channel = ctx.author.voice.channel
        await channel.connect()

    @commands.command(name='leave')
    async def _leave(self, ctx):
        await ctx.voice_client.disconnect()

    @commands.command(name='say', help="Repeats message")
    async def say(self, ctx, *args):
        await ctx.send("{}".format(" ".join(args)))


async def setup(kurisu):
    await kurisu.add_cog(ordersCog(kurisu))