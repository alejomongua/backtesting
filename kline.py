class Kline():
    """
    Main class where candle data is stored
    """

    def __init__(self, symbol: str, candle_data):
        """
        https://github.com/binance/binance-spot-api-docs/blob/master/rest-api.md#klinecandlestick-data

        symbol is the string than represents the pair

        Acording to API documentation, each candle consist of this data
        candle_data = [
                1499040000000,      // Open time
                "0.01634790",       // Open
                "0.80000000",       // High
                "0.01575800",       // Low
                "0.01577100",       // Close
                "148976.11427815",  // Volume
                1499644799999,      // Close time
                "2434.19055334",    // Quote asset volume
                308,                // Number of trades
                "1756.87402397",    // Taker buy base asset volume
                "28.46694368",      // Taker buy quote asset volume
                "17928899.62484339" // Ignore.
            ]
        """
        if len(candle_data) < 11:
            raise 'Kline data incorrect'

        self.symbol = symbol
        self.open_time = candle_data[0] / 1000
        self.open_price = float(candle_data[1])
        self.highest_price = float(candle_data[2])
        self.lowest_price = float(candle_data[3])
        self.close_price = float(candle_data[4])
        self.volume = float(candle_data[5])
        self.close_time = float(candle_data[6])
        self.quote_asset_volume = float(candle_data[7])
        self.number_of_trades = candle_data[8]
        self.taker_buy_base_asset_volume = float(candle_data[9])
        self.taker_buy_quote_asset_volume = float(candle_data[10])

    def to_dict(self):
        return {
            'symbol': self.symbol,
            'open_time': self.open_time,
            'open_price': self.open_price,
            'highest_price': self.highest_price,
            'lowest_price': self.lowest_price,
            'close_price': self.close_price,
            'volume': self.volume,
            'close_time': self.close_time,
            'quote_asset_volume': self.quote_asset_volume,
            'number_of_trades': self.number_of_trades,
            'taker_buy_base_asset_volume': self.taker_buy_base_asset_volume,
            'taker_buy_quote_asset_volume': self.taker_buy_quote_asset_volume,
        }
