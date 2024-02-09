import discord
from discord.ext import commands


import cogs._json, cogs._functions



class nsfwCog(commands.Cog):
    def __init__(self, kurisu):
        self.kurisu = kurisu

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"NSFW Cog has been loaded\n{self.kurisu.lineBreak}")

    @commands.command(name='nhentai', help="6 digit number generator")
    @commands.is_nsfw()
    async def _nhentai(self, ctx):
        await ctx.send(f"https://nhentai.net/g/{cogs._functions.chooseSixDigitNumber()}/")

    @commands.command(name='rule34', aliases=['r34'], help="Horny dispenser")
    @commands.is_nsfw()
    async def _rule34(self, ctx):
        #await ctx.send(f"||{cogs._functions.getRandomR34()}||")
        pass
        


async def setup(kurisu):
    await kurisu.add_cog(nsfwCog(kurisu))