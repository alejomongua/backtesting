import time

from database import Database
from kline import Kline
from client import Client


class Klines():
    def __init__(self):
        self.current_index = 0
        self.database = Database()

    def generate_schema(self):
        DEFAULT_SCHEMA = """
        CREATE TABLE klines (id integer primary key autoincrement,
            symbol char(20)
            open_time float
            open_price float
            highest_price float
            lowest_price float
            close_price float
            volume float
            close_time float
            quote_asset_volume float
            number_of_trades integer
            taker_buy_base_asset_volume float
            taker_buy_quote_asset_volume float);
        """

        self.database.execute(DEFAULT_SCHEMA)
        self.database.execute('CREATE INDEX klines_symbol ON klines (symbol)')
        self.database.execute(
            'CREATE INDEX klines_open_time ON klines (open_time)')

    def next_kline(self):
        self.database.execute('select * from klines where id > ? limit 1',
                              (self.current_index,))

        response = self.database.fetchone()
        self.current_index, symbol, *kline_tuple = response
        return Kline(symbol, kline_tuple)

    def store(self, kline: Kline):
        fields = kline.to_dict()
        fields_names = ', '.join([f':{field}' for field in fields.keys()])
        questions_marks = ', '.join('?' * len(fields.keys()))
        self.database.execute(
            f'insert into klines ({fields_names}) values ({questions_marks})', fields)

    def query_binance(self, symbol):
        client = Client()
        interval = Client.KLINE_INTERVAL_1MINUTE
        empezar = 0
        # desfase tolerable máximo 5 minutos
        while empezar / 1000 < time.time() - 300:
            salida = client.get_klines(
                symbol=symbol, interval=interval, startTime=empezar, limit=1000)
            for item in salida:
                kline = Kline(symbol, item)
                self.store(kline)
                empezar = kline.close_time
