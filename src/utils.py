import requests
import matplotlib.pyplot as plt
import io
import datetime

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

def get_market_trends():
    url = 'https://api.coingecko.com/api/v3/search/trending'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def convert_crypto(amount, from_coin, to_coin):
    url = f'https://api.coingecko.com/api/v3/simple/price?ids={from_coin},{to_coin}&vs_currencies=usd'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if from_coin in data and to_coin in data:
            from_price = data[from_coin]['usd']
            to_price = data[to_coin]['usd']
            converted_amount = (amount * from_price) / to_price
            return converted_amount
        else:
            return None
    else:
        return None

def get_crypto_news():
    url = 'https://newsapi.org/v2/everything?q=cryptocurrency&apiKey=215b97a0439a4d049379244731b97f18'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data['articles']
    else:
        return None

def get_wallet_info(wallet_address):
    url = f'https://api.etherscan.io/api?module=account&action=balance&address={wallet_address}&tag=latest&apikey=USDM5S9RP1ZMYUBXIRZJ9HJCRB9KYA9PZI'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data['status'] == '1':
            balance = int(data['result']) / 10**18
            transactions_url = f'https://api.etherscan.io/api?module=account&action=txlist&address={wallet_address}&startblock=0&endblock=99999999&sort=asc&apikey=USDM5S9RP1ZMYUBXIRZJ9HJCRB9KYA9PZI'
            transactions_response = requests.get(transactions_url)
            if transactions_response.status_code == 200:
                transactions_data = transactions_response.json()
                if transactions_data['status'] == '1':
                    return {
                        'balance': balance,
                        'transactions': len(transactions_data['result'])
                    }
                else:
                    return None
            else:
                return None
        else:
            return None
    else:
        return None

def get_daily_highlights():
    url = 'https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=100&page=1'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        top_gainers = sorted(data, key=lambda x: x['price_change_percentage_24h'], reverse=True)[:5]
        top_losers = sorted(data, key=lambda x: x['price_change_percentage_24h'])[:5]
        return {'gainers': top_gainers, 'losers': top_losers}
    else:
        return None

def get_translation(text, target_language):
    url = f'https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl={target_language}&dt=t&q={text}'
    response = requests.get(url)
    if response.status_code == 200:
        translated_text = response.json()[0][0][0]
        return translated_text
    else:
        return None
