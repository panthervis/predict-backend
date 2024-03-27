from binance_client import BinanceClient
from uniswap_client import UniswapClient

def create_exchange_client(exchange_type, api_key, secret_key):
    if exchange_type == 'binance':
        return BinanceClient(api_key, secret_key)
    elif exchange_type == 'uniswap':
        return UniswapClient(api_key, secret_key)
    else:
        raise ValueError("Invalid exchange type")
