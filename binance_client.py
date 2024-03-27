import ccxt
from datetime import datetime
from exchange_client import ExchangeClient

class BinanceClient(ExchangeClient):
    def __init__(self, api_key, secret_key):
        self.api_key = api_key
        self.secret_key = secret_key

    def get_candlestick_data(self, symbol, interval, limit=100):
        binance_client = ccxt.binance({
            'apiKey': self.api_key,
            'secret': self.secret_key,
        })

        try:
            candlesticks = binance_client.fetch_ohlcv(symbol, interval, limit=limit)
            formatted_candlesticks = [{
                'timestamp': datetime.utcfromtimestamp(candlestick[0] / 1000.0).strftime('%Y-%m-%d %H:%M:%S'),
                'open': candlestick[1],
                'high': candlestick[2],
                'low': candlestick[3],
                'close': candlestick[4],
                'volume': candlestick[5]
            } for candlestick in candlesticks]
            return formatted_candlesticks
        except ccxt.NetworkError as e:
            print(f"Network error: {e}")
        except ccxt.ExchangeError as e:
            print(f"Exchange error: {e}")
        except Exception as e:
            print(f"Error: {e}")
