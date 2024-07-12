import discord
from discord import app_commands
from discord.ext import commands
from src.utils import *

def setup_commands(bot: commands.Bot):
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

    @bot.tree.command(name="trending", description="Get the current trending cryptocurrencies")
    async def trending(interaction: discord.Interaction):
        await interaction.response.defer()
        data = get_market_trends()
        if data:
            coins = data['coins']
            embed = discord.Embed(title='Trending Cryptocurrencies', color=discord.Color.purple())
            for coin in coins:
                item = coin['item']
                embed.add_field(name=item['name'], value=f"Symbol: {item['symbol']}\nMarket Cap Rank: {item['market_cap_rank']}", inline=False)
            await interaction.followup.send(embed=embed)
        else:
            await interaction.followup.send('Error fetching trending cryptocurrencies.')

    @bot.tree.command(name="convert", description="Convert an amount from one cryptocurrency to another")
    @app_commands.describe(amount="The amount to convert", from_coin="The cryptocurrency to convert from", to_coin="The cryptocurrency to convert to")
    async def convert(interaction: discord.Interaction, amount: float, from_coin: str, to_coin: str):
        await interaction.response.defer()
        converted_amount = convert_crypto(amount, from_coin, to_coin)
        if converted_amount:
            embed = discord.Embed(title='Crypto Conversion', color=discord.Color.orange())
            embed.add_field(name='From', value=f'{amount} {from_coin.upper()}', inline=False)
            embed.add_field(name='To', value=f'{converted_amount:.6f} {to_coin.upper()}', inline=False)
            await interaction.followup.send(embed=embed)
        else:
            await interaction.followup.send('Error converting cryptocurrencies.')

    @bot.tree.command(name="alert", description="Set a price alert for a cryptocurrency")
    @app_commands.describe(coin="The cryptocurrency you want to set an alert for", price="The price to trigger the alert", alert_type="above or below the price")
    async def alert(interaction: discord.Interaction, coin: str, price: float, alert_type: str):
        if alert_type.lower() not in ['above', 'below']:
            await interaction.response.send_message('Alert type must be either "above" or "below".', ephemeral=True)
            return

        bot.price_alerts[coin].append({'user_id': interaction.user.id, 'price': price, 'type': alert_type.lower()})
        await interaction.response.send_message(f'Alert set for {coin.capitalize()} at ${price} {alert_type} the price.', ephemeral=True)

    # Auto-complete function for coin names
    @price.autocomplete('coin')
    @info.autocomplete('coin')
    @chart.autocomplete('coin')
    @convert.autocomplete('from_coin')
    @convert.autocomplete('to_coin')
    @alert.autocomplete('coin')
    async def coin_autocomplete(interaction: discord.Interaction, current: str):
        return [
            app_commands.Choice(name=coin['name'], value=coin['id'])
            for coin in bot.coins if current.lower() in coin['name'].lower()
        ][:25]
