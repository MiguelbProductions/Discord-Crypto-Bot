import discord
from discord.ext import commands, tasks
import os
import requests
from dotenv import load_dotenv
from src.commands import setup_commands
from src.tasks import setup_tasks
from collections import defaultdict
from src.utils import get_price_data, get_translation

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True

class CryptoBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=intents)
        self.synced = False
        self.coins = []
        self.price_alerts = defaultdict(list)
        self.favorites = defaultdict(list)

    async def setup_hook(self):
        await self.tree.sync()
        setup_tasks(self)
        self.update_market_data.start()

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

    async def on_message(self, message):
        if message.author == self.user:
            return

        if 'crypto' in message.content.lower():
            await message.channel.send('Interested in cryptocurrencies? Use `/price` to get the latest prices!')

        await self.process_commands(message)

    @tasks.loop(minutes=10)
    async def update_market_data(self):
        for coin, alerts in self.price_alerts.items():
            data = get_price_data(coin, 'usd')
            if data and coin in data:
                price = data[coin]['usd']
                for alert in alerts:
                    if (alert['type'] == 'above' and price > alert['price']) or (alert['type'] == 'below' and price < alert['price']):
                        user = self.get_user(alert['user_id'])
                        if user:
                            await user.send(f'Price alert: {coin.capitalize()} is now {alert["type"]} ${alert["price"]}. Current price: ${price}')
                            alerts.remove(alert)

bot = CryptoBot()
setup_commands(bot)
bot.run(TOKEN)
