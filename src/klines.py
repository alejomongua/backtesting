import os
import time
from datetime import datetime

from src.client import client
from src.database import Database, DATABASE_NAME
from src.kline import Kline

TOLERATED_TIME_DELAY = 60 * 5  # 5 Minutes


class Klines():

    def __init__(self, symbol):
        self.symbol = symbol
        self.next_candle = 0
        self.database = Database()

    def get_data_from_api(self):
        # Check if database exists
        if not os.path.exists(DATABASE_NAME):
            self.database.create_model(Kline)
        last_time = 0
        while (last_time / 1000) < time.time() - TOLERATED_TIME_DELAY:
            data = client.get_klines(symbol=self.symbol,
                                     interval='1m',
                                     startTime=last_time,
                                     limit=1000)
            klines = [Kline.from_api(self.symbol, item) for item in data]
            self.database.persist(klines)
            last_kline = klines[-1]
            last_time = int(datetime.timestamp(last_kline.close_time) * 1000)
            print(f'Stored until {last_kline.close_time.strftime("%F %r")}')
