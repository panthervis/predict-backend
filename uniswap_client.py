import requests
import json
from datetime import datetime
from exchange_client import ExchangeClient

class UniswapClient(ExchangeClient):
    def __init__(self, api_key, secret_key):
        self.api_key = api_key
        self.secret_key = secret_key

    def get_candlestick_data(self, base_currency, quote_currency, time_interval):
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
            'X-API-KEY': self.api_key,
            'Authorization': f'Bearer {self.secret_key}'
        }

        response = requests.post(url, headers=headers, data=payload)
        data = response.json()['data']['ethereum']['dexTrades']

        formatted_candlesticks = [{
            'timestamp': datetime.strptime(trade['timeInterval']['minute'], '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S'),
            'open': trade['open_price'],
            'high': trade['maximum_price'],
            'low': trade['minimum_price'],
            'close': trade['close_price'],
            'volume': trade['quoteAmount']
        } for trade in data]

        return formatted_candlesticks
