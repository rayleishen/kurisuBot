import discord, random, datetime
from discord.ext import commands


class eventsCog(commands.Cog):
    def __init__(self, kurisu):
        self.kurisu = kurisu

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"Events Cog has been loaded\n{self.kurisu.lineBreak}")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        # On member joins we find a channel called general and if it exists,
        # send an embed welcoming them to our guild
        channel = discord.utils.get(member.guild.text_channels, name='general')
        if channel:
            embed = discord.Embed(description='Welcome to our server!', color=random.choice(self.kurisu.colour_list))
            embed.set_thumbnail(url=member.avatar.url)
            embed.set_author(name=member.name, icon_url=member.avatar.url)
            embed.set_footer(text=member.guild, icon_url=member.guild.icon.url)
            embed.timestamp = datetime.datetime.utcnow()

            await channel.send(embed=embed)

        await member.create_dm()
        await member.dm_channel.send(f"Hi {member.name}, welcome to {member.guild.name}!")

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        # On member remove we find a channel called general and if it exists,
        # send an embed saying goodbye from our guild-
        channel = discord.utils.get(member.guild.text_channels, name='general')
        if channel:
            embed = discord.Embed(description='Goodbye from all of us..', color=random.choice(self.kurisu.colour_list))
            embed.set_thumbnail(url=member.avatar.url)
            embed.set_author(name=member.name, icon_url=member.avatar.url)
            embed.set_footer(text=member.guild, icon_url=member.guild.icon.url)
            embed.timestamp = datetime.datetime.utcnow()

            await channel.send(embed=embed)

        #await member.create_dm()
        #await member.dm_channel.send(f"Goodbye {member.name}, sorry to see you leave {member.guild.name}!")

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        #Ignore these errors
        ignored = (commands.CommandNotFound, commands.UserInputError)
        if isinstance(error, ignored):
            return

        if isinstance(error, commands.CommandOnCooldown):
            # If the command is currently on cooldown trip this
            m, s = divmod(error.retry_after, 60)
            h, m = divmod(m, 60)
            if int(h) == 0 and int(m) == 0:
                await ctx.send(f' You must wait {int(s)} seconds to use this command!')
            elif int(h) == 0 and int(m) != 0:
                await ctx.send(f' You must wait {int(m)} minutes and {int(s)} seconds to use this command!')
            else:
                await ctx.send(f' You must wait {int(h)} hours, {int(m)} minutes and {int(s)} seconds to use this command!')
        elif isinstance(error, commands.CheckFailure):
            # If the command has failed a check, trip this
            await ctx.send("Hey! You lack permission to use this command.")
        raise error


    @commands.Cog.listener()
    async def on_message(self, message):
        if "cool" in message.content:
            await message.add_reaction('\U0001F60E')#Unicode to python: '+' becomes '000' and "\" before "U"

    @commands.Cog.listener()
    async def on_message(self, message):
        if "lmfao" in message.content:
            await message.add_reaction('\U0001F923')

    @commands.Cog.listener()
    async def on_message(self, message):
        if "lol" in message.content:
            await message.add_reaction('\U0001F604')
    

async def setup(kurisu):
    await kurisu.add_cog(eventsCog(kurisu))