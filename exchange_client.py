import abc

class ExchangeClient(abc.ABC):
    @abc.abstractmethod
    def get_candlestick_data(self, base_currency, quote_currency, time_interval):
        pass
