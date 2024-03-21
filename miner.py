
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import tensorflow as tf
from data.uniswap.uniswap import get_candlestick_data

class Miner:
    def __init__(self, base_currency, quote_currency, time_interval):
        self.base_currency = base_currency
        self.quote_currency = quote_currency
        self.time_interval = time_interval
        self.model = None
        self.scaler = None
        self.model_dir = 'model.h5'
    
    def fetch_data(self):
        
        candlestick_data = get_candlestick_data(self.base_currency, self.quote_currency, self.time_interval)
        return candlestick_data
    
    def extract_open_price_and_volume(self, data):
        open_prices = []
        volumes = []
        prep_data =[]
        for trade in data:
            open_prices.append(trade['open_price'])
            volumes.append(trade['quoteAmount'])
        prep_data.append(open_prices)
        prep_data.append(volumes)

        return prep_data

    def scale_data(self, prep_data):
        
        prep_data = np.array(prep_data)
        prep_data = prep_data.T

        prep_data = prep_data[-50:,:]
        
        self.scaler = MinMaxScaler()
        scaled_data = self.scaler.fit_transform(prep_data)

        return scaled_data

    def load_model(self, model_path):
        
        self.model = tf.keras.models.load_model(self.model_dir)

    def predict(self):
        if self.model is None:
            self.load_model(self.model_dir)

       
        candlestick_data = self.fetch_data()
        prep_data = self.extract_open_price_and_volume(candlestick_data)
       
        scaled_data = self.scale_data(prep_data)
        last_element = prep_data[0][-1]
        
        print(last_element)
        print(scaled_data.shape)

        scaled_data = np.expand_dims(scaled_data, axis=0)
        prediction = self.model.predict(scaled_data)

        prediction = float(prediction[0])
        last_element = float(last_element)
        print(type(prediction))
        print(type(last_element))
        predicted_price = prediction * last_element

        return predicted_price



base_currency = "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"
quote_currency = "0xdAC17F958D2ee523a2206206994597C13D831ec7"
time_interval = 60
model_path = 'model_communeV1.h5'

miner = Miner(base_currency, quote_currency, time_interval)


prediction = miner.predict()
print("Prix prédit :", prediction)

