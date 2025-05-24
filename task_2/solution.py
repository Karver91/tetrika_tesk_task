import csv
import os
import time
from datetime import datetime

import requests

API_URL = "https://ru.wikipedia.org/w/api.php"
# CYRILLIC_LETTERS = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЭЮЯ"

QUERY_PARAMS = {
    "action": "query",
    "list": "categorymembers",
    "cmtitle": f"Категория:Животные_по_алфавиту",
    "cmlimit": 500,
    "format": "json",
    "cmprop": "title"
}


class FileManager:
    def __init__(self, data):
        self.data = data
        self.file_name = 'beasts.csv'
        self.file_path = self.data_file_path()

    def write_file(self):
        with open(file=self.file_path, mode='w', encoding='utf-8') as file:
            writer = csv.writer(file)
            for key, value in self.data.items():
                writer.writerow((key, value))


    @staticmethod
    def __get_current_date():
        current_date = datetime.now()
        year = current_date.strftime('%Y')
        month = current_date.strftime('%m')
        day = current_date.strftime('%d')
        return year, month, day

    def data_file_path(self):
        current_date = self.__get_current_date()
        current_dir = os.path.dirname(os.path.abspath(__file__))
        data_dir_path = os.path.join(current_dir, "data", *current_date)
        if not os.path.exists(data_dir_path):
            os.makedirs(data_dir_path)
        return os.path.join(data_dir_path, self.file_name)


class Parser:
    def __init__(self, repository, session):
        self.session = session
        self.repository = repository

    def run(self):
        self.start_pulling()
        self.repository.write_file()

    def start_pulling(self):
        while True:
            response = self.__make_request(url=API_URL, params=QUERY_PARAMS)
            response_data = response.json()
            self.parse_data(response_data)
            if not "continue" in response_data:
                break
            QUERY_PARAMS.update(response_data["continue"])

    def parse_data(self, response_data):
        categorymembers = response_data["query"]["categorymembers"]
        for member in categorymembers:
            title = member["title"]
            first_letter = title[0].upper()
            self.repository.data.setdefault(first_letter, 0)
            self.repository.data[first_letter] += 1

    def __make_request(
            self,
            url: str,
            timeout: int = 0.5,
            **kwargs
    ):
        response = self.session.get(url=url, **kwargs)
        time.sleep(timeout)
        print(self.repository.data)
        return response


# beasts_counter = {char: 0 for char in CYRILLIC_LETTERS}
beasts_counter = dict()
session = requests.Session()
repository = FileManager(data=beasts_counter)
parser = Parser(repository=repository, session=session)

if __name__ == '__main__':
    parser.run()
