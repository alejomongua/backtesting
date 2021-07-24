from sqlalchemy import Column, Integer, String, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class Kline(Base):
    __tablename__ = 'klines'

    id = Column(Integer(), primary_key=True)
    symbol = Column(String(20), nullable=False, index=True)
    open_time = Column(DateTime(), nullable=False, index=True)
    open_price = Column(Float(), nullable=False)
    highest_price = Column(Float(), nullable=False)
    lowest_price = Column(Float(), nullable=False)
    close_price = Column(Float(), nullable=False)
    volume = Column(Float(), nullable=False)
    close_time = Column(DateTime(), nullable=False)
    quote_asset_volume = Column(Float(), nullable=False)
    number_of_trades = Column(Integer(), nullable=False)
    taker_buy_base_asset_volume = Column(Float(), nullable=False)
    taker_buy_quote_asset_volume = Column(Float(), nullable=False)

    def __str__(self):
        return f'[{self.symbol}] at {self.open_time.strftime("%F, %r")}'

    @classmethod
    def from_api(cls, symbol, candle_data):
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

        dict_data = {
            'symbol': symbol,
            'open_time': datetime.fromtimestamp(candle_data[0] / 1000),
            'open_price': float(candle_data[1]),
            'highest_price': float(candle_data[2]),
            'lowest_price': float(candle_data[3]),
            'close_price': float(candle_data[4]),
            'volume': float(candle_data[5]),
            'close_time': datetime.fromtimestamp(candle_data[6] / 1000),
            'quote_asset_volume': float(candle_data[7]),
            'number_of_trades': candle_data[8],
            'taker_buy_base_asset_volume': float(candle_data[9]),
            'taker_buy_quote_asset_volume': float(candle_data[10]),
        }

        return cls(**dict_data)
