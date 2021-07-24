import os
import json
import logging

from binance.client import Client

SEGUNDOS_POR_DIA = 60 * 60 * 24

DIR_PATH = os.path.dirname(os.path.realpath(__file__))
CONFIG_FILE = DIR_PATH + "/../config.json"
LOG_FILE_PATH = DIR_PATH + '/../logger.log'
logging.basicConfig(filename=LOG_FILE_PATH, level=logging.DEBUG)

try:
    configuracion = json.load(open(CONFIG_FILE))
    api_key = configuracion["key"]
    api_secret = configuracion["secret"]
    client = Client(api_key, api_secret)
except FileNotFoundError:
    print(f'No hay archivo de configuración {CONFIG_FILE}')
