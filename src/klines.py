import os
import time
from datetime import datetime

from sqlalchemy import desc

from src.client import client
from src.database import Database, DATABASE_NAME
from src.kline import Kline

TOLERATED_TIME_DELAY = 60 * 5  # 5 Minutes


class Klines():

    def __init__(self, symbol):
        self.symbol = symbol
        self.last_candle_index = 0
        self.database = Database()

    def fill_database_from_api(self):
        # Check if database exists
        def get_initial_last_time():
            if not os.path.exists(DATABASE_NAME):
                self.database.create_model(Kline)
                return 0
            session = self.database.get_session()
            kline = session.query(Kline)\
                .order_by(desc(Kline.id))\
                .filter(Kline.symbol == self.symbol)\
                .first()
            if kline is None:
                return 0
            return int(datetime.timestamp(kline.close_time) * 1000)

        last_time = get_initial_last_time()
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

    def get_next_from_database(self):
        session = self.database.get_session()
        kline = session.query(Kline)\
            .order_by(Kline.id)\
            .filter(Kline.id > self.last_candle_index, Kline.symbol == self.symbol)\
            .first()
        if kline is None:
            return None
        self.last_candle_index = kline.id
        return kline

    def get_first_candles(self, quantity):
        klines = self.database\
            .get_session()\
            .query(Kline)\
            .order_by(Kline.id)\
            .limit(quantity)
        self.last_candle_index = klines[-1].id
        return klines

    # Iterator interface

    def __iter__(self):
        return self

    def __next__(self):
        kline = self.get_next_from_database()
        if kline is None:
            raise StopIteration
        return kline
