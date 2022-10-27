import discord
from discord.ext import commands

bot = commands.Bot(command_prefix='!',intents=discord.Intents.all())

@bot.event
async def on_ready():
  print(f"Hi my name is {bot.user.name}. I'm ready!")
  
@bot.command(name="hi")
async def send_hi(ctx):
    name = ctx.author.name

    await ctx.send(f"Hi {name}!")

@bot.command(name="helpme")
async def send_help(ctx):
    await ctx.send("""List of commands:
    - help""")

bot.run("OTU4NzI1OTY5NDU0MTk4ODA1.G7vpzY.7NVdp0__maj78j8dutHDvH0cfVAVzhhNMIfLn8")
