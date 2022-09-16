import discord
from discord.ext import commands


import cogs._json, cogs._functions


class ownerCog(commands.Cog):
    def __init__(self, kurisu):
        self.kurisu = kurisu

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"Owner Cog has been loaded\n{self.kurisu.lineBreak}")

    # Force logout
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


    @commands.command(name='dm', help='DM sliding')
    async def _dm(self, ctx, member:discord.Member, *, content):
        await member.send(content)

    @commands.command(name='giverole', aliases=['addrole'], help='Gives role') #pass_context=True
    @commands.is_owner()
    async def _giverole(self, ctx, user: discord.Member, role: discord.Role):
        await user.add_roles(role)
        await ctx.send(f"Hey {ctx.author.name}, {user.name} has been giving a role called: {role.name}")


    @commands.command(name='rr', help="Reaction roles")
    @commands.is_owner()
    async def _reactionRoles(self, ctx, role: discord.Role, emoji):

        @commands.Cog.listener() #I WANNA ADD MULTIPLE EMOJIES ON A MESSAGE
        async def on_reaction_add(self, reaction, user):
            await user.add_roles(role)
            await user.send(f"{user.name} has been giving a role called: {role.name}")

    # Dev work commands
    @commands.command(name='test', help="For Dev")
    async def _test(self, ctx):

        randomImage = cogs._functions.chooseRandomImage()

        file = discord.File(f"images/{randomImage}", filename=randomImage)
        embed = discord.Embed(title=f'Mommy', colour=ctx.author.colour, timestamp=ctx.message.created_at)
        embed.set_image(url=f"attachment://{randomImage}")
        await ctx.send(file=file, embed=embed)


async def setup(kurisu):
    await kurisu.add_cog(ownerCog(kurisu))