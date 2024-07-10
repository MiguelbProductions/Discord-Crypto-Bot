import discord
import requests
import json

TOKEN = 'AAAA'

client = discord.Client()

@client.event
async def on_ready():
    print(f'Bot conectado como {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!preço'):
        await get_crypto_price(message)

async def get_crypto_price(message):
    try:
        # Substitua 'bitcoin' por outra criptomoeda, se desejar
        crypto = 'bitcoin'
        response = requests.get(f'https://api.coingecko.com/api/v3/simple/price?ids={crypto}&vs_currencies=usd')
        data = response.json()
        price = data[crypto]['usd']
        await message.channel.send(f'O preço atual do {crypto} é ${price:.2f} USD')
    except Exception as e:
        await message.channel.send('Erro ao buscar o preço da criptomoeda.')
        print(e)

client.run(TOKEN)
