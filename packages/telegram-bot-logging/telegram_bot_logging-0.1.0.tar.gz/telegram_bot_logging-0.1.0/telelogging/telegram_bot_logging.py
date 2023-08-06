import os
import logging
from time import gmtime, strftime
from typing import List

import requests
from pymongo import MongoClient


def serialize(data: dict)-> str:
    """Serialize data to string"""
    return str(data).replace("'", '"').replace(':', "-> ").replace(',', "\n").replace('{', "").replace('}', "").replace("[", "").replace("]", "")

def convert_to_dict(data)-> dict:
    """Convert data to dict"""
    data = dict(data)
    data.pop('_id')
    return data


class TelegramBot():
    def __init__(self, token: str, chat_id: str='1332428308'):
        self.token = token
        self.chat_id = chat_id
        self.base_url = f'https://api.telegram.org/bot{self.token}/'

    def send_message(self, message: str):
        url = self.base_url + 'sendMessage'
        data = {
            'chat_id': self.chat_id,
            'text': message
        }
        requests.post(url, data=data)


class LoggerHandler(logging.Handler):

    def __init__(self, service_name: str):
        self.client =  MongoClient(os.environ.get("LOGGING_DATABASE_URL", 'mongodb://127.0.0.1:27017/'))
        self.db = self.client['logging']
        self.collection = self.db[service_name]

    def save_data(self, record):
        database_record = {
            "level": record['levelname'],
            "module": record['module'],
            "line": record['lineno'],
            "asctime": record['asctime'] if getattr(record, "asctime", None) else strftime("%Y-%m-%d %H:%M", gmtime()),
            "message": record['message']
        }
        self.collection.insert_one(database_record)
     
    def get_data(self, limit:int=5)-> List[dict]:
        data = list(map(convert_to_dict, self.collection.find()[0:limit]))
        return data

