from discord.ext import tasks
from src.utils import get_price_data

def setup_tasks(bot):
    @tasks.loop(minutes=10)
    async def update_market_data():
        for coin, alerts in bot.price_alerts.items():
            data = get_price_data(coin, 'usd')
            if data and coin in data:
                price = data[coin]['usd']
                for alert in alerts:
                    if (alert['type'] == 'above' and price > alert['price']) or (alert['type'] == 'below' and price < alert['price']):
                        user = bot.get_user(alert['user_id'])
                        if user:
                            await user.send(f'Price alert: {coin.capitalize()} is now {alert["type"]} ${alert["price"]}. Current price: ${price}')
                            alerts.remove(alert)
