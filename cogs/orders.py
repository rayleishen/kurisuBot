import discord
from discord.ext import commands
import platform

import cogs._json, cogs._functions


class OrdersCog(commands.Cog):
    def __init__(self, kurisu):
        self.kurisu = kurisu

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"Orders Cog has been loaded\n{self.kurisu.lineBreak}")

    # Bot commands
    @commands.command(name='hello', aliases=['hi'], help='Says hello!')
    async def _hello(self, ctx): #ctx: commands.Context
        await ctx.send(f"Hello {ctx.author.mention}!")
        #await ctx.send(f"Hi <@{ctx.author.id}>!")  

    @commands.command(name='stats', help='Embeded bot stats.')
    async def _stats(self, ctx):
        serverCount = len(self.kurisu.guilds)
        memberCount = len(self.kurisu.get_all_members()) # len(set(kurisu.get_all_members())) unique members

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

    @commands.command(name='ping', help='Latency test')
    async def ping(self, ctx): # This was inside '__init__' before
        await ctx.send(f'pong!\n{round(self.client.latency * 1000)}ms')

    @commands.command(name='logout', aliases=['disconnect', 'close', 'stopbot'], help='Disconnects bot')
    @commands.is_owner()
    async def _logout(self, ctx):
        await ctx.send(f"{ctx.author.mention} has requested the bot to be disconnected.")
        await self.kurisu.close()

    # Blacklist manager
    @commands.command()
    @commands.is_owner()
    async def blacklist(self, ctx, user: discord.Member):
        if ctx.message.author.id == user.id:
            await ctx.send("You cannot blacklist yourself!")
            return

        self.kurisu.blacklisted_users.append(user.id)
        data = cogs._json.read_json("blacklist")
        data["blacklistedUsers"].append(user.id)
        cogs._json.write_json(data, "blacklist")
        await ctx.send(f"{user.name} has been blacklisted.")

    @commands.command()
    @commands.is_owner()
    async def unblacklist(self, ctx, user: discord.Member):
        self.kurisu.blacklisted_users.remove(user.id)
        data = cogs._json.read_json("blacklist")
        data["blacklistedUsers"].remove(user.id)
        cogs._json.write_json(data, "blacklist")
        await ctx.send(f"{user.name} has been unblacklisted.")


    # General commands
    @commands.command(name='echo', help="Repeats message")
    async def _echo(self, ctx, *, message=None):
        message = message or "Please provide the message to be repeated."

        await ctx.message.delete()
        await ctx.send(message)



    # Dev work commands
    @commands.command(name='test', help="For Dev")
    async def _test(self, ctx):

        randomImage = cogs._functions.chooseRandomImage()

        file = discord.File(f"images/{randomImage}", filename=randomImage)
        embed = discord.Embed(title=f'Mommy', colour=ctx.author.colour, timestamp=ctx.message.created_at)
        embed.set_image(url=f"attachment://{randomImage}")
        await ctx.send(file=file, embed=embed)


async def setup(kurisu):
    await kurisu.add_cog(OrdersCog(kurisu))