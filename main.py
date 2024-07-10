import discord
from discord import app_commands
from discord.ext import commands
import requests
import matplotlib.pyplot as plt
import io
import datetime
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True

class CryptoBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=intents)
        self.synced = False
        self.coins = []

    async def setup_hook(self):
        await self.tree.sync()

    async def on_ready(self):
        await self.sync_coins()
        print(f'Bot connected as {self.user}')
        if not self.synced:
            await self.tree.sync()
            self.synced = True
        print("Slash commands synced")

    async def sync_coins(self):
        url = 'https://api.coingecko.com/api/v3/coins/list'
        response = requests.get(url)
        if response.status_code == 200:
            self.coins = response.json()
        else:
            print("Failed to fetch coin list")

bot = CryptoBot()

def get_price_data(coin, currency):
    url = f'https://api.coingecko.com/api/v3/simple/price?ids={coin}&vs_currencies={currency}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def get_detailed_data(coin):
    url = f'https://api.coingecko.com/api/v3/coins/{coin}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def get_top_coins():
    url = 'https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=10&page=1'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def create_price_chart(prices, coin):
    dates = [datetime.datetime.fromtimestamp(ts/1000) for ts in prices['dates']]
    values = prices['values']

    plt.figure(figsize=(12, 6))
    plt.plot(dates, values, color='b')

    plt.title(f'{coin.capitalize()} Price in the Last 30 Days')
    plt.xlabel('Date')
    plt.ylabel('Price (USD)')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()
    return buf

@bot.tree.command(name="price", description="Get the price of a cryptocurrency")
@app_commands.describe(coin="The cryptocurrency you want to check", currency="The currency to compare (default is USD)")
async def price(interaction: discord.Interaction, coin: str, currency: str = 'usd'):
    await interaction.response.defer()
    data = get_price_data(coin, currency)
    if data and coin in data:
        if currency in data[coin]:
            price = data[coin][currency]
            embed = discord.Embed(title=f'{coin.capitalize()} Price', color=discord.Color.blue())
            embed.add_field(name='Price', value=f'{price} {currency.upper()}', inline=False)
            await interaction.followup.send(embed=embed)
        else:
            await interaction.followup.send(f'Currency {currency} not found for {coin}.')
    else:
        await interaction.followup.send('Cryptocurrency or currency not found.')

@bot.tree.command(name="info", description="Get detailed information about a cryptocurrency")
@app_commands.describe(coin="The cryptocurrency you want to check")
async def info(interaction: discord.Interaction, coin: str):
    await interaction.response.defer()
    data = get_detailed_data(coin)
    if data:
        name = data['name']
        description = data['description']['en'][:200]
        market_cap = data['market_data']['market_cap']['usd']
        volume = data['market_data']['total_volume']['usd']
        embed = discord.Embed(title=name, description=description, color=discord.Color.green())
        embed.add_field(name='Market Cap', value=f'${market_cap:,}', inline=False)
        embed.add_field(name='Total Volume', value=f'${volume:,}', inline=False)
        await interaction.followup.send(embed=embed)
    else:
        await interaction.followup.send('Cryptocurrency not found.')

@bot.tree.command(name="top", description="Get the top 10 cryptocurrencies by market cap")
async def top(interaction: discord.Interaction):
    await interaction.response.defer()
    data = get_top_coins()
    if data:
        embed = discord.Embed(title='Top 10 Cryptocurrencies', color=discord.Color.gold())
        for coin in data:
            embed.add_field(name=coin['name'], value=f"Price: ${coin['current_price']:,}\nMarket Cap: ${coin['market_cap']:,}", inline=False)
        await interaction.followup.send(embed=embed)
    else:
        await interaction.followup.send('Error fetching top cryptocurrencies data.')

@bot.tree.command(name="chart", description="Get the price chart of a cryptocurrency for the last 30 days")
@app_commands.describe(coin="The cryptocurrency you want to check")
async def chart(interaction: discord.Interaction, coin: str):
    await interaction.response.defer()
    url = f'https://api.coingecko.com/api/v3/coins/{coin}/market_chart?vs_currency=usd&days=30'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        prices = {
            'dates': [x[0] for x in data['prices']],
            'values': [x[1] for x in data['prices']]
        }
        buf = create_price_chart(prices, coin)
        file = discord.File(buf, filename=f'{coin}_price_chart.png')
        await interaction.followup.send(file=file)
    else:
        await interaction.followup.send('Error fetching data for the chart.')

# Auto-complete function for coin names
@price.autocomplete('coin')
@info.autocomplete('coin')
@chart.autocomplete('coin')
async def coin_autocomplete(interaction: discord.Interaction, current: str):
    return [
        app_commands.Choice(name=coin['name'], value=coin['id'])
        for coin in bot.coins if current.lower() in coin['name'].lower()
    ][:25]

bot.run(TOKEN)
