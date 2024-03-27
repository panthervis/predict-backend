import csv

def export_to_csv(data, filename):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['time', 'pair', 'quoteAmount', 'open', 'high', 'low', 'close'])

        for candlestick in data:
            time = candlestick['timestamp']
            pair = f"{candlestick['baseCurrency']['symbol']}/{candlestick['quoteCurrency']['symbol']}" if 'baseCurrency' in candlestick else 'UNI/USDT'
            quote_amount = candlestick['quoteAmount'] if 'quoteAmount' in candlestick else candlestick['volume']
            open_price = candlestick['open']
            high_price = candlestick['high']
            low_price = candlestick['low']
            close_price = candlestick['close']

            writer.writerow([time, pair, quote_amount, open_price, high_price, low_price, close_price])
