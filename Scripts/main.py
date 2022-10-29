import discord
from discord.ext import commands, tasks

from StringProgressBar import progressBar
from typing import Union
import requests
import asyncio

cryptocurrency = {
  "BTC": "<:BTC:1035598473074061403>", 
  "ETH":"<:ETH:1035600610784976967>",
  "USDT": "<:USDT:1035601040323649586>",
  "BNB": "<:BNB:1035601038620758137>",
  "USDC": "<:USDC:1035601593376190524>",
  "XRP": "<:XRP:1035601942438740058>", 
  "BUSD": "<:BUSD:1035602336296480819>",
  "ADA": "<:ADA:1035602963940511777>", 
  "SOL": "<:SOL:1035602960392134817>", 
  "DOGE": "<:DOGE:1035603924247400469>",
}

bot = commands.Bot(command_prefix='!',intents=discord.Intents.all())

@bot.event
async def on_ready():
  print(f"Hi my name is {bot.user.name}. I'm ready!")
  
@bot.event
async def on_message(message):
  if message.content.startswith('!cryptoprice'):
        
    total = 10
    current = 0

    bardata = progressBar.filledBar(total, current, size=30)

    embedloading = discord.Embed(title="Mike Bot | Loading...", description="\u200b", color=0x0000ff)

    embedloading.add_field(
      name=bardata[0], 
      value="\u200b", 
      inline=False
    )
    
    loadingmsg = await message.channel.send(embed=embedloading)

    cryptocurrencyprices = []

    for x in cryptocurrency.keys():
      link = f"https://www.binance.com/api/v3/ticker/price?symbol={x}USDT"
      response = requests.get(link)

      data = response.json()
      price = data.get("price")

      cryptocurrencyprices.append(price)

      current += 1
      
      bardata = progressBar.filledBar(total, current, size=30)

      embedloading = discord.Embed(title="Mike Bot | Loading...", description="\u200b", color=0x0000ff)

      embedloading.add_field(
        name=bardata[0], 
        value="\u200b", 
        inline=False
      )

      await loadingmsg.edit(embed = embedloading)

    embedcrypto = discord.Embed(title="Mike Bot | Cryptocurrencies Prices", description="This is actual price of cryptocurrencies", color=0x0000ff)

    embedcrypto.add_field(
      name="\u200b", 
      value=f"""
      {cryptocurrency["BTC"]} \u200b BITCOIN - {cryptocurrencyprices[0]}\n
      {cryptocurrency["ETH"]} \u200b ETHEREUM - {cryptocurrencyprices[1]}\n
      {cryptocurrency["USDT"]} \u200b TETHER - 1.00000000\n
      {cryptocurrency["BNB"]} \u200b BINANCE - {cryptocurrencyprices[3]}\n
      {cryptocurrency["USDC"]} \u200b USD COIN - {cryptocurrencyprices[4]}\n
      {cryptocurrency["XRP"]} \u200b XRP - {cryptocurrencyprices[5]}\n
      {cryptocurrency["BUSD"]} \u200b BINANCE USD - {cryptocurrencyprices[6]}\n
      {cryptocurrency["ADA"]} \u200b CARDANO - {cryptocurrencyprices[7]}\n
      {cryptocurrency["SOL"]} \u200b SOLANA - {cryptocurrencyprices[8]}\n
      {cryptocurrency["DOGE"]} \u200b DODGE COIN - {cryptocurrencyprices[9]}\n
      """, 
      inline=False
    )

    await loadingmsg.delete()
    
    await message.channel.send(embed=embedcrypto)

  if message.content.startswith('!cryptoconvert'):
    embedcrypto = discord.Embed(title="Mike Bot | Crypto Conversion", description="Choose the **FIRST** cryptocurrency to compare with another", color=0x0000ff)
    
    embedcrypto.add_field(
      name="\u200b", 
      value=f"""
      {cryptocurrency["BTC"]} \u200b BITCOIN\n
      {cryptocurrency["ETH"]} \u200b ETHEREUM \n
      {cryptocurrency["USDT"]} \u200b TETHER \n
      {cryptocurrency["BNB"]} \u200b BINANCE \n
      {cryptocurrency["USDC"]} \u200b USD COIN \n
      {cryptocurrency["XRP"]} \u200b XRP \n
      {cryptocurrency["BUSD"]} \u200b BINANCE USD \n
      {cryptocurrency["ADA"]} \u200b CARDANO \n
      {cryptocurrency["SOL"]} \u200b SOLANA \n
      {cryptocurrency["DOGE"]} \u200b DODGE COIN \n
      """, 
      inline=False
    )
    
    msg = await message.channel.send(embed=embedcrypto)

    loadingmsg = await message.channel.send("**Please wait for all reactions to appear...**")

    await msg.add_reaction(cryptocurrency["BTC"])
    await msg.add_reaction(cryptocurrency["ETH"])
    await msg.add_reaction(cryptocurrency["USDT"])
    await msg.add_reaction(cryptocurrency["BNB"])
    await msg.add_reaction(cryptocurrency["USDC"])
    await msg.add_reaction(cryptocurrency["XRP"])
    await msg.add_reaction(cryptocurrency["BUSD"])
    await msg.add_reaction(cryptocurrency["ADA"])
    await msg.add_reaction(cryptocurrency["SOL"])
    await msg.add_reaction(cryptocurrency["DOGE"])

    await loadingmsg.delete()

    def check(r: discord.Reaction, u: Union[discord.Member, discord.User]):
      BTC = "<:BTC:1035598473074061403>"
      ETH = "<:ETH:1035600610784976967>"
      USDT = "<:USDT:1035601040323649586>"
      BNB = "<:BNB:1035601038620758137>"
      USDC = "<:USDC:1035601593376190524>"
      XRP = "<:XRP:1035601942438740058>"
      BUSD = "<:BUSD:1035602336296480819>"
      ADA = "<:ADA:1035602963940511777>"
      SOL = "<:SOL:1035602960392134817>"
      DOGE = "<:DOGE:1035603924247400469>"
      
      return u.id == message.author.id and r.message.channel.id == message.channel.id and \
        str(r.emoji) in [BTC, ETH, USDT, BNB, USDC, XRP, BUSD, ADA, SOL,DOGE]

    reaction = ()

    try:
      reaction = await bot.wait_for('reaction_add', check = check, timeout = 60.0)
    except asyncio.TimeoutError:
      waittimeexceeded = discord.Embed(title="Mike Bot | Wait time exceeded", description=f"**{message.author}**, you didnt react in 60 seconds.", color=0x0000ff)

      await message.channel.send(embed=waittimeexceeded) 
    else:
      pass

    await msg.delete()

    if reaction:
      embedcrypto2 = discord.Embed(title="Mike Bot | Cryptos Conversion", description="Choose the **SECOND** cryptocurrency to compare with the first", color=0x0000ff)
      
      embedcrypto2.add_field(
        name="\u200b", 
        value=f"""
        {cryptocurrency["BTC"]} \u200b BITCOIN\n
        {cryptocurrency["ETH"]} \u200b ETHEREUM \n
        {cryptocurrency["USDT"]} \u200b TETHER \n
        {cryptocurrency["BNB"]} \u200b BINANCE \n
        {cryptocurrency["USDC"]} \u200b USD COIN \n
        {cryptocurrency["XRP"]} \u200b XRP \n
        {cryptocurrency["BUSD"]} \u200b BINANCE USD \n
        {cryptocurrency["ADA"]} \u200b CARDANO \n
        {cryptocurrency["SOL"]} \u200b SOLANA \n
        {cryptocurrency["DOGE"]} \u200b DODGE COIN \n
        """, 
        inline=False
      )
      
      msg = await message.channel.send(embed=embedcrypto2)

      BTC = "<:BTC:1035598473074061403>"
      ETH = "<:ETH:1035600610784976967>"
      USDT = "<:USDT:1035601040323649586>"
      BNB = "<:BNB:1035601038620758137>"
      USDC = "<:USDC:1035601593376190524>"
      XRP = "<:XRP:1035601942438740058>"
      BUSD = "<:BUSD:1035602336296480819>"
      ADA = "<:ADA:1035602963940511777>"
      SOL = "<:SOL:1035602960392134817>"
      DOGE = "<:DOGE:1035603924247400469>"

      loadingmsg2 = await message.channel.send("**Please wait for all reactions to appear...**")

      await msg.add_reaction(BTC)
      await msg.add_reaction(ETH)
      await msg.add_reaction(USDT)
      await msg.add_reaction(BNB)
      await msg.add_reaction(USDC)
      await msg.add_reaction(XRP)
      await msg.add_reaction(BUSD)
      await msg.add_reaction(ADA)
      await msg.add_reaction(SOL)
      await msg.add_reaction(DOGE)

      await loadingmsg2.delete()

      def check(r: discord.Reaction, u: Union[discord.Member, discord.User]):  # r = discord.Reaction, u = discord.Member or discord.User.
        return u.id == message.author.id and r.message.channel.id == message.channel.id and \
            str(r.emoji) in [BTC, ETH, USDT, BNB, USDC, XRP, BUSD, ADA, SOL,DOGE]

      try:
        reaction2 = await bot.wait_for('reaction_add', check = check, timeout = 60.0)
      except asyncio.TimeoutError:
        waittimeexceeded = discord.Embed(title="Mike Bot | Wait time exceeded", description=f"**{message.author}**, you didnt react in 60 seconds.", color=0x0000ff)

        await msg.delete()

        await message.channel.send(embed=waittimeexceeded) 
      else:
        pass

      link = f"https://www.binance.com/api/v3/ticker/price?symbol={reaction[0].emoji.name}{reaction2[0].emoji.name}"
      response = requests.get(link)

      data = response.json()
      price = data.get("price")

      embedcryptoconversion = discord.Embed(title="Mike Bot | Crypto Conversion Result", description=f"The result is the conversion from {cryptocurrency[reaction[0].emoji.name]} {reaction[0].emoji.name} to {cryptocurrency[reaction2[0].emoji.name]} {reaction2[0].emoji.name}", color=0x0000ff)
      
      if price:
        embedcryptoconversion.add_field(
          name="\u200b", 
          value=f"The result of conversion is {price}", 
          inline=False
        )
      else:
        embedcryptoconversion.add_field(
          name="\u200b", 
          value=f"The convertion is not possible!", 
          inline=False
        )

      await msg.delete()
      await message.channel.send(embed=embedcryptoconversion)
         
  else:
    await bot.process_commands(message)


bot.run("OTU4NzI1OTY5NDU0MTk4ODA1.Gtaq2R.0CIjnhLtIz7HBOTEYnELqN6sSN-AwQAmJV9uXQ")
