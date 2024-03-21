import requests
import json
import csv
from io import StringIO

def get_candlestick_data(base_currency, quote_currency, time_interval):
    url = "https://graphql.bitquery.io"

    query = f"""
    {{
      ethereum(network: ethereum) {{
        dexTrades(
          options: {{limit: 100000, asc: "timeInterval.minute"}}
          date: {{since: "2024-02-21"}}
          exchangeName: {{is: "Uniswap"}}
          baseCurrency: {{is: "{base_currency}"}}
          quoteCurrency: {{is: "{quote_currency}"}}
        ) {{
          timeInterval {{
            minute(count: {time_interval})
          }}
          baseCurrency {{
            symbol
            address
          }}
          baseAmount
          quoteCurrency {{
            symbol
            address
          }}
          quoteAmount
          trades: count
          quotePrice
          maximum_price: quotePrice(calculate: maximum)
          minimum_price: quotePrice(calculate: minimum)
          open_price: minimum(of: block, get: quote_price)
          close_price: maximum(of: block, get: quote_price)
        }}
      }}
    }}
    """

    payload = json.dumps({
        "query": query,
        "variables": "{}"
    })

    headers = {
        'Content-Type': 'application/json',
        'X-API-KEY': 'BQYTgWKfABe75fiX64pZhVWc41R4QPio',
        'Authorization': 'Bearer ory_at_9bJN9x4ERl4lcDON0irL68IxSY-fYblUStq9ANEw968.D1HcxxXj32f0ufjSjAQZTLTRtF-HZzKMBY7ZpNGcK2Q'
    }

    response = requests.post(url, headers=headers, data=payload)
    return response.json()['data']['ethereum']['dexTrades']

def export_to_csv(data, filename):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['time', 'pair', 'quoteAmount', 'open', 'high', 'low', 'close'])

        for trade in data:
            time = trade['timeInterval']['minute']
            pair = f"{trade['baseCurrency']['symbol']}/{trade['quoteCurrency']['symbol']}"
            quote_amount = trade['quoteAmount']
            open_price = trade['open_price']
            high_price = trade['maximum_price']
            low_price = trade['minimum_price']
            close_price = trade['close_price']

            writer.writerow([time, pair, quote_amount, open_price, high_price, low_price, close_price])

# Example usage:
base_currency = "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"
quote_currency = "0xdAC17F958D2ee523a2206206994597C13D831ec7"
time_interval = 5

result = get_candlestick_data(base_currency, quote_currency, time_interval)
export_to_csv(result, 'candlestick_data.csv')
