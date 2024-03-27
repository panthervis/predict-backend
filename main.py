from exchange_client_factory import create_exchange_client
from csv_exporter import export_to_csv


# Example usage
api_key_binance = 'uuaSIO0YJkUa6aPxusijUh4AxNwlKpDKOuOZEJdRIHsHEiUUA0JpYICDS3ySoQTh'
secret_key_binance = '6OIKo6fTbDX9rU1RQrswjbp8376jGVmbm2O5xUbHpQA14faJQYXDqlrQPhCiALtk'
api_key_uniswap = 'BQYTgWKfABe75fiX64pZhVWc41R4QPio'
secret_key_uniswap = 'ory_at_9bJN9x4ERl4lcDON0irL68IxSY-fYblUStq9ANEw968.D1HcxxXj32f0ufjSjAQZTLTRtF-HZzKMBY7ZpNGcK2Q'

# Create Binance client
binance_client = create_exchange_client('binance', api_key_binance, secret_key_binance)
symbol_binance = 'BTCUSDT'
interval_binance = '1h'
candlestick_data_binance = binance_client.get_candlestick_data(symbol_binance, interval_binance)

# Export to CSV
export_to_csv(candlestick_data_binance, f'{symbol_binance}_candlesticks_binance.csv')

# Create Uniswap client
uniswap_client = create_exchange_client('uniswap', api_key_uniswap, secret_key_uniswap)
base_currency_uniswap = "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"
quote_currency_uniswap = "0xdAC17F958D2ee523a2206206994597C13D831ec7"
time_interval_uniswap = 5
candlestick_data_uniswap = uniswap_client.get_candlestick_data(base_currency_uniswap, quote_currency_uniswap, time_interval_uniswap)

# Export to CSV
export_to_csv(candlestick_data_uniswap, 'candlestick_data_uniswap.csv')
